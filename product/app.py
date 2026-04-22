from flask import Flask, jsonify, request
from pymongo import MongoClient
import time
import os
import bson

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongodb:27017/shopwave")
client = MongoClient(MONGO_URI)
db = client.shopwave
products_col = db.products

# Seed products if collection is empty
SEED_PRODUCTS = [
    {"name": "Laptop Pro", "category": "electronics", "price": 75000, "stock": 10, "rating": 4.5, "review_count": 120, "description": "High performance laptop for professionals", "image_emoji": "💻"},
    {"name": "Smartphone X", "category": "electronics", "price": 25000, "stock": 15, "rating": 4.3, "review_count": 95, "description": "Latest flagship smartphone", "image_emoji": "📱"},
    {"name": "Noise Cancelling Headphones", "category": "electronics", "price": 8000, "stock": 25, "rating": 4.6, "review_count": 200, "description": "Premium noise cancelling headphones", "image_emoji": "🎧"},
    {"name": "Smart TV 55\"", "category": "electronics", "price": 45000, "stock": 8, "rating": 4.4, "review_count": 75, "description": "4K Smart TV with HDR", "image_emoji": "📺"},
    {"name": "Wireless Mouse", "category": "electronics", "price": 1500, "stock": 50, "rating": 4.2, "review_count": 180, "description": "Ergonomic wireless mouse", "image_emoji": "🖱️"},
    {"name": "Mechanical Keyboard", "category": "electronics", "price": 4500, "stock": 30, "rating": 4.7, "review_count": 145, "description": "RGB mechanical keyboard", "image_emoji": "⌨️"},
    {"name": "Tablet Pro", "category": "electronics", "price": 35000, "stock": 12, "rating": 4.5, "review_count": 88, "description": "10 inch tablet with stylus support", "image_emoji": "📟"},
    {"name": "Smart Watch", "category": "electronics", "price": 12000, "stock": 20, "rating": 4.3, "review_count": 110, "description": "Fitness tracking smart watch", "image_emoji": "⌚"},
    {"name": "Cotton T-Shirt", "category": "clothing", "price": 599, "stock": 100, "rating": 4.1, "review_count": 300, "description": "Premium cotton round neck t-shirt", "image_emoji": "👕"},
    {"name": "Slim Fit Jeans", "category": "clothing", "price": 1499, "stock": 60, "rating": 4.3, "review_count": 220, "description": "Comfortable slim fit denim jeans", "image_emoji": "👖"},
    {"name": "Running Shoes", "category": "clothing", "price": 3500, "stock": 40, "rating": 4.6, "review_count": 175, "description": "Lightweight running shoes", "image_emoji": "👟"},
    {"name": "Leather Jacket", "category": "clothing", "price": 5999, "stock": 25, "rating": 4.4, "review_count": 90, "description": "Genuine leather biker jacket", "image_emoji": "🧥"},
    {"name": "Formal Shirt", "category": "clothing", "price": 1299, "stock": 70, "rating": 4.2, "review_count": 140, "description": "Wrinkle-free formal shirt", "image_emoji": "👔"},
    {"name": "Sports Cap", "category": "clothing", "price": 499, "stock": 80, "rating": 4.0, "review_count": 95, "description": "UV protection sports cap", "image_emoji": "🧢"},
    {"name": "Python Programming", "category": "books", "price": 799, "stock": 50, "rating": 4.8, "review_count": 450, "description": "Complete Python programming guide", "image_emoji": "📗"},
    {"name": "Data Structures & Algorithms", "category": "books", "price": 899, "stock": 40, "rating": 4.7, "review_count": 320, "description": "Master DSA for coding interviews", "image_emoji": "📘"},
    {"name": "The Alchemist", "category": "books", "price": 299, "stock": 100, "rating": 4.9, "review_count": 800, "description": "Paulo Coelho's masterpiece", "image_emoji": "📕"},
    {"name": "Atomic Habits", "category": "books", "price": 499, "stock": 75, "rating": 4.8, "review_count": 650, "description": "Build good habits, break bad ones", "image_emoji": "📙"},
    {"name": "System Design Interview", "category": "books", "price": 999, "stock": 30, "rating": 4.7, "review_count": 280, "description": "Ace your system design interviews", "image_emoji": "📒"},
    {"name": "Football", "category": "sports", "price": 1200, "stock": 35, "rating": 4.4, "review_count": 160, "description": "FIFA approved match football", "image_emoji": "⚽"},
    {"name": "Cricket Bat", "category": "sports", "price": 2500, "stock": 20, "rating": 4.5, "review_count": 130, "description": "English willow cricket bat", "image_emoji": "🏏"},
    {"name": "Yoga Mat", "category": "sports", "price": 800, "stock": 55, "rating": 4.6, "review_count": 210, "description": "Non-slip premium yoga mat", "image_emoji": "🧘"},
    {"name": "Dumbbells Set", "category": "sports", "price": 3500, "stock": 15, "rating": 4.7, "review_count": 145, "description": "Adjustable dumbbells 5-25kg", "image_emoji": "🏋️"},
    {"name": "Badminton Racket", "category": "sports", "price": 1800, "stock": 28, "rating": 4.3, "review_count": 98, "description": "Professional badminton racket", "image_emoji": "🏸"},
    {"name": "LEGO City Set", "category": "toys", "price": 3999, "stock": 20, "rating": 4.8, "review_count": 185, "description": "Creative LEGO city building set", "image_emoji": "🧱"},
    {"name": "Remote Control Car", "category": "toys", "price": 1500, "stock": 30, "rating": 4.4, "review_count": 120, "description": "High speed RC car", "image_emoji": "🚗"},
    {"name": "Board Game - Chess", "category": "toys", "price": 699, "stock": 45, "rating": 4.6, "review_count": 200, "description": "Premium wooden chess set", "image_emoji": "♟️"},
    {"name": "Rubik's Cube", "category": "toys", "price": 299, "stock": 60, "rating": 4.5, "review_count": 350, "description": "Original 3x3 speed cube", "image_emoji": "🎲"},
]

def seed_products():
    if products_col.count_documents({}) == 0:
        for p in SEED_PRODUCTS:
            p["created_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        products_col.insert_many(SEED_PRODUCTS)
        print(f"Seeded {len(SEED_PRODUCTS)} products")

seed_products()

def serialize_product(p):
    p["id"] = str(p["_id"])
    del p["_id"]
    return p

@app.route('/health')
def health():
    try:
        client.admin.command('ping')
        return jsonify({"status": "ok", "service": "product-service", "db": "connected"})
    except:
        return jsonify({"status": "ok", "service": "product-service", "db": "disconnected"})

@app.route('/api/products', methods=['GET'])
def list_products():
    limit = int(request.args.get('limit', 12))
    page = int(request.args.get('page', 1))
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    query = {}
    if category:
        query['category'] = category
    if search:
        query['name'] = {'$regex': search, '$options': 'i'}
    if min_price or max_price:
        query['price'] = {}
        if min_price:
            query['price']['$gte'] = float(min_price)
        if max_price:
            query['price']['$lte'] = float(max_price)

    total = products_col.count_documents(query)
    skip = (page - 1) * limit
    products = [serialize_product(p) for p in products_col.find(query).skip(skip).limit(limit)]

    return jsonify({
        "products": products,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    })

@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    try:
        p = products_col.find_one({"_id": bson.ObjectId(product_id)})
        if p:
            return jsonify(serialize_product(p))
    except:
        pass
    return jsonify({"error": "Product not found"}), 404

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data or not data.get("name") or not data.get("price"):
        return jsonify({"error": "name and price required"}), 400
    product = {
        "name": data["name"],
        "category": data.get("category", "general"),
        "price": data["price"],
        "stock": data.get("stock", 0),
        "rating": data.get("rating", 0),
        "review_count": data.get("review_count", 0),
        "description": data.get("description", ""),
        "image_emoji": data.get("image_emoji", "📦"),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    result = products_col.insert_one(product)
    product["_id"] = result.inserted_id
    return jsonify(serialize_product(product)), 201

@app.route('/api/products/<product_id>', methods=['PATCH'])
def update_product(product_id):
    data = request.get_json()
    try:
        result = products_col.find_one_and_update(
            {"_id": bson.ObjectId(product_id)},
            {"$set": data},
            return_document=True
        )
        if result:
            return jsonify({"message": "Updated", "product": serialize_product(result)})
    except:
        pass
    return jsonify({"error": "Product not found"}), 404

@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        result = products_col.delete_one({"_id": bson.ObjectId(product_id)})
        if result.deleted_count:
            return jsonify({"message": "Product deleted"})
    except:
        pass
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002)