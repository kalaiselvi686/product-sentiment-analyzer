from flask import Blueprint, jsonify, request
from database.db import get_all_products, get_product_by_id, get_reviews_by_product_id
from sentiment.analyzer import compute_summary_analytics, calculate_word_frequency

products_bp = Blueprint('products', __name__)

@products_bp.route('/api/products', methods=['GET'])
def get_products():
    """Endpoint to list all analyzed products."""
    try:
        products = get_all_products()
        return jsonify({
            "success": True,
            "count": len(products),
            "products": products
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to retrieve products: {str(e)}"
        }), 500

@products_bp.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Endpoint to retrieve a specific product with its analytics summary."""
    try:
        product = get_product_by_id(product_id)
        if not product:
            return jsonify({
                "success": False,
                "error": "Product not found"
            }), 404

        reviews = get_reviews_by_product_id(product_id)
        summary = compute_summary_analytics(reviews)
        word_freq = calculate_word_frequency(reviews)

        return jsonify({
            "success": True,
            "product": product,
            "summary": summary,
            "word_frequency": word_freq,
            "total_reviews": len(reviews)
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to fetch product details: {str(e)}"
        }), 500
