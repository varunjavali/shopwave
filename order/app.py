from flask import Flask, jsonify, request
from pymongo import MongoClient
import time
import os
import bson

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongodb:27017/shopwave")
client = MongoClient(MONGO_URI)
db = client.shopwave
orders_col = db.orders

def serialize_order(o):
    o["id"] = str(o["_id"])
    del o["_id"]
    return o

@app.route('/health')
def health():
    try:
        client.admin.command('ping')
        return jsonify({"status": "ok", "service": "order-service", "db": "connected"})
    except:
        return jsonify({"status": "ok", "service": "order-service", "db": "disconnected"})

@app.route('/api/orders', methods=['GET'])
def list_orders():
    user_id = request.args.get("user_id")
    query = {"user_id": user_id} if user_id else {}
    orders = [serialize_order(o) for o in orders_col.find(query)]
    return jsonify({"orders": orders, "total": len(orders)})

@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    try:
        o = orders_col.find_one({"_id": bson.ObjectId(order_id)})
        if o:
            return jsonify(serialize_order(o))
    except:
        pass
    return jsonify({"error": "Order not found"}), 404

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    if not data or not data.get("items"):
        return jsonify({"error": "items required"}), 400
    total = sum(item.get("price", 0) * item.get("quantity", 1) for item in data["items"])
    order = {
        "user_id": data.get("user_id", ""),
        "items": data["items"],
        "total": total,
        "status": "pending",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    result = orders_col.insert_one(order)
    order["_id"] = result.inserted_id
    return jsonify(serialize_order(order)), 201

@app.route('/api/orders/<order_id>', methods=['PATCH'])
def update_order(order_id):
    data = request.get_json()
    try:
        result = orders_col.find_one_and_update(
            {"_id": bson.ObjectId(order_id)},
            {"$set": {"status": data.get("status", "pending")}},
            return_document=True
        )
        if result:
            return jsonify({"message": "Order updated", "order": serialize_order(result)})
    except:
        pass
    return jsonify({"error": "Order not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3003)