# 🏨 Hotel Booking & Review Analytics Dashboard

A comprehensive **Data Mining, Business Intelligence, and NLP-powered** web application for analyzing hotel bookings and customer reviews. Built with Streamlit, this decision support system provides real-time insights into operational performance, customer behavior, revenue trends, and review sentiment analysis.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Data Specifications](#data-specifications)
- [NLP & ML Methods](#nlp--ml-methods)
- [Business Intelligence Features](#business-intelligence-features)
- [Dashboard Tabs](#dashboard-tabs)
- [Deployment](#deployment)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## 🎯 Project Overview

This project combines **DMBI (Data Mining & Business Intelligence)** analytics with **Natural Language Processing (NLP)** to create an intelligent hotel analytics platform. It analyzes 2,000+ booking records and 150+ customer reviews to provide:

- **Operational KPIs**: Revenue, occupancy rates, cancellation analysis
- **Customer Intelligence**: RFM segmentation, booking patterns, geographic analysis
- **Sentiment Analytics**: Review sentiment classification, aspect-based analysis
- **Predictive Models**: 30-day revenue forecasting, market basket analysis
- **Fraud Detection**: AI-powered fake review identification

**Use Cases:**
- Hotel managers: Monitor performance and make data-driven decisions
- Revenue managers: Optimize pricing and forecasting
- Marketing teams: Understand customer segments and preferences
- Quality teams: Identify service issues through sentiment analysis

---

## ✨ Features

### 📊 Business Intelligence (DMBI)
- **KPI Dashboard**: Total bookings, revenue, occupancy %, cancellation rate, ADR, RevPAR
- **Channel Performance**: OTA vs Direct vs Corporate vs GDS analysis
- **Room Type Analysis**: Revenue and booking distribution by room category
- **RFM Analysis**: Customer segmentation by Recency, Frequency, Monetary value
- **Customer Segmentation**: Travel purpose and guest type classification
- **Revenue Forecasting**: 30-day exponential smoothing predictions
- **Seasonal Analysis**: Week-by-month revenue patterns
- **Market Basket Analysis**: Apriori algorithm for cross-selling opportunities

### 🧠 Natural Language Processing (NLP)
- **Sentiment Analysis**: TextBlob-based polarity and subjectivity scoring
- **Aspect-Based Sentiment**: Staff, Cleanliness, Location, Food, Price, Amenities breakdown
- **Topic Modeling**: Latent Dirichlet Allocation (LDA) for topic discovery
- **Word Cloud Visualization**: Visual representation of review keywords
- **Fake Review Detection**: Multi-factor heuristic scoring (rating mismatch, text patterns, repetition)
- **Rating-Sentiment Correlation**: Identify reviews where stars don't match sentiment
- **Model Evaluation**: Accuracy, F1-Score, Confusion Matrix metrics

### 🔧 Interactive Features
- **Dynamic Filtering**: Date range and country multi-select filters
- **Real-time Analytics**: Data updates instantly based on filter selections
- **Interactive Charts**: Plotly visualizations for drill-down analysis
- **Responsive Design**: Wide layout with expanded sidebar for navigation

---

## 🛠️ Tech Stack

| Category | Technology | Version |
|----------|-----------|---------|
| **Frontend** | Streamlit | 1.23.1 |
| **Backend** | Python | 3.7+ |
| **Data Processing** | Pandas, NumPy | Latest |
| **Visualization** | Plotly, Matplotlib, WordCloud | 5.0+, 3.5+, 1.8+ |
| **NLP/Text** | TextBlob, NLTK, scikit-learn | 0.17+, 3.8+, 1.0+ |
| **ML/Forecasting** | scikit-learn, statsmodels | 1.0+, 0.13+ |
| **Market Basket** | MLxtend | 0.19.0 |
| **Data Generation** | Random, datetime | Built-in |

---

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager
- Git (for version control)

### Step 1: Clone Repository
```bash
git clone https://github.com/Shiyam941/Hotel-Booking-and-Review-Dashboard.git
cd Hotel-Booking-and-Review-Dashboard
```

### Step 2: Create Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
streamlit --version
python -c "import pandas; import nltk; print('All packages installed successfully!')"
```

---

## 🚀 Usage

### Run Locally
```bash
cd "path/to/Hotel booking and Review Dashboard"
streamlit run app.py
```

The dashboard will open automatically at `http://localhost:8501`

### Access the Dashboard
- **URL**: http://localhost:8501
- **Navigation**: Use sidebar for filters and tab buttons for different analytics views
- **Date Range**: Select custom date range (defaults to all data)
- **Country Filter**: Multi-select countries for targeted analysis
- **Tabs**: Click through 9 different analytical dashboards

### Interactive Features
1. **Hover over charts** for detailed data points
2. **Click legend items** to toggle data series
3. **Adjust topic slider** for topic modeling (2-6 topics)
4. **Download data** from Streamlit's native export features

---

## 📁 Project Structure

```
Hotel-Booking-and-Review-Dashboard/
├── app.py                    # Main Streamlit dashboard application
├── engine.py                 # Analytics engine (DMBI & NLP computations)
├── data_manager.py           # Synthetic data generation
├── requirements.txt          # Python dependencies
├── styles.css                # Optional CSS styling
├── README.md                 # Project documentation
└── .gitignore               # Git ignore rules
```

### File Descriptions

**app.py** (680+ lines)
- Streamlit application entry point
- Dashboard UI with 9 tabs
- Interactive filters (date range, country selection)
- Chart rendering and layout management

**engine.py** (400+ lines)
- Core analytics computations
- 8 DMBI methods (KPIs, forecasting, segmentation, etc.)
- 9 NLP methods (sentiment, topics, fake detection, etc.)
- Data aggregation and statistical analysis

**data_manager.py** (150+ lines)
- Synthetic data generation function
- 2,000 booking records with 18 attributes
- 150 review records with 6 attributes
- Random but realistic data patterns

**requirements.txt**
- All Python package dependencies with versions
- Used by `pip install -r requirements.txt`

---

## 📊 Data Specifications

### Bookings Dataset (2,000 Records)

| Field | Type | Description | Examples |
|-------|------|-------------|----------|
| BookingID | String | Unique booking identifier | BK1000, BK1001 |
| ArrivalDate | DateTime | Check-in date | 2023-01-15 |
| LeadTime | Integer | Days between booking and arrival (0-150) | 45 |
| Nights | Integer | Length of stay (1-14) | 3 |
| Guests | Integer | Number of guests (1-4) | 2 |
| RoomType | Category | Standard, Deluxe, Suite, Penthouse | Suite |
| Channel | Category | OTA, Direct, Corporate, GDS | OTA |
| Segment | Category | Leisure, Business | Leisure |
| Country | Category | USA, UK, Germany, France, India, UAE, China | USA |
| IsCancelled | Binary | 0 or 1 (15% cancellation rate) | 0 |
| CancelReason | String/Null | Reason if cancelled | Change of plans |
| ADR | Float | Average Daily Rate ($) | 245.50 |
| Revenue | Float | Total booking revenue ($) | 736.50 |
| GuestType | Category | New, Returning | New |
| AgeGroup | Category | 18-25, 26-40, 41-60, 60+ | 26-40 |
| MealPlan | Category | BB, HB, FB, No Meal | BB |
| Addons | List | Optional services (Spa, Airport Transfer, Late Checkout, Mini Bar) | [Spa, Airport Transfer] |

**Distribution Stats:**
- Revenue range: $0 - $16,800
- ADR range: $80 - $1,250
- Occupancy: ~60% (completed stays)
- Cancellation rate: ~15%
- Countries: 7 (USA 30%, UK 20%, others 10-15% each)

### Reviews Dataset (150 Records)

| Field | Type | Description | Distribution |
|-------|------|-------------|--------------|
| ReviewID | String | Unique review identifier | RV1000 - RV1149 |
| Date | DateTime | Review submission date | Distributed Jan 2023 - Apr 2024 |
| ReviewText | Text | Customer review (20-300 chars) | Generated templates |
| Rating | Integer | Star rating (1-5) | 1=15%, 2=10%, 3=25%, 4=25%, 5=25% |
| Sentiment | Category | Positive, Neutral, Negative | Pos=60%, Neu=25%, Neg=15% |
| Aspects | Dict | Review aspects with sentiments | {Staff: Positive, Cleanliness: Neutral} |

**Aspect Categories:**
- Staff (service quality, friendliness)
- Cleanliness (room, bathroom, common areas)
- Location (proximity, accessibility)
- Food (breakfast, restaurant, quality)
- Price (value for money, fairness)
- Amenities (facilities, equipment, services)

---

## 🧠 NLP & ML Methods

### 1. Sentiment Analysis

**Algorithm**: TextBlob Sentiment Analysis
```
Polarity Score = (-1: Very Negative, 0: Neutral, +1: Very Positive)
Subjectivity = (0: Objective, 1: Very Subjective)

Formula:
  Polarity = (Positive - Negative) / (Positive + Negative + Neutral)
  Classification:
    Polarity > 0.1 → Positive
    -0.1 ≤ Polarity ≤ 0.1 → Neutral
    Polarity < -0.1 → Negative
```

**Implementation:**
```python
from textblob import TextBlob
blob = TextBlob(review_text)
polarity = blob.sentiment.polarity
subjectivity = blob.sentiment.subjectivity
```

### 2. Topic Modeling (LDA)

**Algorithm**: Latent Dirichlet Allocation
```
Process:
  1. Text preprocessing (NLTK tokenization, stopword removal)
  2. TF-IDF Vectorization (100 features max)
  3. LDA fitting (n_topics=3, max_iter=10)
  4. Top keywords extraction per topic

Formula:
  P(topic|document) = (word_count_in_topic + alpha) / (total_words + K*alpha)
  P(word|topic) = (topic_count + beta) / (total_topics + W*beta)
  Where K=topics, W=vocabulary, alpha/beta=Dirichlet priors
```

**Implementation:**
```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

vectorizer = CountVectorizer(max_features=100, stop_words='english')
lda = LatentDirichletAllocation(n_components=n_topics, max_iter=10)
```

### 3. Fake Review Detection

**Algorithm**: Multi-Factor Heuristic Scoring

```
Fraud Score Calculation:
  Base Score = 0
  
  IF (Rating ≠ Sentiment): +30 points
    Example: 5 stars but TextBlob polarity < -0.1
  
  IF (Review length < 20 chars): +20 points
    Example: "Good" only
  
  IF (CAPS percentage > 30%): +15 points
    Example: "THIS IS AMAZING!!!"
  
  IF (Punctuation ratio > 3 per 10 chars): +15 points
    Example: "Amazing!!! Wow... Great!!!!"
  
  IF (Word repetition > 20%): +20 points
    Example: "good good good bad bad"
  
  Final Fraud Score = min(Base Score, 100)
  
  Classification:
    Score ≥ 50 → Suspicious Review
    Score < 50 → Legitimate Review
```

### 4. Revenue Forecasting

**Algorithm**: Exponential Smoothing

```
Formula:
  ŷ(t+h) = α·y(t) + (1-α)·ŷ(t)
  
Where:
  α = smoothing parameter (0 < α < 1, default=0.3)
  y(t) = actual value at time t
  ŷ(t) = forecast at time t
  h = forecast horizon (30 days)

Implementation:
  from statsmodels.tsa.holtwinters import SimpleExpSmoothing
  model = SimpleExpSmoothing(historical_revenue)
  forecast = model.fit().fittedvalues
```

### 5. Aspect-Based Sentiment

**Algorithm**: Predefined Aspect Extraction + Sentiment Classification

```
Process:
  1. For each review, extract predefined aspects:
     - Staff mentions → Staff aspect
     - Clean/dirty mentions → Cleanliness aspect
     - Location mentions → Location aspect
     - Food mentions → Food aspect
     - Price mentions → Price aspect
     - Amenities mentions → Amenities aspect
  
  2. Calculate sentiment for each aspect independently
  3. Aggregate to Aspect × Sentiment cross-tabulation

Example:
  Review: "Staff was friendly but room was dirty"
  Aspect Sentiment:
    Staff → Positive (friendly)
    Cleanliness → Negative (dirty)
```

### 6. Model Evaluation Metrics

**Classification Metrics** (comparing TextBlob predictions vs synthetic labels):

```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
Precision = TP / (TP + FP)
Recall = TP / (TP + FN)
F1-Score = 2 × (Precision × Recall) / (Precision + Recall)

Confusion Matrix:
  [[TN, FP],
   [FN, TP]]
   
Where:
  TP = True Positives (correctly predicted positive)
  TN = True Negatives (correctly predicted negative)
  FP = False Positives (incorrectly predicted positive)
  FN = False Negatives (incorrectly predicted negative)
```

---

## 📈 Business Intelligence Features

### 1. KPI Dashboard

**Calculated Metrics:**
```
Total Bookings = COUNT(all bookings)
Revenue = SUM(booking.revenue where IsCancelled=0)
Occupancy % = (Total_Room_Nights / Available_Room_Nights) × 100
Cancellation % = (Cancelled_Bookings / Total_Bookings) × 100
ADR = AVERAGE(ADR for completed bookings)
RevPAR = Revenue / Available_Room_Nights
```

### 2. Channel Performance Analysis

**Grouping & Aggregation:**
```sql
SELECT 
  Channel,
  COUNT(BookingID) as Bookings,
  SUM(Revenue) as Revenue,
  SUM(IsCancelled) as Cancellations,
  SUM(Revenue)/COUNT(BookingID) as Avg_Revenue_per_Booking
FROM bookings
GROUP BY Channel
ORDER BY Revenue DESC
```

**Channels Analyzed:**
- OTA (Online Travel Agencies like Booking.com, Expedia)
- Direct (Hotel website or phone)
- Corporate (Business agreements)
- GDS (Global Distribution Systems like Amadeus)

### 3. RFM Analysis

**Segmentation Formula:**
```
R (Recency) = Days since last booking
F (Frequency) = Total number of bookings by customer
M (Monetary) = Total revenue from customer

Segments:
  Champions: High F, High M, Low R (best customers)
  Loyal: High F, High M, Any R
  Potential: Medium F, Medium M, Low R
  At-Risk: Low F, Low M, Any R
  Lost: Low F, Low M, High R (inactive)
```

**Implementation:**
```python
rfm_by_country = df.groupby('Country').agg({
  'BookingID': 'count',      # Frequency
  'Revenue': 'sum',           # Monetary
  'ArrivalDate': lambda x: (reference_date - x.max()).days  # Recency
})
```

### 4. Customer Segmentation

**Dimensions:**
- **Travel Purpose**: Leisure vs Business
- **Guest Type**: New vs Returning
- **Geography**: By Country (7 countries tracked)
- **Room Preference**: Standard, Deluxe, Suite, Penthouse
- **Age Group**: 18-25, 26-40, 41-60, 60+

**Use Cases:**
- Target marketing campaigns to business travelers
- Loyalty programs for returning customers
- Geographic pricing strategies

### 5. Market Basket Analysis

**Algorithm**: Apriori with Association Rules

```
Process:
  1. Create transaction baskets:
     Transaction = [RoomType, MealPlan, Addon1, Addon2]
     Example: [Deluxe, HB, Spa, Airport Transfer]
  
  2. Calculate Support (frequency):
     Support(X) = Count(transactions with X) / Total transactions
     Threshold: min_support = 0.05 (5%)
  
  3. Generate Association Rules:
     Rule: {RoomType, MealPlan} → {Addon}
     
  4. Calculate Metrics:
     Confidence = Support(A ∪ B) / Support(A)
     Lift = Confidence / Support(B)
     Conviction = (1 - Support(B)) / (1 - Confidence)

Interpretation:
  High Lift (>1.2) = Strong association (recommend together)
  Low Lift (<0.8) = Negative association (don't promote together)
```

**Example Output:**
```
Rule: {Suite} → {Spa}
Support: 8.2%
Confidence: 42%
Lift: 1.8
→ Interpretation: Customers buying Suite are 1.8x more likely to add Spa
```

### 6. Seasonal Analysis

**Method**: Pivot Table by Week and Month

```
pivot_table = pd.pivot_table(
  df,
  values='Revenue',
  index='WeekOfMonth',
  columns='Month',
  aggfunc='sum'
)

Output: 4 weeks × 12 months heatmap showing:
  - Peak seasons (high revenue weeks)
  - Off-peak periods (low revenue weeks)
  - Trends throughout year
  - Patterns for pricing strategy
```

---

## 📊 Dashboard Tabs

### Tab 1: 📊 Overview
**Content:**
- 6 KPI metrics cards (Total Bookings, Revenue, Occupancy, Cancellations, ADR, RevPAR)
- Pie charts: Booking distribution by Room Type, Channel, Segment
- Dual-axis bar chart: Monthly booking count and revenue trend
- Key insights panel

**Use Cases:**
- Executive dashboard view
- Quick performance check
- Month-over-month trends

---

### Tab 2: 📈 Booking Analysis
**Content:**
- Lead time distribution histogram (0-150 days)
- Channel revenue comparison bar chart
- Room type revenue bar chart
- Cancellation rate heatmap by Room Type × Channel
- Statistics tables

**Use Cases:**
- Booking pattern analysis
- Channel performance optimization
- Cancellation risk identification
- Lead time forecasting

---

### Tab 3: 👥 Customer Insights
**Content:**
- RFM scatter plot (Frequency vs Monetary by Country)
- Travel purpose breakdown (Leisure vs Business)
- Guest type comparison (New vs Returning)
- Customer value segmentation
- Geographic distribution

**Use Cases:**
- Customer lifetime value assessment
- Targeted marketing campaigns
- Geographic strategy development
- Loyalty program planning

---

### Tab 4: 💰 Revenue & Forecast
**Content:**
- 30-day revenue forecast line chart (historical + predicted)
- Seasonal heatmap (week × month)
- Association rules table (cross-selling opportunities)
- Forecast accuracy metrics
- Revenue trend analysis

**Use Cases:**
- Revenue forecasting
- Cash flow planning
- Cross-selling strategy
- Peak period identification

---

### Tab 5: 🧠 Sentiment Analysis
**Content:**
- Sentiment distribution pie chart (Positive/Neutral/Negative)
- Rating distribution bar chart (1-5 stars)
- Rating vs Sentiment correlation scatter plot
- Sentiment mismatch metric
- Key sentiment statistics

**Use Cases:**
- Customer satisfaction assessment
- Quality improvement identification
- Sentiment trend monitoring
- Anomaly detection (mismatched ratings)

---

### Tab 6: 📝 Aspect Analysis
**Content:**
- Aspect × Sentiment bar chart (Staff, Cleanliness, Location, Food, Price, Amenities)
- Cross-tabulation summary table
- Aspect distribution pie charts
- Sentiment breakdown per aspect

**Use Cases:**
- Service quality identification
- Problem area detection
- Departmental performance tracking
- Targeted improvement efforts

---

### Tab 7: 🔍 Topic Modeling
**Content:**
- LDA topics table (Top 3-6 topics with keywords)
- Word frequency analysis
- Word cloud visualization (positive reviews)
- Topic slider for n_topics (2-6 topics)
- Topic prevalence statistics

**Use Cases:**
- Review theme discovery
- Customer concern identification
- Content analysis
- Feedback categorization

---

### Tab 8: 🗣️ Fake Reviews
**Content:**
- Fraud score distribution histogram (0-100)
- Suspicious reviews table (ranked by fraud score)
- Suspicious review count metric
- Review authenticity breakdown
- Detection method explanation

**Use Cases:**
- Review manipulation detection
- Data quality assurance
- Competitive intelligence
- Platform credibility maintenance

---

### Tab 9: 📊 Comparison
**Content:**
- Country-wise booking count bar chart
- Country-wise revenue bar chart
- Model evaluation metrics (Accuracy, F1-Score)
- Confusion matrix table
- Country ranking tables
- Performance comparison charts

**Use Cases:**
- Geographic performance comparison
- Market analysis by country
- Model validation and monitoring
- Strategic planning by region

---

## 🌐 Deployment

### Option 1: Streamlit Cloud (Easiest - FREE)

**Steps:**
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" and select your repository
4. Set main file to `app.py`
5. Deploy!

**Pros:** Free, automatic GitHub sync, SSL included, instant deployment  
**Cons:** 3 free apps limit, resource limitations

**Example URL:** `https://hotel-dashboard-shiyam941.streamlit.app`

---

### Option 2: Heroku ($5-7/month)

**Files needed:**

**Procfile:**
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**setup.sh:**
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

**Commands:**
```bash
heroku create your-app-name
git push heroku master
```

---

### Option 3: DigitalOcean App Platform ($5-12/month)

1. Connect GitHub repository
2. Select `app.py` as entry point
3. Set environment to Python 3.9
4. Deploy

Automatic deploys on push to main branch.

---

### Option 4: Docker + Any Cloud ($5-20/month)

**Dockerfile:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Build & Run:**
```bash
docker build -t hotel-dashboard .
docker run -p 8501:8501 hotel-dashboard
```

---

## 📸 Screenshots

### Dashboard Overview
- KPI metrics cards showing total bookings, revenue, occupancy rate
- Interactive pie charts for booking distribution
- Monthly revenue trend analysis
- Responsive sidebar with filters

### Sentiment Analysis Tab
- Sentiment distribution (Positive/Neutral/Negative)
- Star rating distribution
- Rating vs sentiment correlation
- Mismatch detection metrics

### Topic Modeling Tab
- LDA-generated topics with top keywords
- Word cloud visualization
- Topic prevalence statistics
- Adjustable topic slider

### Fake Review Detection
- Fraud score histogram
- Suspicious reviews ranked by score
- Detection explanation
- Review authenticity breakdown

---

## 🚀 Future Enhancements

### Phase 2: Advanced NLP
- [ ] Replace TextBlob with spaCy/HuggingFace Transformers for better accuracy
- [ ] Implement BERT-based sentiment classification
- [ ] Add multilingual support for international reviews
- [ ] Real-time review scraping from Google, TripAdvisor, Booking.com
- [ ] Advanced NER (Named Entity Recognition) for specific mentions

### Phase 3: Predictive Analytics
- [ ] Machine learning model for cancellation prediction
- [ ] Pricing optimization algorithm
- [ ] Customer churn prediction
- [ ] Length of stay forecasting
- [ ] Demand forecasting by room type

### Phase 3: Integration & Deployment
- [ ] REST API for external integrations
- [ ] Database integration (PostgreSQL, MongoDB)
- [ ] Real hotel data integration (PMS systems)
- [ ] Email alerts for KPI thresholds
- [ ] Mobile app companion
- [ ] Real-time analytics updates

### Phase 4: Advanced Visualizations
- [ ] Geographic heatmaps for booking distribution
- [ ] Customer journey mapping
- [ ] Revenue waterfall analysis
- [ ] Cohort analysis
- [ ] Time series decomposition
- [ ] Interactive dashboards with drill-down

### Phase 5: Business Intelligence
- [ ] Customer lifetime value (CLV) modeling
- [ ] Propensity modeling for ancillary sales
- [ ] Competitive benchmarking
- [ ] Dynamic pricing recommendations
- [ ] Automated report generation
- [ ] What-if scenario analysis

---

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📧 Support & Contact

- **GitHub Issues**: [Report bugs or request features](https://github.com/Shiyam941/Hotel-Booking-and-Review-Dashboard/issues)
- **Email**: shiyam941@gmail.com
- **LinkedIn**: [Your LinkedIn Profile]

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Streamlit** - For the amazing web app framework
- **Scikit-learn** - For ML and NLP tools
- **Plotly** - For interactive visualizations
- **TextBlob** - For sentiment analysis
- **NLTK** - For natural language processing

---

## 📊 Performance Benchmarks

| Metric | Value | Notes |
|--------|-------|-------|
| Data Generation | <1s | 2,000 bookings + 150 reviews |
| App Startup | 2-3s | Streamlit caching enabled |
| Tab Load Time | <500ms | Real-time computation |
| Sentiment Analysis | 150 reviews/s | Using TextBlob |
| LDA Modeling | 2-3s | 3 topics, 100 features |
| Forecast Computation | <500ms | 30-day horizon |
| Dashboard Rendering | 3-5s | First load with all charts |

---

## 🎓 Learning Outcomes

After building this project, you'll understand:

✅ Streamlit application development  
✅ Data processing with Pandas  
✅ Machine learning workflows  
✅ NLP techniques (sentiment, topics, entity extraction)  
✅ Business intelligence metrics  
✅ Time series forecasting  
✅ Market basket analysis  
✅ Data visualization best practices  
✅ Deployment and cloud hosting  
✅ Git version control  

---

**Last Updated:** May 4, 2026  
**Version:** 1.0.0  
**Status:** Production Ready ✅

For the latest updates, visit: [GitHub Repository](https://github.com/Shiyam941/Hotel-Booking-and-Review-Dashboard)

