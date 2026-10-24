import re
from collections import Counter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize VADER analyzer
vader_analyzer = SentimentIntensityAnalyzer()

# Common English stop words
COMMON_STOP_WORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't",
    'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by',
    'can', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing',
    'don', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has',
    "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's",
    'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've",
    'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', 'let', "let's", 'me', 'more',
    'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or',
    'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she',
    "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's",
    'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they',
    "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under',
    'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't",
    'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's",
    'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll",
    "you're", "you've", 'your', 'yours', 'yourself', 'yourselves', 'this', 'product', 'item', 'one', 'bought'
}

def analyze_review(text):
    """
    Analyze a single review text using VADER.
    Returns dict with sentiment label and compound score.
    """
    if not text or not isinstance(text, str):
        return {
            "sentiment": "Neutral",
            "score": 0.0
        }
    
    scores = vader_analyzer.polarity_scores(text)
    compound = scores.get('compound', 0.0)

    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"

    return {
        "sentiment": label,
        "score": round(compound, 4)
    }

def analyze_reviews_batch(reviews):
    """
    Analyze a list of review dicts (each having 'review_text' or 'text').
    Appends 'sentiment' and 'sentiment_score' to each review item.
    """
    processed = []
    for r in reviews:
        text = r.get("review_text") or r.get("text", "")
        res = analyze_review(text)
        r["sentiment"] = res["sentiment"]
        r["sentiment_score"] = res["score"]
        if "review_text" not in r:
            r["review_text"] = text
        processed.append(r)
    return processed

def calculate_word_frequency(reviews, top_n=15):
    """
    Extract top N word frequencies from all review texts.
    """
    combined_text = " ".join([r.get("review_text", r.get("text", "")) for r in reviews])
    # Lowercase and keep letters/words
    words = re.findall(r'\b[a-zA-Z]{3,}\b', combined_text.lower())
    
    filtered_words = [word for word in words if word not in COMMON_STOP_WORDS]
    counter = Counter(filtered_words)
    
    return [{"word": word, "count": count} for word, count in counter.most_common(top_n)]

def compute_summary_analytics(reviews):
    """
    Compute summary metrics: totals, percentage, average rating, rating distribution.
    """
    total = len(reviews)
    if total == 0:
        return {
            "total_reviews": 0,
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "positive_pct": 0,
            "negative_pct": 0,
            "neutral_pct": 0,
            "average_rating": 0,
            "rating_distribution": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        }

    positive_count = sum(1 for r in reviews if r.get("sentiment") == "Positive")
    negative_count = sum(1 for r in reviews if r.get("sentiment") == "Negative")
    neutral_count = sum(1 for r in reviews if r.get("sentiment") == "Neutral")

    rating_dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    total_rating = 0
    valid_ratings_count = 0

    for r in reviews:
        r_val = r.get("rating", 5)
        try:
            r_val = int(round(float(r_val)))
            if 1 <= r_val <= 5:
                rating_dist[r_val] = rating_dist.get(r_val, 0) + 1
                total_rating += r_val
                valid_ratings_count += 1
        except (ValueError, TypeError):
            pass

    avg_rating = round(total_rating / valid_ratings_count, 1) if valid_ratings_count > 0 else 0.0

    return {
        "total_reviews": total,
        "positive": positive_count,
        "negative": negative_count,
        "neutral": neutral_count,
        "positive_pct": round((positive_count / total) * 100, 1),
        "negative_pct": round((negative_count / total) * 100, 1),
        "neutral_pct": round((neutral_count / total) * 100, 1),
        "average_rating": avg_rating,
        "rating_distribution": rating_dist
    }
