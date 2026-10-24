# Product Sentiment Analyzer and Review Dashboard

A full-stack web application for automated e-commerce product review scraping, NLP sentiment classification, and visual dashboard analytics. Built as a college major project.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Technologies Used](#technologies-used)
4. [System Architecture](#system-architecture)
5. [Folder Structure](#folder-structure)
6. [Prerequisites](#prerequisites)
7. [Installation & Local Setup](#installation--local-setup)
   - [Backend Setup](#1-backend-setup)
   - [MongoDB Setup](#2-mongodb-setup)
   - [Frontend Setup](#3-frontend-setup)
8. [Environment Variables](#environment-variables)
9. [Running the Application](#running-the-application)
10. [API Endpoints](#api-endpoints)
11. [Screenshots Placeholder](#screenshots-placeholder)
12. [Deployment Guide](#deployment-guide)
   - [Backend Deployment (Render)](#backend-deployment-render)
   - [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
13. [Future Enhancements](#future-enhancements)

---

## Project Overview
The **Product Sentiment Analyzer and Review Dashboard** allows users to input any e-commerce product URL, dynamically scrape user reviews using Selenium and BeautifulSoup, analyze the emotional polarity of each review using VADER NLP sentiment analysis, store structured data in MongoDB Atlas, and view visual analytics through an interactive React dashboard.

It features a **Demo Mode Fallback**, ensuring the system remains presentable and functional even if target websites update their dynamic HTML layout or employ anti-bot measures.

---

## Key Features
- **Dynamic Web Scraping**: Headless Chrome via Selenium to render dynamic e-commerce review pages.
- **VADER Sentiment Analysis**: Rule-based NLP classifier labeling reviews as *Positive*, *Negative*, or *Neutral* with compound confidence scores.
- **Interactive Visual Dashboard**: Built with React & Recharts featuring:
  - Sentiment Distribution Pie Chart
  - 1-to-5 Star Rating Breakdown Bar Chart
  - Keyword & Word Frequency Cloud
  - Searchable & Filterable Customer Review List
- **MongoDB Database**: Persistent storage for products, metadata, and analyzed reviews with PyMongo.
- **Fault-Tolerant Fallback**: Automatic offline demo dataset loader if live web scraping is restricted.

---

## Technologies Used

### Backend
- **Python 3.12**
- **Flask** & **Flask-CORS** (RESTful API Web Framework)
- **Selenium** & **BeautifulSoup4** (Dynamic Web Scraping)
- **VADER Sentiment** (`vaderSentiment` NLP package)
- **PyMongo** (MongoDB Driver)
- **pandas** & **NumPy** (Data processing)

### Frontend
- **React.js 19** (Vite framework)
- **Axios** (HTTP REST Client)
- **Recharts** (Visual analytics charts)
- **CSS3** (Responsive custom dashboard styling)

### Database
- **MongoDB Atlas** (Cloud NoSQL Database)

---

## System Architecture

```
React Frontend (Vite)
       │
       │ Axios REST API (JSON)
       ▼
Flask Backend (Python)
  ├── 1. Scraper Module (Selenium + BeautifulSoup)
  ├── 2. Sentiment Module (VADER NLP Analyzer)
  └── 3. Database Handler (PyMongo / In-Memory Fallback)
       │
       ▼
MongoDB Atlas (Cloud Storage)
  ├── Products Collection
  └── Reviews Collection
```

---

## Folder Structure

```
product-sentiment-analyzer/
│
├── backend/
│   ├── app.py                 # Main Flask server entrypoint
│   ├── config.py              # Environment configuration loader
│   ├── requirements.txt       # Python dependencies
│   ├── Procfile               # Render deployment start command
│   ├── .env                   # Environment variables (git-ignored)
│   ├── .env.example           # Example environment template
│   │
│   ├── database/
│   │   └── db.py              # PyMongo database layer with fallback
│   │
│   ├── scraper/
│   │   └── scraper.py         # Selenium web scraping engine
│   │
│   ├── sentiment/
│   │   └── analyzer.py        # VADER sentiment & word frequency analyzer
│   │
│   ├── routes/
│   │   ├── products.py        # Product API routes
│   │   └── reviews.py         # Scraping & review API routes
│   │
│   └── data/
│       └── demo_reviews.json  # Pre-compiled sample dataset for Demo Mode
│
├── frontend/
│   ├── package.json           # Node dependencies and scripts
│   ├── index.html             # HTML entry file
│   ├── vite.config.js         # Vite configuration with API proxy
│   ├── vercel.json            # Vercel deployment rewrite rules
│   │
│   └── src/
│       ├── main.jsx           # React app renderer
│       ├── App.jsx            # Main dashboard container
│       ├── api.js             # Axios API client
│       ├── index.css          # Dashboard styling
│       │
│       └── components/
│           ├── Navbar.jsx          # Header navigation bar
│           ├── SearchBar.jsx       # URL search & demo trigger
│           ├── ProductCard.jsx     # Product summary header
│           ├── SummaryCards.jsx    # Metric counter cards
│           ├── SentimentChart.jsx  # Recharts Pie chart
│           ├── RatingChart.jsx     # Recharts Bar chart
│           ├── WordFrequency.jsx   # Top keyword cloud
│           └── ReviewList.jsx      # Filterable review list
│
├── README.md
├── PROJECT_REPORT.md
└── .gitignore
```

---

## Prerequisites
- **Python 3.10+**
- **Node.js 18+** & **npm**
- **Google Chrome Browser** (required for Selenium headless browser scraping)
- **MongoDB Atlas Connection String** (optional; fallback in-memory database will run if not provided)

---

## Installation & Local Setup

### 1. Backend Setup
```bash
# Navigate to backend folder
cd backend

# Create virtual environment (optional)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. MongoDB Setup
1. Create a free MongoDB Atlas cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Create a database user and copy your connection string (`mongodb+srv://...`).
3. Copy `.env.example` to `.env` inside `backend/` directory:
   ```bash
   cp .env.example .env
   ```
4. Replace `MONGO_URI` with your connection string.

### 3. Frontend Setup
```bash
# Navigate to frontend folder
cd ../frontend

# Install node dependencies
npm install
```

---

## Environment Variables

### Backend (`backend/.env`)
```env
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/product_sentiment?retryWrites=true&w=majority
PORT=5000
FLASK_ENV=development
```

### Frontend (`frontend/.env`)
```env
VITE_API_URL=http://localhost:5000
```

---

## Running the Application

### Step 1: Start Backend Server
```bash
cd backend
python app.py
```
*Backend runs on `http://localhost:5000`*

### Step 2: Start Frontend Development Server
```bash
cd frontend
npm run dev
```
*Frontend opens at `http://localhost:5173`*

---

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Health check endpoint |
| `GET` | `/api/products` | Get list of all saved products |
| `GET` | `/api/products/<product_id>` | Get details and metrics for one product |
| `GET` | `/api/reviews/<product_id>` | Get all reviews for a specific product |
| `POST` | `/api/scrape` | Scrape product URL, analyze sentiment, store results |
| `POST` | `/api/analyze` | Analyze sentiment of custom text input |

### Sample `POST /api/scrape` Request Body
```json
{
  "url": "https://www.amazon.com/dp/B08N5WRWNW"
}
```

---

## Screenshots Placeholder
*(Add screenshots of your running React dashboard here for viva presentation)*
- **Dashboard Header & Search Section**
- **Summary Metrics & Pie Chart**
- **Rating Bar Chart & Word Cloud**
- **Filtered Review List**

---

## Deployment Guide

### Backend Deployment (Render)
1. Push project code to GitHub.
2. Go to [Render Dashboard](https://render.com) and create a **Web Service**.
3. Connect your repository and select the `backend` directory.
4. Set Build Command: `pip install -r requirements.txt`
5. Set Start Command: `gunicorn app:app`
6. Add Environment Variable `MONGO_URI` in Render settings.

### Frontend Deployment (Vercel)
1. Go to [Vercel Dashboard](https://vercel.com) and import project repository.
2. Root Directory: `frontend`
3. Framework Preset: **Vite**
4. Set Environment Variable: `VITE_API_URL` = `<your-render-backend-url>`
5. Click **Deploy**.

---

## Future Enhancements
- Support multi-website scrapers (Amazon, eBay, Walmart, Flipkart).
- User authentication and saved search history.
- Aspect-based sentiment analysis (detecting sentiment for specific features like battery, screen, price).
- Automated email alerts on negative sentiment spikes.
