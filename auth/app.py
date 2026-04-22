from flask import Flask, jsonify, request
from pymongo import MongoClient
import hashlib
import time
import os
import bson

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongodb:27017/shopwave")
client = MongoClient(MONGO_URI)
db = client.shopwave
users_col = db.users
tokens_col = db.tokens

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token(user_id):
    token = hashlib.sha256(f"{user_id}{time.time()}".encode()).hexdigest()
    tokens_col.insert_one({"token": token, "user_id": str(user_id)})
    return token

def get_user_from_token(req):
    auth = req.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = auth[7:]
        record = tokens_col.find_one({"token": token})
        if record:
            user = users_col.find_one({"_id": bson.ObjectId(record["user_id"])})
            if user:
                return user
    return None

def serialize_user(user):
    return {
        "id": str(user["_id"]),
        "name": user.get("name", ""),
        "email": user.get("email", "")
    }

@app.route('/health')
def health():
    try:
        client.admin.command('ping')
        return jsonify({"status": "ok", "service": "auth-service", "db": "connected"})
    except Exception as e:
        return jsonify({"status": "ok", "service": "auth-service", "db": "disconnected"})

@app.route('/api/users/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "email and password required"}), 400
    if users_col.find_one({"email": data["email"]}):
        return jsonify({"error": "Email already exists"}), 409
    user = {
        "name": data.get("name", ""),
        "email": data["email"],
        "password": hash_password(data["password"]),
        "role": "user",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    result = users_col.insert_one(user)
    user["_id"] = result.inserted_id
    token = generate_token(str(result.inserted_id))
    return jsonify({
        "message": "User registered successfully",
        "token": token,
        "user": serialize_user(user)
    }), 201

@app.route('/api/users/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "email and password required"}), 400
    user = users_col.find_one({"email": data["email"], "password": hash_password(data["password"])})
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401
    token = generate_token(str(user["_id"]))
    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": serialize_user(user)
    })

@app.route('/api/users/profile', methods=['GET'])
def profile():
    user = get_user_from_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(serialize_user(user))

@app.route('/api/users/profile', methods=['PUT'])
def update_profile():
    user = get_user_from_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    if data.get("name"):
        users_col.update_one({"_id": user["_id"]}, {"$set": {"name": data["name"]}})
        user["name"] = data["name"]
    return jsonify({"message": "Profile updated", "user": serialize_user(user)})

@app.route('/api/users', methods=['GET'])
def list_users():
    users = list(users_col.find({}, {"password": 0}))
    return jsonify([serialize_user(u) for u in users])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)