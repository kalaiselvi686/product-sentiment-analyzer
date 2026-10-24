import logging
import uuid
from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.errors import PyMongoError, ConnectionFailure
from config import Config

logger = logging.getLogger(__name__)

# Fallback in-memory storage if MongoDB connection fails
in_memory_db = {
    "products": [],
    "reviews": []
}

def get_db():
    """Attempt to return a PyMongo database client or None if offline."""
    if not Config.MONGO_URI or Config.MONGO_URI == "mongodb://localhost:27017/product_sentiment":
        # Check if local Mongo or URI is provided
        pass
    try:
        client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=2000)
        # Force a call to check if connection works
        client.admin.command('ping')
        return client.get_database("product_sentiment")
    except Exception as e:
        logger.warning(f"MongoDB connection unavailable: {e}. Falling back to in-memory DB.")
        return None

def save_product(product_data):
    """Save a product document to MongoDB or in-memory fallback."""
    db = get_db()
    if db is not None:
        try:
            # Check if product with same URL exists
            existing = db.products.find_one({"url": product_data.get("url")})
            if existing:
                db.products.update_one(
                    {"_id": existing["_id"]},
                    {"$set": {
                        "name": product_data.get("name"),
                        "rating": product_data.get("rating"),
                        "total_reviews": product_data.get("total_reviews"),
                        "source": product_data.get("source")
                    }}
                )
                return str(existing["_id"])
            else:
                result = db.products.insert_one(product_data)
                return str(result.inserted_id)
        except PyMongoError as e:
            logger.error(f"Error saving product to MongoDB: {e}")

    # Fallback storage
    pid = str(uuid.uuid4())
    product_data["_id"] = pid
    # Check duplicate in memory
    for idx, p in enumerate(in_memory_db["products"]):
        if p.get("url") == product_data.get("url"):
            in_memory_db["products"][idx].update(product_data)
            return p["_id"]
    in_memory_db["products"].append(product_data)
    return pid

def get_all_products():
    """Retrieve all stored products."""
    db = get_db()
    if db is not None:
        try:
            products = list(db.products.find())
            for p in products:
                p["_id"] = str(p["_id"])
            return products
        except PyMongoError as e:
            logger.error(f"Error reading products from MongoDB: {e}")

    return in_memory_db["products"]

def get_product_by_id(product_id):
    """Retrieve a single product by ID."""
    db = get_db()
    if db is not None:
        try:
            if ObjectId.is_valid(product_id):
                product = db.products.find_one({"_id": ObjectId(product_id)})
                if product:
                    product["_id"] = str(product["_id"])
                    return product
        except PyMongoError as e:
            logger.error(f"Error fetching product from MongoDB: {e}")

    for p in in_memory_db["products"]:
        if p["_id"] == product_id:
            return p
    return None

def save_reviews(product_id, reviews):
    """Save review documents linked to product_id."""
    db = get_db()
    formatted_reviews = []
    for r in reviews:
        doc = {
            "product_id": str(product_id),
            "review_text": r.get("review_text", r.get("text", "")),
            "rating": r.get("rating", 5),
            "sentiment": r.get("sentiment", "Neutral"),
            "sentiment_score": r.get("sentiment_score", r.get("score", 0.0)),
            "source": r.get("source", "Web Scraper")
        }
        formatted_reviews.append(doc)

    if db is not None:
        try:
            # Delete old reviews for this product before adding new
            db.reviews.delete_many({"product_id": str(product_id)})
            if formatted_reviews:
                db.reviews.insert_many(formatted_reviews)
                for r in formatted_reviews:
                    if "_id" in r:
                        r["_id"] = str(r["_id"])
            return formatted_reviews
        except PyMongoError as e:
            logger.error(f"Error saving reviews to MongoDB: {e}")

    # Fallback
    in_memory_db["reviews"] = [r for r in in_memory_db["reviews"] if r.get("product_id") != str(product_id)]
    for r in formatted_reviews:
        r["_id"] = str(uuid.uuid4())
        in_memory_db["reviews"].append(r)
    return formatted_reviews

def get_reviews_by_product_id(product_id):
    """Retrieve reviews for a given product."""
    db = get_db()
    if db is not None:
        try:
            reviews = list(db.reviews.find({"product_id": str(product_id)}))
            for r in reviews:
                r["_id"] = str(r["_id"])
            return reviews
        except PyMongoError as e:
            logger.error(f"Error reading reviews from MongoDB: {e}")

    return [r for r in in_memory_db["reviews"] if r.get("product_id") == str(product_id)]
