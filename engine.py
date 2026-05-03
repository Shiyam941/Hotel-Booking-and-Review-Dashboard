import pandas as pd
import numpy as np
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
import warnings

warnings.filterwarnings('ignore')

class AnalyticsEngine:
    def __init__(self, df_bookings, df_reviews):
        self.df_bookings = df_bookings.copy()
        self.df_reviews = df_reviews.copy()
        self.df_bookings['ArrivalDate'] = pd.to_datetime(self.df_bookings['ArrivalDate'])
        self.df_reviews['Date'] = pd.to_datetime(self.df_reviews['Date'])

    # ============ DMBI FEATURES ============

    def get_kpis(self):
        """Enhanced KPI calculations"""
        total_bookings = len(self.df_bookings)
        revenue = self.df_bookings['Revenue'].sum()
        cancelled = self.df_bookings['IsCancelled'].sum()
        cancel_rate = (cancelled / total_bookings * 100) if total_bookings > 0 else 0
        completed = total_bookings - cancelled
        
        adr = self.df_bookings[self.df_bookings['IsCancelled'] == 0]['ADR'].mean()
        total_room_nights = completed * self.df_bookings[self.df_bookings['IsCancelled'] == 0]['Nights'].mean()
        occupancy = (total_room_nights / (480 * 100) * 100) if completed > 0 else 0
        revpar = revenue / (480 * 100)
        
        return {
            'Total Bookings': total_bookings,
            'Revenue': f"${revenue:,.0f}",
            'Occupancy': f"{occupancy:.1f}%",
            'Cancellations': f"{cancel_rate:.1f}%",
            'ADR': f"${adr:.0f}",
            'RevPAR': f"${revpar:.0f}"
        }

    def get_channel_performance(self):
        """Channel analysis"""
        channel_data = self.df_bookings.groupby('Channel').agg({
            'BookingID': 'count',
            'Revenue': 'sum',
            'IsCancelled': 'sum'
        }).reset_index()
        channel_data.columns = ['Channel', 'Bookings', 'Revenue', 'Cancellations']
        return channel_data

    def get_room_type_analysis(self):
        """Room type performance"""
        room_data = self.df_bookings.groupby('RoomType').agg({
            'BookingID': 'count',
            'Revenue': 'sum'
        }).reset_index()
        room_data.columns = ['RoomType', 'Bookings', 'Revenue']
        return room_data

    def rfm_analysis(self):
        """RFM Analysis by Country"""
        reference_date = self.df_bookings['ArrivalDate'].max()
        rfm = self.df_bookings.groupby('Country').agg({
            'BookingID': 'count',
            'Revenue': 'sum',
            'ArrivalDate': lambda x: (reference_date - x.max()).days
        }).reset_index()
        rfm.columns = ['Country', 'Frequency', 'Monetary', 'Recency']
        rfm = rfm.sort_values('Monetary', ascending=False)
        return rfm

    def customer_segmentation(self):
        """Customer segments"""
        segments = self.df_bookings.groupby(['Segment', 'GuestType']).agg({
            'BookingID': 'count',
            'Revenue': 'sum'
        }).reset_index()
        segments.columns = ['TravelPurpose', 'GuestType', 'Bookings', 'Revenue']
        return segments

    def forecast_revenue(self, periods=30):
        """Revenue forecasting using exponential smoothing"""
        daily_rev = self.df_bookings.groupby('ArrivalDate')['Revenue'].sum()
        daily_rev = daily_rev.asfreq('D', fill_value=0)
        
        if len(daily_rev) > 5:
            model = SimpleExpSmoothing(daily_rev).fit(smoothing_level=0.2, optimized=False)
            forecast = model.forecast(periods)
            return daily_rev, forecast
        return daily_rev, pd.Series([daily_rev.mean()] * periods)

    def seasonal_analysis(self):
        """Seasonal heatmap data"""
        df_copy = self.df_bookings.copy()
        df_copy['Month'] = df_copy['ArrivalDate'].dt.month
        df_copy['Week'] = df_copy['ArrivalDate'].dt.isocalendar().week
        seasonal = df_copy.pivot_table(values='Revenue', index='Week', columns='Month', aggfunc='sum', fill_value=0)
        return seasonal

    def association_rules_mining(self):
        """Market basket analysis"""
        transactions = []
        for _, row in self.df_bookings.iterrows():
            transaction = [row['RoomType'], row['MealPlan']]
            if row['Addons'] and isinstance(row['Addons'], list):
                transaction.extend(row['Addons'][:2])
            transactions.append(transaction)
        
        te = TransactionEncoder()
        te_ary = te.fit(transactions).transform(transactions)
        df_encoded = pd.DataFrame(te_ary, columns=te.columns_)
        
        frequent_itemsets = apriori(df_encoded, min_support=0.05, use_colnames=True)
        if len(frequent_itemsets) > 1:
            rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
            if len(rules) > 0:
                rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
                rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
                return rules.sort_values('lift', ascending=False).head(10)
        return pd.DataFrame()

    # ============ NLP FEATURES ============

    def analyze_sentiment(self):
        """Calculate sentiment using TextBlob"""
        self.df_reviews['Polarity'] = self.df_reviews['ReviewText'].apply(
            lambda x: TextBlob(str(x)).sentiment.polarity)
        self.df_reviews['Subjectivity'] = self.df_reviews['ReviewText'].apply(
            lambda x: TextBlob(str(x)).sentiment.subjectivity)
        return self.df_reviews

    def get_sentiment_distribution(self):
        """Sentiment distribution statistics"""
        sentiment_counts = self.df_reviews['Sentiment'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']
        return sentiment_counts

    def get_aspect_sentiment(self):
        """Aspect-based sentiment analysis"""
        aspect_data = []
        for _, row in self.df_reviews.iterrows():
            if isinstance(row['Aspects'], dict):
                for aspect, sentiment in row['Aspects'].items():
                    aspect_data.append({'Aspect': aspect, 'Sentiment': sentiment})
        return pd.DataFrame(aspect_data)

    def get_aspect_summary(self):
        """Aspect sentiment summary"""
        aspect_df = self.get_aspect_sentiment()
        if len(aspect_df) > 0:
            summary = aspect_df.groupby('Aspect')['Sentiment'].value_counts().unstack(fill_value=0)
            return summary
        return pd.DataFrame()

    def get_keywords_tfidf(self, n_keywords=10):
        """TF-IDF keyword extraction"""
        vectorizer = TfidfVectorizer(max_features=n_keywords, stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(self.df_reviews['ReviewText'].fillna(''))
        keywords = vectorizer.get_feature_names_out()
        return keywords[:n_keywords]

    def topic_modeling(self, n_topics=3):
        """LDA Topic Modeling"""
        vectorizer = CountVectorizer(stop_words='english', max_features=100)
        data_vectorized = vectorizer.fit_transform(self.df_reviews['ReviewText'].fillna(''))
        
        lda = LatentDirichletAllocation(n_components=n_topics, random_state=42, max_iter=10)
        lda.fit(data_vectorized)
        
        words = vectorizer.get_feature_names_out()
        topics = []
        for topic_idx, topic in enumerate(lda.components_):
            top_words = [words[i] for i in topic.argsort()[-5:]]
            topics.append({'Topic': f'Topic {topic_idx+1}', 'Keywords': ', '.join(top_words)})
        return pd.DataFrame(topics)

    def get_rating_sentiment_correlation(self):
        """Compare star ratings with review sentiment"""
        self.analyze_sentiment()
        
        rating_sentiment = self.df_reviews.groupby('Rating').agg({
            'Polarity': 'mean'
        }).reset_index()
        rating_sentiment.columns = ['Rating', 'AvgPolarity']
        
        # Calculate mismatch
        mismatch = self.df_reviews[
            ((self.df_reviews['Rating'] >= 4) & (self.df_reviews['Polarity'] < 0)) |
            ((self.df_reviews['Rating'] <= 2) & (self.df_reviews['Polarity'] > 0))
        ]
        mismatch_rate = (len(mismatch) / len(self.df_reviews) * 100) if len(self.df_reviews) > 0 else 0
        
        return rating_sentiment, mismatch_rate

    def get_sentiment_trend(self):
        """Sentiment trend over time"""
        df_copy = self.df_reviews.copy()
        df_copy['Month'] = df_copy['Date'].dt.to_period('M')
        trend = df_copy.groupby(['Month', 'Sentiment']).size().unstack(fill_value=0)
        return trend

    def detect_fake_reviews(self):
        """Fake review detection using heuristics"""
        fake_indicators = []
        
        for idx, row in self.df_reviews.iterrows():
            score = 0
            text = str(row['ReviewText']).lower()
            
            sentiment_score = TextBlob(text).sentiment.polarity
            if (row['Rating'] >= 4 and sentiment_score < -0.2) or (row['Rating'] <= 2 and sentiment_score > 0.5):
                score += 30
            
            if len(text.split()) < 5:
                score += 20
            
            if len([c for c in text if c.isupper()]) > len(text) * 0.3:
                score += 15
            
            if text.count('!') > 3 or text.count('?') > 2:
                score += 15
            
            words = text.split()
            if len(words) > 0 and max([words.count(w) for w in set(words)]) > len(words) * 0.4:
                score += 20
            
            fake_indicators.append({
                'ReviewID': row['ReviewID'],
                'Rating': row['Rating'],
                'Text': text[:50],
                'FakeScore': min(score, 100),
                'IsFake': score >= 50
            })
        
        return pd.DataFrame(fake_indicators)

    def get_wordcloud_data(self, sentiment='Positive'):
        """Prepare word cloud data"""
        sentiment_reviews = self.df_reviews[self.df_reviews['Sentiment'] == sentiment]['ReviewText'].str.cat()
        return sentiment_reviews if isinstance(sentiment_reviews, str) else ''

    def model_evaluation_metrics(self):
        """Calculate NLP model evaluation metrics"""
        self.analyze_sentiment()
        
        y_true = self.df_reviews['Sentiment'].values
        y_pred = []
        
        for _, row in self.df_reviews.iterrows():
            polarity = TextBlob(str(row['ReviewText'])).sentiment.polarity
            if polarity > 0.1:
                y_pred.append('Positive')
            elif polarity < -0.1:
                y_pred.append('Negative')
            else:
                y_pred.append('Neutral')
        
        accuracy = accuracy_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
        cm = confusion_matrix(y_true, y_pred)
        
        return {
            'Accuracy': f"{accuracy:.3f}",
            'F1-Score': f"{f1:.3f}",
            'ConfusionMatrix': cm
        }
