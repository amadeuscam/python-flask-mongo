from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util, ObjectId


app = Flask(__name__)
url = "localhost"
database_name = "pythonmongo"
app.config["MONGO_URI"] = f"mongodb://{url}/{database_name}"
mongo = PyMongo(app)


@app.route('/users', methods=['POST'])
def create_user():
    # recibir datos
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if username and email and password:
        hash_password = generate_password_hash(password=password)
        id_mon = mongo.db.users.insert({
            'username': username,
            'email': email,
            "password": hash_password
        })
        return {
            'id': str(id_mon),
            'username': username,
            'email': email,
            "password": hash_password
        }
    else:
        return not_found()


@app.route('/users', methods=['GET'])
def show_users():
    users = mongo.db.users.find()
    res = json_util.dumps(users)
    return Response(res, mimetype="application/json")


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    res = json_util.dumps(user)
    return Response(res, mimetype="application/json"), 200


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = mongo.db.users.delete_one({"_id": ObjectId(user_id)})
    return jsonify({"message": f"user {user_id} se ha borrado"}), 200


@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):

    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if username and email and password:
        hash_password = generate_password_hash(password=password)
        user = mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {
            'username': username,
            'email': email,
            "password": hash_password

        }})
    return jsonify({"message": f"el usuario {user_id} se ha actualizado"}), 200


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': "Recurso no encontrado: " + request.url,
        'status': 404
    }
    return message, 404


if __name__ == "__main__":
    app.run(debug=True)
