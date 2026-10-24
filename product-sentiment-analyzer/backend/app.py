from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from routes.products import products_bp
from routes.reviews import reviews_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for frontend requests
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Register API blueprints
    app.register_blueprint(products_bp)
    app.register_blueprint(reviews_bp)

    @app.route('/', methods=['GET'])
    def health_check():
        return jsonify({
            "status": "online",
            "service": "Product Sentiment Analyzer API",
            "version": "1.0.0"
        }), 200

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "error": "Requested resource not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"success": False, "error": "Internal server error"}), 500

    return app

app = create_app()

if __name__ == '__main__':
    print(f"Starting Product Sentiment Analyzer Backend on port {Config.PORT}...")
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
