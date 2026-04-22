from flask import Flask, jsonify, request
from pymongo import MongoClient
import time
import os
import bson

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongodb:27017/shopwave")
client = MongoClient(MONGO_URI)
db = client.shopwave
notifs_col = db.notifications

def serialize_notif(n):
    n["id"] = str(n["_id"])
    del n["_id"]
    return n

@app.route('/health')
def health():
    try:
        client.admin.command('ping')
        return jsonify({"status": "ok", "service": "notification-service", "db": "connected"})
    except:
        return jsonify({"status": "ok", "service": "notification-service", "db": "disconnected"})

@app.route('/api/notifications', methods=['GET'])
def list_notifications():
    user_id = request.args.get("user_id")
    query = {"user_id": user_id} if user_id else {}
    notifs = [serialize_notif(n) for n in notifs_col.find(query)]
    return jsonify({"notifications": notifs, "total": len(notifs)})

@app.route('/api/notifications', methods=['POST'])
def create_notification():
    data = request.get_json()
    if not data or not data.get("message"):
        return jsonify({"error": "message required"}), 400
    notif = {
        "user_id": data.get("user_id", ""),
        "message": data["message"],
        "type": data.get("type", "info"),
        "read": False,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    result = notifs_col.insert_one(notif)
    notif["_id"] = result.inserted_id
    return jsonify(serialize_notif(notif)), 201

@app.route('/api/notifications/<notif_id>/read', methods=['PATCH'])
def mark_read(notif_id):
    try:
        result = notifs_col.find_one_and_update(
            {"_id": bson.ObjectId(notif_id)},
            {"$set": {"read": True}},
            return_document=True
        )
        if result:
            return jsonify({"message": "Marked as read", "notification": serialize_notif(result)})
    except:
        pass
    return jsonify({"error": "Notification not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3005)