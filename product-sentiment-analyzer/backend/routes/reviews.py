from flask import Blueprint, jsonify, request
from database.db import save_product, save_reviews, get_reviews_by_product_id, get_product_by_id
from scraper.scraper import scrape_product
from sentiment.analyzer import analyze_review, analyze_reviews_batch, compute_summary_analytics, calculate_word_frequency

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/api/reviews/<product_id>', methods=['GET'])
def get_product_reviews(product_id):
    """Retrieve all stored reviews for a given product."""
    try:
        reviews = get_reviews_by_product_id(product_id)
        return jsonify({
            "success": True,
            "product_id": product_id,
            "count": len(reviews),
            "reviews": reviews
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to fetch reviews: {str(e)}"
        }), 500

@reviews_bp.route('/api/scrape', methods=['POST'])
def scrape_and_analyze():
    """
    Main API endpoint:
    Receives product URL, scrapes reviews, performs VADER sentiment analysis,
    stores results in DB, and returns complete dashboard visualization payload.
    """
    data = request.get_json(silent=True) or {}
    url = data.get("url")

    if not url or not isinstance(url, str) or not url.strip():
        return jsonify({
            "success": False,
            "error": "Missing or invalid product URL. Please provide a valid URL."
        }), 400

    try:
        # Step 1: Run Web Scraper
        scraped_res = scrape_product(url.strip())

        if not scraped_res.get("success"):
            return jsonify({
                "success": False,
                "error": scraped_res.get("error", "Scraping failed")
            }), 400

        product_info = scraped_res["product"]
        raw_reviews = scraped_res["reviews"]
        is_demo = scraped_res.get("is_demo", False)
        notice = scraped_res.get("notice", None)

        # Step 2: Analyze Sentiments using VADER
        analyzed_reviews = analyze_reviews_batch(raw_reviews)

        # Step 3: Calculate Metrics & Summary
        summary = compute_summary_analytics(analyzed_reviews)
        word_freq = calculate_word_frequency(analyzed_reviews)

        # Update product info with calculated average rating and count
        product_info["total_reviews"] = summary["total_reviews"]
        if summary["average_rating"] > 0:
            product_info["rating"] = summary["average_rating"]

        # Step 4: Save to Database (MongoDB / Fallback)
        product_id = save_product(product_info)
        saved_reviews = save_reviews(product_id, analyzed_reviews)

        product_info["_id"] = product_id

        # Step 5: Return dashboard response
        return jsonify({
            "success": True,
            "is_demo": is_demo,
            "notice": notice,
            "product": product_info,
            "summary": summary,
            "word_frequency": word_freq,
            "reviews": saved_reviews
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"An unexpected error occurred during analysis: {str(e)}"
        }), 500

@reviews_bp.route('/api/analyze', methods=['POST'])
def analyze_single():
    """Endpoint to analyze a single piece of review text directly."""
    data = request.get_json(silent=True) or {}
    text = data.get("text")

    if not text or not isinstance(text, str):
        return jsonify({
            "success": False,
            "error": "Missing 'text' parameter in request body."
        }), 400

    result = analyze_review(text)
    return jsonify({
        "success": True,
        "input_text": text,
        "sentiment": result["sentiment"],
        "score": result["score"]
    }), 200
