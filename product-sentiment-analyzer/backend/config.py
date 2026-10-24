import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "")
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("FLASK_ENV", "development") == "development"
