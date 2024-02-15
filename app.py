import traceback
from flask import Flask, request, render_template, jsonify, session, redirect, url_for  

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

class TreeNode:
    def __init__(self, key, data=None):
        self.key = key
        self.data = data
        self.left = None
        self.right = None

    def inorder(self):
        if self.left:
            yield from self.left.inorder()
        yield self
        if self.right:
            yield from self.right.inorder()

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key, data=None):
        self.root = self._insert_recursive(self.root, key, data)

    def _insert_recursive(self, node, key, data):
        if node is None:
            return TreeNode(key, data)
        if key < node.key:
            node.left = self._insert_recursive(node.left, key, data)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key, data)
        return node

    def find(self, key):
        return self._find_recursive(self.root, key)

    def _find_recursive(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._find_recursive(node.left, key)
        else:
            return self._find_recursive(node.right, key)

class Attraction:
    def __init__(self, name, country, type, postcode):
        self.name = str(name)
        self.country = str(country)
        self.type = str(type)
        self.postcode = str(postcode)
        self.votes = 0
        self.comments = []

    def add_vote(self, comment):
        self.votes += 1
        self.comments.append(str(comment))

class User:
    def __init__(self, user_id):
        self.user_id = str(user_id)
        self.vote_history = BinarySearchTree()

    def add_vote(self, attraction_name, comment):
        self.vote_history.insert(str(attraction_name), str(comment))

class AttractionSystem:
    votes_file = "votes.txt"
    places_file = "places.txt"

    def __init__(self):
        self.users = BinarySearchTree()
        self.countries = BinarySearchTree()
        self.types = BinarySearchTree()
        self.attractions = BinarySearchTree()
        
        try:
            with open(self.votes_file, "r") as file:
                lines = file.readlines()
                if not lines:
                    print("No previous user info.")
                else:
                    for line in lines:
                        parts = line.strip().split("||")
                        user_id = parts[0]
                        if not self.users.find(user_id):
                            self.users.insert(user_id, User(user_id))
                        for part in parts[1:]:
                            elements = part.strip().split('|')
                            place_voted = elements[0].strip()
                            vote_comment = elements[1].strip()
                            user_node = self.users.find(user_id)
                            user_node.data.vote_history.insert(place_voted, vote_comment)
                    print("Votings loaded successfully.")
        except FileNotFoundError:
            print(f"{self.votes_file} not found, starting fresh.")
        try:
            with open(self.places_file, "r") as file:
                lines = file.readlines()
                if not lines:
                    print("No previous attraction info.")
                else:
                    for line in lines:
                        parts = line.strip().split("||")
                        name = parts[0] 
                        country = parts[1] 
                        type = parts[2] 
                        postcode = parts[3] 
                        votes = parts[4] 
                        comments = parts[5]
                        attraction = Attraction(name, country, type, postcode)
                        attraction.votes = int(votes)
                        attraction.comments = comments.split("|")
                        self.insert_attraction(attraction)
                    print("Attractions loaded successfully.")
        except FileNotFoundError:
            print(f"{self.places_file} not found, starting fresh.")



    def insert_attraction(self, attraction):
        country_node = self.countries.find(attraction.country)
        if not country_node:
            country_tree = BinarySearchTree()
            self.countries.insert(attraction.country, country_tree)
            country_node = self.countries.find(attraction.country)
        
        country_node.data.insert(attraction.name, attraction)
    
        type_node = self.types.find(attraction.type)
        if not type_node:
            type_tree = BinarySearchTree()
            self.types.insert(attraction.type, type_tree)
            type_node = self.types.find(attraction.type)
        
        type_node.data.insert(attraction.name, attraction)
    
        self.attractions.insert(attraction.name, attraction)

    def vote(self, user_id, attraction_name, comment):
        user_node = self.users.find(user_id)
        if not user_node:
            self.users.insert(user_id, User(user_id))
        user = user_node.data

        vote_node = user.vote_history.find(attraction_name)
        if vote_node:
            raise ValueError("Invalid vote! Already voted once.")

        attraction_node = self.attractions.find(attraction_name)
        if attraction_node:
            attraction = attraction_node.data
            attraction.add_vote(comment)
            user.add_vote(attraction_name, comment)
        else:
            raise ValueError("Attraction not found")
    
    def get_attractions_by_country(self, country_name):
        country_node = self.countries.find(str(country_name))
        if country_node:
            return [attraction.data for attraction in country_node.data.root.inorder()]
        else:
            return [] 

    def get_attractions_by_type(self, type_name):
        type_node = self.types.find(str(type_name))
        if type_node:
            return [attraction.data for attraction in type_node.data.root.inorder()]
        else:
            return []
                
    def check_postcode_exists(self, postcode):
        if self.attractions.root is not None:  
            for attraction in self.attractions.root.inorder():
                if attraction.data.postcode == postcode:
                    return True
        return False
    
    def save_and_quit(self):
        try:
            if self.users.root:
                with open(self.votes_file, "w") as file:
                    for user_node in self.users.root.inorder():
                        user = user_node.data
                        user_id = user.user_id
                        line = f"{user_id}"
                        vote_histories = user.vote_history
                        for vote_node in vote_histories.root.inorder():
                            place_voted = vote_node.key
                            vote_comment = vote_node.data
                            line += f"||{place_voted}|{vote_comment}"
                        file.write(line + "\n")

            if self.attractions.root:
                with open(self.places_file, "w") as file:
                    for attraction_node in self.attractions.root.inorder():
                        attraction = attraction_node.data
                        comments_str = "|".join(attraction.comments)
                        line = f"{attraction.name}||{attraction.country}||{attraction.type}||{attraction.postcode}||{attraction.votes}||{comments_str}\n"
                        file.write(line)

            return "Data saved successfully and system exited.", 200
        except Exception as e:
            return str(e), 500

system = AttractionSystem()

@app.route('/tourism', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        session['user_id'] = user_id
        return redirect(url_for('main_page'))
    else:
        return render_template('main_page.html')

@app.route('/tourism/quit', methods=['GET'])
def save_and_quit_system():
    return system.save_and_quit()


@app.route('/tourism/submit', methods=['GET', 'POST'])
def submit_place():
    if request.method == 'POST':    
        data = request.form
        country = data.get('country', '').lower()
        place = data.get('place', '').lower()
        type = data.get('type', '').lower()
        postalCode = data.get('postalCode', '')

        if not country.isalpha():
            return jsonify({'message': "Country must contain only letters."}), 400
        elif not place.replace(' ', '').isalpha():
            return jsonify({'message': "Place must contain only letters and spaces."}), 400
        elif type not in ['natural attractions', 'cultural and historical attractions', 'modern entertainment attractions']:
            return jsonify({'message': "Invalid type provided. Please choose a valid attraction type."}), 400
        elif not postalCode.isalnum():
            return jsonify({'message': "Postal code must contain only letters and numbers."}), 400
        elif system.check_postcode_exists(postalCode):
            return jsonify({'message': "Submission failed, postal code already exists in the system."}), 400
        else:
            try:
                attraction = Attraction(place, country, type, postalCode)
                system.insert_attraction(attraction)
                return jsonify({'message': 'Successful submission!'}), 200
            except Exception as e:
                return jsonify({'message': f"Invalid input! {e}."}), 500

    return render_template('submit_place.html')

@app.route('/tourism/VoteHistory', methods=['GET'])
def voting_history(): 
    try:
        user_id = session.get('user_id')
        if not user_id:
            return "User not logged in", 403  

        user_node = system.users.find(user_id)
        if not user_node:
            return "User not found", 404

        vote_history = [{'name': vote_node.key, 'comment': vote_node.data} for vote_node in user_node.data.vote_history.root.inorder()]
        return render_template('voting_history.html', vote_history=vote_history)
    except Exception as e:
        app.logger.error('An error occurred: %s\n%s', e, traceback.format_exc())
        return jsonify({'error': str(e)}), 500


@app.route('/tourism/PlaceVoteInfo', methods=['GET', 'POST'])
def search():
    
    if request.method == 'GET':
        return render_template('filtered_places.html', attractions=[])

    elif request.method == 'POST':
        data = request.form
        country_name = data.get('country', default='').strip().lower()
        type_name = data.get('type', default='').strip().lower()

        if country_name and type_name:
            attractions = system.get_attractions_by_country(country_name)
            attractions = [attr for attr in attractions if attr.type == type_name]
        elif country_name:
            attractions = system.get_attractions_by_country(country_name)
        elif type_name:
            attractions = system.get_attractions_by_type(type_name)
        else:
            attractions = [attr.data for attr in system.attractions.root.inorder()]

        attractions_dict = [{
            'name': attr.name,
            'country': attr.country,
            'type': attr.type,
            'postcode': attr.postcode,
            'votes': attr.votes,
            'comments': attr.comments
        } for attr in attractions]

        return jsonify(attractions_dict)



@app.route('/tourism/PlaceVoteInfo/<name>', methods=['GET', 'POST'])
def place_vote_info(name):
    attraction_node = system.attractions.find(name)
    if attraction_node:
        attraction = attraction_node.data
        if request.method == 'POST':
            data = request.json
            comment = data.get('comment', '')
            user_id = session.get('user_id')
            user_node = system.users.find(user_id)
            if not user_node:
                user = User(user_id)
                system.users.insert(user_id, user)
            else:
                user = user_node.data
                if user.vote_history.find(name):
                    return jsonify({'error': 'You have already voted for this attraction.'}), 400

            if attraction_node:
                attraction.add_vote(comment)
                user.add_vote(name, comment)
                return jsonify({'message': 'Vote submitted successfully'})
            else:
                return jsonify({"error": "Attraction not found"}), 404
        else:
            return render_template('votes.html', attraction=attraction)
    else:
        return jsonify({"error": "Attraction not found"}), 404


@app.route('/tourism/Analysis', methods=['GET', 'POST'])
def analysis():
    if request.method == 'POST':
        data = request.json  
        country_name = data.get('country', '').strip().lower()
        type_name = data.get('type', '').strip().lower()

        if country_name and type_name:
            attractions = system.get_attractions_by_country(country_name)
            attractions = [attr for attr in attractions if attr.type == type_name]
        elif country_name:
            attractions = system.get_attractions_by_country(country_name)
        elif type_name:
            attractions = system.get_attractions_by_type(type_name)
        else:
            attractions = [attr.data for attr in system.attractions.root.inorder()]

        sorted_attractions = sorted(attractions, key=lambda x: x.votes, reverse=True)
        
        top_10_attractions = sorted_attractions[:10]
        
        chart_data = {attr.name: attr.votes for attr in top_10_attractions}

        return jsonify(chart_data)
    else:
        return render_template('votes_analysis.html')

if __name__ == '__main__':
    app.run(debug=True,port=5050)
