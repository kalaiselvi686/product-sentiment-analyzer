import json
import os
import re
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

logger = logging.getLogger(__name__)

def load_demo_data():
    """Load demo dataset from json file as a fallback."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    demo_file = os.path.join(base_dir, "data", "demo_reviews.json")
    try:
        with open(demo_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load demo file: {e}")
        return {
            "product": {
                "name": "Sample Demo Product",
                "url": "https://example.com/demo",
                "source": "Demo Mode",
                "rating": 4.0,
                "total_reviews": 5
            },
            "reviews": [
                {"text": "Great product! Works perfectly.", "rating": 5},
                {"text": "Decent quality for the price.", "rating": 4},
                {"text": "Average product, could be improved.", "rating": 3},
                {"text": "Poor quality, disappointed.", "rating": 2},
                {"text": "Terrible experience, broke on day one.", "rating": 1}
            ]
        }

def setup_chrome_driver():
    """Initialize a headless Selenium Chrome WebDriver."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        # First try direct Chrome driver instantiation
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        logger.warning(f"WebDriverManager failed: {e}. Trying default Chrome instantiation.")
        try:
            driver = webdriver.Chrome(options=options)
            return driver
        except Exception as e2:
            logger.error(f"Chrome Driver initialization failed: {e2}")
            return None

def scrape_product(url):
    """
    Main scraping function.
    Given a URL, launches Selenium, parses the DOM, extracts product info and reviews.
    If scraping fails or URL is 'demo', returns demo dataset with a flag indicating demo source.
    """
    if not url or not isinstance(url, str):
        return {"success": False, "error": "Invalid URL provided"}

    clean_url = url.strip().lower()
    if clean_url in ["demo", "http://demo", "https://demo"] or "example.com" in clean_url:
        demo_data = load_demo_data()
        return {
            "success": True,
            "is_demo": True,
            "product": demo_data["product"],
            "reviews": demo_data["reviews"]
        }

    driver = None
    try:
        driver = setup_chrome_driver()
        if not driver:
            logger.warning("Selenium unavailable, falling back to Demo Mode.")
            demo = load_demo_data()
            demo["is_demo"] = True
            demo["notice"] = "Live browser scraping unavailable in environment. Loaded demo dataset."
            return {"success": True, **demo}

        driver.get(url)
        # Wait up to 5 seconds for page load
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Extract title
        product_title = ""
        title_el = soup.find("h1") or soup.find("span", {"id": "productTitle"}) or soup.find("meta", {"property": "og:title"})
        if title_el:
            product_title = title_el.get_text(strip=True) if hasattr(title_el, "get_text") else title_el.get("content", "")
        
        if not product_title:
            product_title = soup.title.string.strip() if soup.title else "Scraped E-Commerce Product"

        # Generic review text extraction using common class names / tags
        reviews_data = []

        # Common selector patterns for e-commerce sites (Amazon, Flipkart, generic stores)
        review_containers = soup.find_all(class_=re.compile(r'review|comment|feedback|testimonial|rating-text', re.I))
        
        if not review_containers:
            # Fallback to paragraph inspection
            review_containers = soup.find_all(['p', 'div'], text=True)

        for container in review_containers:
            text = container.get_text(strip=True)
            if len(text) > 15 and text not in [r["text"] for r in reviews_data]:
                # Try finding rating in container or default to 4/5
                rating = 4
                rating_match = re.search(r'([1-5])\s*(?:out of 5|stars|star|\/5)', container.get_text(), re.I)
                if rating_match:
                    try:
                        rating = int(rating_match.group(1))
                    except ValueError:
                        rating = 4

                reviews_data.append({
                    "text": text,
                    "rating": rating
                })
                if len(reviews_data) >= 30:
                    break

        if not reviews_data:
            # If no reviews could be parsed, fallback gracefully to demo data with custom product name
            logger.warning("No review structures found on page. Returning demo dataset.")
            demo = load_demo_data()
            demo["product"]["name"] = product_title if product_title else demo["product"]["name"]
            demo["product"]["url"] = url
            return {
                "success": True,
                "is_demo": True,
                "notice": "Could not extract live reviews from dynamic structure. Loaded demo reviews for analysis.",
                "product": demo["product"],
                "reviews": demo["reviews"]
            }

        # Calculate average scraped rating
        avg_rating = round(sum(r["rating"] for r in reviews_data) / len(reviews_data), 1)

        product_info = {
            "name": product_title[:120],
            "url": url,
            "source": "Web Scraper",
            "rating": avg_rating,
            "total_reviews": len(reviews_data)
        }

        return {
            "success": True,
            "is_demo": False,
            "product": product_info,
            "reviews": reviews_data
        }

    except Exception as e:
        logger.error(f"Error scraping product URL '{url}': {e}")
        # Return fallback demo data on scraping exception
        demo = load_demo_data()
        return {
            "success": True,
            "is_demo": True,
            "notice": f"Live scraper error ({str(e)}). Displaying demo data.",
            "product": demo["product"],
            "reviews": demo["reviews"]
        }
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass
