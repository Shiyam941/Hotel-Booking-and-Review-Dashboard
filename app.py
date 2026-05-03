import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from engine import AnalyticsEngine
from data_manager import generate_hotel_data
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np

# Page Config
st.set_page_config(page_title="Hotel Intelligence Dashboard", layout="wide", initial_sidebar_state="expanded")

# Data Initialization
@st.cache_data
def load_data():
    return generate_hotel_data(n_bookings=2000, n_reviews=150)

df_bookings, df_reviews = load_data()
engine = AnalyticsEngine(df_bookings, df_reviews)

# Sidebar Filters
st.sidebar.title("🏨 Hotel Intelligence")
st.sidebar.markdown("---")

date_range = st.sidebar.date_input(
    "Select Date Range", 
    value=[df_bookings['ArrivalDate'].min(), df_bookings['ArrivalDate'].max()],
    key="date_range"
)

countries = df_bookings['Country'].unique().tolist()
hotel_filter = st.sidebar.multiselect(
    "Select Countries", 
    options=countries,
    default=countries,
    key="country_filter"
)

# Filter Data
if len(date_range) == 2:
    filtered_bookings = df_bookings[
        (df_bookings['Country'].isin(hotel_filter)) & 
        (df_bookings['ArrivalDate'].between(pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])))
    ]
else:
    filtered_bookings = df_bookings[df_bookings['Country'].isin(hotel_filter)]

# Main Dashboard
st.title("🏨 Hotel Booking & Review Analytics Dashboard")
st.markdown("#### Decision Support System with NLP & Business Intelligence")

# Create Tabs
tabs = st.tabs([
    "📊 Overview", 
    "📈 Booking Analysis", 
    "👥 Customer Insights", 
    "💰 Revenue & Forecast", 
    "🧠 Sentiment Analysis",
    "📝 Aspect Analysis",
    "🔍 Topic Modeling",
    "🗣️ Fake Reviews",
    "📊 Comparison"
])

# ============ TAB 1: OVERVIEW ============
with tabs[0]:
    st.header("KPI Overview")
    
    kpis = engine.get_kpis()
    cols = st.columns(len(kpis))
    
    for idx, (label, value) in enumerate(kpis.items()):
        with cols[idx]:
            st.metric(label, value)
    
    st.markdown("---")
    
    # Booking Distributions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📌 Booking by Room Type")
        room_dist = filtered_bookings['RoomType'].value_counts()
        if len(room_dist) > 0:
            fig = px.pie(names=room_dist.index, values=room_dist.values)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                             font=dict(color="white"), height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🔗 Booking by Channel")
        channel_dist = filtered_bookings['Channel'].value_counts()
        if len(channel_dist) > 0:
            fig = px.pie(names=channel_dist.index, values=channel_dist.values)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                             font=dict(color="white"), height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        st.subheader("✈️ Booking by Segment")
        segment_dist = filtered_bookings['Segment'].value_counts()
        if len(segment_dist) > 0:
            fig = px.pie(names=segment_dist.index, values=segment_dist.values)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                             font=dict(color="white"), height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    # Monthly Trend
    st.subheader("📅 Monthly Booking & Revenue Trend")
    monthly = filtered_bookings.groupby(filtered_bookings['ArrivalDate'].dt.to_period('M')).agg({
        'BookingID': 'count',
        'Revenue': 'sum'
    }).reset_index()
    monthly['ArrivalDate'] = monthly['ArrivalDate'].astype(str)
    
    if len(monthly) > 0:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=monthly['ArrivalDate'], y=monthly['Revenue'], name='Revenue', yaxis='y1'))
        fig.add_trace(go.Scatter(x=monthly['ArrivalDate'], y=monthly['BookingID'], name='Bookings', yaxis='y2', mode='lines+markers'))
        fig.update_layout(yaxis=dict(title='Revenue ($)'), yaxis2=dict(title='Bookings', overlaying='y', side='right'),
                         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=400)
        st.plotly_chart(fig, use_container_width=True)

# ============ TAB 2: BOOKING ANALYSIS ============
with tabs[1]:
    st.header("Booking Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⏱️ Lead Time Analysis")
        fig = px.histogram(filtered_bookings, x='LeadTime', color='IsCancelled', nbins=30)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💳 Channel Performance")
        channel_perf = engine.get_channel_performance()
        if not channel_perf.empty:
            fig = px.bar(channel_perf, x='Channel', y='Revenue')
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🛏️ Room Type Performance")
        room_perf = engine.get_room_type_analysis()
        if not room_perf.empty:
            fig = px.bar(room_perf, x='RoomType', y='Revenue')
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Cancellation Rate by Room Type")
        cancel_by_room = filtered_bookings.groupby('RoomType')['IsCancelled'].agg(['sum', 'count']).reset_index()
        cancel_by_room['CancelRate'] = (cancel_by_room['sum'] / cancel_by_room['count'] * 100).round(2)
        if len(cancel_by_room) > 0:
            fig = px.bar(cancel_by_room, x='RoomType', y='CancelRate')
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=400)
            st.plotly_chart(fig, use_container_width=True)

# ============ TAB 3: CUSTOMER INSIGHTS ============
with tabs[2]:
    st.header("Customer Segmentation & RFM Analysis")
    
    st.subheader("👥 RFM Analysis by Country")
    rfm = engine.rfm_analysis()
    
    fig = px.scatter(rfm, x='Recency', y='Monetary', size='Frequency', hover_name='Country')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(rfm.sort_values('Monetary', ascending=False), use_container_width=True)
    
    st.markdown("---")
    st.subheader("✈️ Travel Purpose Analysis")
    
    segments = engine.customer_segmentation()
    if not segments.empty:
        fig = px.bar(segments, x='TravelPurpose', y='Revenue', color='GuestType')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=400)
        st.plotly_chart(fig, use_container_width=True)

# ============ TAB 4: REVENUE & FORECAST ============
with tabs[3]:
    st.header("Revenue & Forecasting")
    
    st.subheader("📈 30-Day Revenue Forecast")
    hist, forecast = engine.forecast_revenue(periods=30)
    
    if len(hist) > 0:
        last_date = hist.index[-1]
        forecast_index = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=len(forecast), freq='D')
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist.index, y=hist.values, name='Historical Revenue', fill='tozeroy'))
        fig.add_trace(go.Scatter(x=forecast_index, y=forecast.values, name='Forecast', line=dict(dash='dash')))
        
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🌡️ Seasonal Trends")
    seasonal = engine.seasonal_analysis()
    if not seasonal.empty:
        fig = px.imshow(seasonal)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🔗 Association Rule Mining")
    rules = engine.association_rules_mining()
    if not rules.empty:
        st.dataframe(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].round(3), use_container_width=True)
    else:
        st.info("No strong association rules found")

# ============ TAB 5: SENTIMENT ANALYSIS ============
with tabs[4]:
    st.header("🧠 NLP Sentiment Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sentiment Distribution")
        sentiment_dist = engine.get_sentiment_distribution()
        if len(sentiment_dist) > 0:
            fig = px.pie(sentiment_dist, names='Sentiment', values='Count')
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Rating Distribution")
        rating_dist = df_reviews['Rating'].value_counts().sort_index()
        if len(rating_dist) > 0:
            fig = px.bar(x=rating_dist.index, y=rating_dist.values)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("⭐ Rating vs Sentiment Correlation")
    rating_sentiment, mismatch_rate = engine.get_rating_sentiment_correlation()
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(rating_sentiment, x='Rating', y='AvgPolarity')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.metric("Rating-Sentiment Mismatch Rate", f"{mismatch_rate:.2f}%")
        st.info(f"Reviews where rating doesn't match sentiment")

# ============ TAB 6: ASPECT-BASED SENTIMENT ============
with tabs[5]:
    st.header("📝 Aspect-Based Sentiment Analysis")
    
    st.subheader("Sentiment by Aspect")
    aspect_data = engine.get_aspect_sentiment()
    
    if len(aspect_data) > 0:
        fig = px.bar(aspect_data, x='Aspect', color='Sentiment')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Aspect Summary")
        aspect_summary = engine.get_aspect_summary()
        st.dataframe(aspect_summary, use_container_width=True)

# ============ TAB 7: TOPIC MODELING ============
with tabs[6]:
    st.header("🔍 Topic Modeling with LDA")
    
    n_topics = st.slider("Number of Topics", 2, 6, 3, key="n_topics_slider")
    topics_df = engine.topic_modeling(n_topics=n_topics)
    
    if len(topics_df) > 0:
        st.dataframe(topics_df, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Word Cloud - Positive Reviews")
        
        positive_text = engine.get_wordcloud_data('Positive')
        if len(positive_text) > 10:
            wc = WordCloud(width=800, height=400, background_color='white').generate(positive_text)
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wc, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)

# ============ TAB 8: FAKE REVIEW DETECTION ============
with tabs[7]:
    st.header("🗣️ Fake Review Detection")
    
    fake_reviews = engine.detect_fake_reviews()
    
    if len(fake_reviews) > 0:
        st.metric("Potential Fake Reviews", int(fake_reviews['IsFake'].sum()))
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Fake Score Distribution")
            fig = px.histogram(fake_reviews, x='FakeScore', nbins=20)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Suspicious Reviews")
            suspicious = fake_reviews[fake_reviews['IsFake']].sort_values('FakeScore', ascending=False).head(10)
            st.dataframe(suspicious, use_container_width=True)

# ============ TAB 9: COMPARISON ============
with tabs[8]:
    st.header("📊 Comparison Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Bookings by Country")
        country_bookings = filtered_bookings['Country'].value_counts()
        if len(country_bookings) > 0:
            fig = px.bar(x=country_bookings.index, y=country_bookings.values)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Revenue by Country")
        country_revenue = filtered_bookings.groupby('Country')['Revenue'].sum().sort_values(ascending=False)
        if len(country_revenue) > 0:
            fig = px.bar(x=country_revenue.index, y=country_revenue.values)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Model Evaluation Metrics")
    metrics = engine.model_evaluation_metrics()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Accuracy", metrics['Accuracy'])
    with col2:
        st.metric("F1-Score", metrics['F1-Score'])
    
    st.subheader("Confusion Matrix")
    st.dataframe(pd.DataFrame(metrics['ConfusionMatrix'], 
                             index=['Pred: Neg', 'Pred: Neu', 'Pred: Pos'],
                             columns=['Actual: Neg', 'Actual: Neu', 'Actual: Pos']))
