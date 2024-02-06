

import logging

from flask import Flask, request, render_template, jsonify
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

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
    def __init__(self):
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

# 实例化AttractionSystem
system = AttractionSystem()

@app.route('/tourism', methods=['GET', 'POST'])
def main_page():
    user_id = request.args.get('user_id')
    if request.method == 'POST':
        return render_template('main_page.html')
    else:
        return render_template('main_page.html')  # 处理GET请求


@app.route('/tourism/submit', methods=['GET', 'POST'])
def submit_place():
    if request.method == 'POST':
        data = request.form
        ###加了改小写
        country = data.get('country', '').lower()  # 转换为小写
        place = data.get('place', '').lower()  # 转换为小写
        type = data.get('type', '').lower()

        ###加了type报错
        valid_types = ['natural attractions', 'cultural and historical attractions', 'modern entertainment attractions']
        if type not in valid_types:
            # 如果类型无效，渲染并返回一个错误页面
            return render_template('error.html', error="Invalid type provided. Please choose a valid attraction type.")
        
        try:
            # 确保这里的字段与HTML表单的name属性相匹配
            attraction = Attraction(data['place'], data['country'], data['type'],data['postalCode'])
            system.insert_attraction(attraction)

            return jsonify({"message": "Successfully submitted!"}), 200
        except KeyError as e:
            return jsonify({"message": "Invalid input! Missing data."}), 400
    else:
        # GET请求时显示表单
        return render_template('submit_place.html')
#不要回到jsonify，直接在下面跳出成功提交



@app.route('/tourism/VoteHistory', methods=['GET'])
def voting_history():
    user_id = request.args.get('user_id')
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


# 新建一个视图函数用于显示景点的投票信息
@app.route('/tourism/PlaceVoteInfo/<name>', methods=['GET','POST'])
def vote(name):
    if request.method == 'GET':
        attraction_node = system.attractions.find(name)
        attraction = attraction_node.data
        
        # 将景点信息转换为可以序列化的字典列表
        attraction_dict = {
            'name': attraction.name,
            'country': attraction.country,
            'type': attraction.type,
            'postcode': attraction.postcode,
            'votes': attraction.votes,
            'comments': attraction.comments
        }
            
        # 渲染模板并传递数据
        return render_template('votes.html', attraction=attraction, attraction_dict=attraction_dict)
    
    # elif request.method == 'POST':
    #     # 从哪里获取？
    #     user_id = request.args.get('user_id')
    #     user_node = system.users.find(user_id)
    #     if user_node:
    #         user = user_node.data
    #         return render_template('voting_history.html', user=user)
        
    #     attraction_node = system.vote(user_id, name, comment)   

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

