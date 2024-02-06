import logging

from flask import Flask, request, render_template, jsonify, session, request
import matplotlib.pyplot as plt
import io
import base64
import sys

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
        self.name = name
        self.country = country
        self.type = type
        self.postcode = postcode
        self.votes = 0
        self.comments = []

    def add_vote(self, comment):
        self.votes += 1
        self.comments.append(comment)

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.vote_history = BinarySearchTree()

    def add_vote(self, attraction_name, comment):
        self.vote_history.insert(attraction_name, comment)

class AttractionSystem:
    
    votes_file = "votes.txt"
    places_file = "places.txt"
    
    def __init__(self):
        #Initialize records cx0206
        # try:
        #     with open(self.votes_file, "r") as file:
        #         lines = file.readlines() 
        #         if not lines:
        #             print("No previous user info.")
        #         else:
        #             for line in lines:
        #                 parts = line.strip().split("||")
        #                 user_id = parts[0]
        #                 if not self.users.find(user_id):
        #                     self.users.insert(user_id, User(user_id))
        #                 for part in parts[1:]:
        #                     elements = part.strip().split('|')
        #                     place_voted = elements[0].strip()
        #                     vote_comment = elements[1].strip()
        #                     user_node = self.users.find(user_id)
        #                     user_node.data.vote_history.insert(place_voted, vote_comment)
        #             print("Votings loaded successfully.")
        # except FileNotFoundError:
        #     print(f"{self.votes_file} not found, starting fresh.")
        # try:
        #     with open(self.places_file, "r") as file:
        #         lines = file.readlines() 
        #         if not lines:
        #             print("No previous attraction info.")
        #         else:
        #             for line in lines:
        #                 parts = line.strip().split("||")
        #                 name, country, type, postcode, votes, comments = parts
        #                 attraction = Attraction(name, country, type, postcode)
        #                 attraction.votes = int(votes)
        #                 attraction.comments = comments.split("|")  
        #                 self.attractions.insert(name, attraction)
        #             print("Attractions loaded successfully.")
        # except FileNotFoundError:
        #     print(f"{self.places_file} not found, starting fresh.")  
            
        self.users = BinarySearchTree()
        self.countries = BinarySearchTree()
        self.types = BinarySearchTree()
        self.attractions = BinarySearchTree()

    def insert_attraction(self, attraction):
        # Insert into country BST
        country_node = self.countries.find(attraction.country)
        if not country_node:
            country_tree = BinarySearchTree()
            self.countries.insert(attraction.country, country_tree)
            country_node = self.countries.find(attraction.country)
        
        # Insert attraction into the country's BST
        country_node.data.insert(attraction.name, attraction)
    
        # Insert into type BST
        type_node = self.types.find(attraction.type)
        if not type_node:
            type_tree = BinarySearchTree()
            self.types.insert(attraction.type, type_tree)
            type_node = self.types.find(attraction.type)
        
        # Insert attraction into the type's BST
        type_node.data.insert(attraction.name, attraction)
    
        # Insert into attractions BST
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
        country_node = self.countries.find(country_name)
        if country_node:
            return [attraction.data for attraction in country_node.data.root.inorder()]
        else:
            return [] 

    def get_attractions_by_type(self, type_name):
        type_node = self.types.find(type_name)
        if type_node:
            return [attraction.data for attraction in type_node.data.root.inorder()]
        else:
            return []
                
    # quit system and save votes and place info into txt files cx0206
    def quit(self):
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
                    file.write(line+"\n")     
        else:   
            print("No voting records to save.")
            
        if self.attractions.root:
            with open(self.places_file, "w") as file:
                for attraction_node in self.attractions.root.inorder():
                    attraction = attraction_node.data
                    comments_str = "|".join(attraction.comments)
                    line = f"{attraction.name}||{attraction.country}||{attraction.type}||{attraction.postcode}||{attraction.votes}||{comments_str}\n"
                    file.write(line)  
        else:   
            print("No attraction records to save.")
        sys.exit(0)

# 实例化AttractionSystem
system = AttractionSystem()

@app.route('/tourism', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        # 将用户ID存储在会话中 0206
        user_id = request.form.get('user_id')
        session['user_id'] = user_id  
        with open("id.txt", "w") as file:
            file.write(user_id)
        return render_template('main_page.html')
    else:
        return render_template('main_page.html')


@app.route('/tourism/submit', methods=['GET', 'POST'])
def submit_place():
    if request.method == 'POST':
        data = request.form
        user_id = session.get('user_id')
        valid_types = ['natural attractions', 'cultural and historical attractions', 'modern entertainment attractions']
        if type not in valid_types:
            return render_template('error.html', error="Invalid type provided. Please choose a valid attraction type.")

        try:
            attraction = Attraction(data['place'].lower(), data['country'].lower(), data['type'].lower(), data['postalCode'])
            system.insert_attraction(attraction)
            # 重定向到该地点的投票页面
            return redirect(url_for('place_vote_info', name=attraction.name))
        except KeyError as e:
            return render_template('error.html', error="Invalid input! Missing data.")

    else:
        return render_template('submit_place.html')




@app.route('/tourism/VoteHistory', methods=['GET'])
def voting_history():
    user_id = session.get('user_id')
    user_node = system.users.find(user_id)
    if user_node:
        user = user_node.data
        return render_template('voting_history.html', user=user)
    return render_template('user_not_found.html')


@app.route('/tourism/PlaceVoteInfo', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('filtered_places.html', attractions=[])

    elif request.method == 'POST':
        data = request.form
        country_name = data.get('country', default="", type=str)
        type_name = data.get('type', default="", type=str)

        if country_name and type_name:
            attractions = system.get_attractions_by_country(country_name)
            attractions = [attr for attr in attractions if attr.type == type_name]
        elif country_name:
            attractions = system.get_attractions_by_country(country_name)
        elif type_name:
            attractions = system.get_attractions_by_type(type_name)
        else:
            attractions = []

        # 将景点信息转换为可以序列化的字典列表
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
    app.logger.info(f"Looking up attraction '{name}'.")
    attraction_node = system.attractions.find(name)
    if attraction_node:
        attraction = attraction_node.data
        app.logger.info(f"Attraction '{name}' found with {attraction.votes} votes.")
        if request.method == 'POST':
            data = request.json
            comment = data.get('comment', '')
            attraction_node = system.attractions.find(name)
            if attraction_node:
                attraction = attraction_node.data
                attraction.add_vote(comment)  # Make sure the Attraction class has this method
                # After a vote is submitted successfully, return a JSON response
                return jsonify({"message": "Vote submitted successfully"}), 200
            else:
                # If the attraction is not found, return a JSON error response
                return jsonify({"error": "Attraction not found"}), 404
        else:
            # GET logic here
            attraction_node = system.attractions.find(name)
            if attraction_node:
                attraction = attraction_node.data
            return render_template('votes.html', attraction=attraction)
    else:
        app.logger.error(f"Attraction '{name}' not found.")
        return jsonify({"error": "Attraction not found"}), 404





@app.route('/tourism/Analysis', methods=['GET'])
def analysis():
    # 获取前10名票数景点
    all_attractions = [attraction.data for attraction in system.attractions.root.inorder()]
    top_10_attractions = sorted(all_attractions, key=lambda x: x.votes, reverse=True)[:10]

    # 生成图表
    names = [attraction.name for attraction in top_10_attractions]
    votes = [attraction.votes for attraction in top_10_attractions]

    plt.figure(figsize=(10, 6))
    plt.barh(names, votes)
    plt.xlabel('Number of Votes')
    plt.title('Top 10 Attractions by Votes')
    
    # 将图表保存为字节流
    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    
    # 将图表转换为Base64编码以嵌入到HTML页面
    img_base64 = base64.b64encode(img_data.read()).decode()
    
    return render_template('analysis.html', img_base64=img_base64)

if __name__ == '__main__':
    app.run(debug=True,port=5050)
