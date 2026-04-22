from flask import Flask, jsonify, request
from pymongo import MongoClient
import time
import os
import bson

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongodb:27017/shopwave")
client = MongoClient(MONGO_URI)
db = client.shopwave
payments_col = db.payments

def serialize_payment(p):
    p["id"] = str(p["_id"])
    del p["_id"]
    return p

@app.route('/health')
def health():
    try:
        client.admin.command('ping')
        return jsonify({"status": "ok", "service": "payment-service", "db": "connected"})
    except:
        return jsonify({"status": "ok", "service": "payment-service", "db": "disconnected"})

@app.route('/api/payments', methods=['GET'])
def list_payments():
    payments = [serialize_payment(p) for p in payments_col.find()]
    return jsonify({"payments": payments, "total": len(payments)})

@app.route('/api/payments/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    try:
        p = payments_col.find_one({"_id": bson.ObjectId(payment_id)})
        if p:
            return jsonify(serialize_payment(p))
    except:
        pass
    return jsonify({"error": "Payment not found"}), 404

@app.route('/api/payments', methods=['POST'])
def create_payment():
    data = request.get_json()
    if not data or not data.get("order_id") or not data.get("amount"):
        return jsonify({"error": "order_id and amount required"}), 400
    payment = {
        "order_id": data["order_id"],
        "amount": data["amount"],
        "method": data.get("method", "card"),
        "status": "success",
        "transaction_id": f"TXN{int(time.time())}",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    result = payments_col.insert_one(payment)
    payment["_id"] = result.inserted_id
    return jsonify(serialize_payment(payment)), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3004)