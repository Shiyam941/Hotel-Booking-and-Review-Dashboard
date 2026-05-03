import pandas as pd
import numpy as np
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
import warnings
import re

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
        cancel_rate = (cancelled / total_bookings) * 100
        completed = total_bookings - cancelled
        
        adr = self.df_bookings[self.df_bookings['IsCancelled'] == 0]['ADR'].mean()
        total_room_nights = completed * self.df_bookings[self.df_bookings['IsCancelled'] == 0]['Nights'].mean()
        occupancy = (total_room_nights / (480 * 100)) * 100
        revpar = revenue / (480 * 100)
        
        return {
            'Total Bookings': total_bookings,
            'Revenue': f"${revenue:,.0f}",
            'Occupancy Rate': f"{occupancy:.1f}%",
            'Cancellation Rate': f"{cancel_rate:.1f}%",
            'ADR': f"${adr:.2f}",
            'RevPAR': f"${revpar:.2f}"
        }

    def get_channel_performance(self):
        """Channel analysis: OTA vs Direct vs Corporate"""
        channel_data = self.df_bookings.groupby('Channel').agg({
            'BookingID': 'count',
            'Revenue': 'sum',
            'IsCancelled': 'sum',
            'ADR': 'mean'
        }).reset_index()
        channel_data.columns = ['Channel', 'Bookings', 'Revenue', 'Cancellations', 'AvgADR']
        channel_data['CancelRate'] = (channel_data['Cancellations'] / channel_data['Bookings'] * 100).round(2)
        return channel_data

    def get_room_type_analysis(self):
        """Room type performance analysis"""
        room_data = self.df_bookings.groupby('RoomType').agg({
            'BookingID': 'count',
            'Revenue': 'sum',
            'ADR': 'mean',
            'IsCancelled': 'sum'
        }).reset_index()
        room_data.columns = ['RoomType', 'Bookings', 'Revenue', 'AvgADR', 'Cancellations']
        return room_data

    def rfm_analysis(self):
        """Recency, Frequency, Monetary analysis by Country"""
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
        """Segment customers by travel purpose and guest type"""
        segments = self.df_bookings.groupby(['Segment', 'GuestType']).agg({
            'BookingID': 'count',
            'Revenue': 'sum',
            'ADR': 'mean'
        }).reset_index()
        segments.columns = ['TravelPurpose', 'GuestType', 'Bookings', 'Revenue', 'AvgADR']
        return segments

    def seasonal_analysis(self):
        """Seasonal trends - heatmap ready format"""
        self.df_bookings['Month'] = self.df_bookings['ArrivalDate'].dt.month
        self.df_bookings['Week'] = self.df_bookings['ArrivalDate'].dt.isocalendar().week
        
        seasonal = self.df_bookings.pivot_table(
            values='Revenue',
            index='Week',
            columns='Month',
            aggfunc='sum'
        ).fillna(0)
        
        return seasonal

    def forecast_revenue(self, periods=30):
        """Forecast revenue using Simple Exponential Smoothing"""
        daily_revenue = self.df_bookings.groupby(self.df_bookings['ArrivalDate'].dt.date)['Revenue'].sum()
        daily_revenue.index = pd.to_datetime(daily_revenue.index)
        daily_revenue = daily_revenue.sort_index()
        daily_revenue = daily_revenue.asfreq('D', fill_value=0)
        
        if len(daily_revenue) > 10:
            try:
                model = SimpleExpSmoothing(daily_revenue).fit(smoothing_level=0.3, optimized=False)
                forecast = model.forecast(periods)
                return daily_revenue, forecast
            except:
                return daily_revenue, np.zeros(periods)
        return daily_revenue, np.zeros(periods)

    # ============ NLP FEATURES ============

    def analyze_sentiment_detailed(self):
        """Comprehensive sentiment analysis using TextBlob"""
        sentiments = []
        
        for _, row in self.df_reviews.iterrows():
            blob = TextBlob(str(row['ReviewText']))
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            if polarity > 0.1:
                pred_sentiment = 'Positive'
            elif polarity < -0.1:
                pred_sentiment = 'Negative'
            else:
                pred_sentiment = 'Neutral'
            
            sentiments.append({
                'ReviewID': row['ReviewID'],
                'Rating': row['Rating'],
                'ActualSentiment': row['Sentiment'],
                'PredictedSentiment': pred_sentiment,
                'Polarity': polarity,
                'Subjectivity': subjectivity,
                'ReviewText': row['ReviewText']
            })
        
        return pd.DataFrame(sentiments)

    def get_sentiment_metrics(self):
        """Calculate sentiment model performance metrics"""
        df_sentiment = self.analyze_sentiment_detailed()
        
        cm = confusion_matrix(
            df_sentiment['ActualSentiment'],
            df_sentiment['PredictedSentiment'],
            labels=['Positive', 'Neutral', 'Negative']
        )
        
        accuracy = accuracy_score(df_sentiment['ActualSentiment'], df_sentiment['PredictedSentiment'])
        f1 = f1_score(df_sentiment['ActualSentiment'], df_sentiment['PredictedSentiment'], 
                      average='weighted', zero_division=0)
        
        return {
            'accuracy': accuracy,
            'f1_score': f1,
            'confusion_matrix': cm
        }

    def get_sentiment_distribution(self):
        """Get sentiment distribution"""
        df_sentiment = self.analyze_sentiment_detailed()
        dist = df_sentiment['PredictedSentiment'].value_counts().reset_index()
        dist.columns = ['Sentiment', 'Count']
        return dist

    def get_rating_sentiment_correlation(self):
        """Analyze correlation between rating and predicted sentiment"""
        df_sentiment = self.analyze_sentiment_detailed()
        
        rating_sentiment = df_sentiment.groupby('Rating').agg({
            'Polarity': 'mean',
            'ReviewID': 'count'
        }).reset_index()
        rating_sentiment.columns = ['Rating', 'AvgPolarity', 'ReviewCount']
        
        df_sentiment['IsMismatch'] = (
            ((df_sentiment['Rating'] >= 4) & (df_sentiment['PredictedSentiment'] == 'Negative')) |
            ((df_sentiment['Rating'] <= 2) & (df_sentiment['PredictedSentiment'] == 'Positive'))
        )
        
        mismatch_rate = (df_sentiment['IsMismatch'].sum() / len(df_sentiment) * 100)
        
        return rating_sentiment, mismatch_rate

    def get_topic_modeling(self, n_topics=4):
        """LDA Topic Modeling"""
        if len(self.df_reviews) < 10:
            return pd.DataFrame({'Topic': ['Insufficient data'], 'Keywords': ['Need at least 10 reviews']})
        
        texts = self.df_reviews['ReviewText'].astype(str).tolist()
        
        vectorizer = CountVectorizer(
            stop_words='english',
            max_features=100,
            min_df=2,
            lowercase=True
        )
        
        try:
            data_vectorized = vectorizer.fit_transform(texts)
            lda = LatentDirichletAllocation(n_components=n_topics, random_state=42, max_iter=10)
            lda.fit(data_vectorized)
            
            words = vectorizer.get_feature_names_out()
            topics = []
            
            for topic_idx, topic in enumerate(lda.components_):
                top_indices = topic.argsort()[-5:][::-1]
                top_words = [words[i] for i in top_indices]
                topics.append({
                    'Topic': f'Topic {topic_idx + 1}',
                    'Keywords': ', '.join(top_words)
                })
            
            return pd.DataFrame(topics)
        except:
            return pd.DataFrame({'Topic': ['Error'], 'Keywords': ['Could not generate topics']})

    def get_aspect_sentiment_analysis(self):
        """Analyze sentiment by aspect"""
        aspects_list = []
        
        for _, row in self.df_reviews.iterrows():
            if isinstance(row['Aspects'], dict):
                for aspect, sentiment in row['Aspects'].items():
                    aspects_list.append({
                        'Aspect': aspect,
                        'Sentiment': sentiment,
                        'Rating': row['Rating']
                    })
        
        if not aspects_list:
            return pd.DataFrame(), pd.DataFrame()
        
        df_aspects = pd.DataFrame(aspects_list)
        aspect_summary = df_aspects.groupby('Aspect')['Sentiment'].value_counts().unstack(fill_value=0)
        aspect_summary['Total'] = aspect_summary.sum(axis=1)
        
        return df_aspects, aspect_summary

    def get_keywords(self, sentiment_filter=None, top_n=15):
        """Extract top keywords using TF-IDF"""
        if sentiment_filter:
            texts = self.df_reviews[self.df_reviews['Sentiment'] == sentiment_filter]['ReviewText'].tolist()
        else:
            texts = self.df_reviews['ReviewText'].tolist()
        
        texts = [re.sub(r'[^a-zA-Z\s]', '', text.lower()) for text in texts]
        texts = [text for text in texts if text.strip()]
        
        if len(texts) < 2:
            return pd.DataFrame()
        
        vectorizer = TfidfVectorizer(stop_words='english', max_features=top_n, lowercase=True)
        
        try:
            tfidf_matrix = vectorizer.fit_transform(texts)
            scores = tfidf_matrix.sum(axis=0).A1
            keywords = vectorizer.get_feature_names_out()
            keyword_scores = pd.DataFrame({'Keyword': keywords, 'Score': scores})
            return keyword_scores.sort_values('Score', ascending=False)
        except:
            return pd.DataFrame()

    def get_wordcloud_data(self, sentiment_filter=None):
        """Prepare data for word cloud generation"""
        if sentiment_filter:
            texts = ' '.join(self.df_reviews[self.df_reviews['Sentiment'] == sentiment_filter]['ReviewText'].tolist())
        else:
            texts = ' '.join(self.df_reviews['ReviewText'].tolist())
        
        return texts

    def detect_fake_reviews(self, polarity_threshold=0.05, subjectivity_threshold=0.9):
        """Detect potentially fake reviews based on linguistic patterns"""
        df_sentiment = self.analyze_sentiment_detailed()
        
        df_sentiment['VeryHighSubjectivity'] = df_sentiment['Subjectivity'] > subjectivity_threshold
        df_sentiment['NeutralPolarity'] = df_sentiment['Polarity'].abs() < polarity_threshold
        df_sentiment['ReviewLength'] = df_sentiment['ReviewText'].str.split().str.len()
        df_sentiment['VeryShortReview'] = df_sentiment['ReviewLength'] < 5
        
        df_sentiment['FakeReviewScore'] = (
            (df_sentiment['VeryHighSubjectivity'].astype(int) * 0.3) +
            (df_sentiment['NeutralPolarity'].astype(int) * 0.2) +
            (df_sentiment['VeryShortReview'].astype(int) * 0.5)
        )
        
        suspicious = df_sentiment[df_sentiment['FakeReviewScore'] > 0.5].copy()
        
        return suspicious[['ReviewID', 'ReviewText', 'Rating', 'FakeReviewScore']], \
               (len(suspicious) / len(df_sentiment) * 100 if len(df_sentiment) > 0 else 0)

    def get_sentiment_trend(self):
        """Sentiment trend over time"""
        df_sentiment = self.analyze_sentiment_detailed()
        df_sentiment = pd.merge(df_sentiment, self.df_reviews[['ReviewID', 'Date']], on='ReviewID')
        df_sentiment['Date'] = pd.to_datetime(df_sentiment['Date'])
        
        trend = df_sentiment.groupby([df_sentiment['Date'].dt.to_period('M'), 'PredictedSentiment']).size().unstack(fill_value=0)
        
        return trend
