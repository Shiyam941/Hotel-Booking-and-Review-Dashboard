import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_hotel_data(n_bookings=2000, n_reviews=150):
    # --- Booking Data Generation ---
    start_date = datetime(2023, 1, 1)
    booking_data = []
    
    room_types = ['Standard', 'Deluxe', 'Suite', 'Penthouse']
    channels = ['OTA', 'Direct', 'Corporate', 'GDS']
    segments = ['Leisure', 'Business']
    countries = ['USA', 'UK', 'Germany', 'France', 'India', 'UAE', 'China']
    cancel_reasons = ['Change of plans', 'Found better price', 'Personal emergency', 'Travel restrictions', None]

    for i in range(n_bookings):
        b_date = start_date + timedelta(days=random.randint(0, 480))
        stay_nights = random.randint(1, 14)
        lead_time = random.randint(0, 150)
        room = random.choice(room_types)
        adr = {'Standard': 120, 'Deluxe': 200, 'Suite': 450, 'Penthouse': 1200}[room] + random.uniform(-20, 50)
        
        is_cancelled = random.random() < 0.15 # 15% cancellation rate
        
        booking_data.append({
            'BookingID': f'BK{1000+i}',
            'ArrivalDate': b_date,
            'LeadTime': lead_time,
            'Nights': stay_nights,
            'Guests': random.randint(1, 4),
            'RoomType': room,
            'Channel': random.choice(channels),
            'Segment': random.choice(segments),
            'Country': random.choice(countries),
            'IsCancelled': 1 if is_cancelled else 0,
            'CancelReason': random.choice(cancel_reasons) if is_cancelled else None,
            'ADR': adr,
            'Revenue': adr * stay_nights if not is_cancelled else 0,
            'GuestType': 'Returning' if random.random() < 0.3 else 'New',
            'AgeGroup': random.choice(['18-25', '26-40', '41-60', '60+']),
            'MealPlan': random.choice(['BB', 'HB', 'FB', 'No Meal']),
            'Addons': random.sample(['Spa', 'Airport Transfer', 'Late Checkout', 'Mini Bar'], random.randint(0, 2))
        })
    
    df_bookings = pd.DataFrame(booking_data)
    
    # --- Review Data Generation ---
    review_templates = {
        'Positive': [
            "Amazing stay! The staff was incredibly helpful and the room was spotless.",
            "Great location, right in the heart of the city. Loved the breakfast.",
            "Exceeded expectations. The spa facilities are top-notch.",
            "Very comfortable bed and beautiful view from the balcony.",
            "Excellent service. Check-in was smooth and fast.",
            "The hotel staff went above and beyond to make our stay memorable.",
            "Fantastic amenities and exceptional cleanliness throughout the property.",
            "Best breakfast buffet I've ever had at a hotel. Highly recommend!",
            "The location is perfect for exploring the city. Staff is very friendly.",
            "Wonderful experience from start to finish. Will definitely return.",
            "Luxury finishes and modern decor. Very impressed with the quality.",
            "Outstanding customer service. They handled everything perfectly.",
            "The room was spacious, comfortable, and beautifully decorated.",
            "Amazing value for money. Far exceeded my expectations.",
            "Perfect for business travelers. Has all the amenities you need."
        ],
        'Neutral': [
            "Good hotel but a bit noisy at night. Staff was okay.",
            "Decent stay for the price. Room was small but clean.",
            "Location is great, however, the elevators were slow.",
            "Average experience. Nothing special but no major complaints.",
            "Breakfast was good, but the gym is very limited.",
            "Stayed here for a week. It's fine for a business trip.",
            "The room was as advertised. Check-in took a while though.",
            "Okay parking situation. Wi-Fi worked most of the time.",
            "The restaurant had decent food. Service was average.",
            "Room was comfortable. Housekeeping could have been faster.",
            "It's a decent hotel. Nothing particularly special or bad.",
            "Fine for the price point. Some amenities were broken.",
            "The view was nice but the room was a bit dated.",
            "Staff was neutral but helpful. Rooms could use updating.",
            "Acceptable stay. Would stay here again if needed."
        ],
        'Negative': [
            "Disappointing experience. The room smelled like smoke.",
            "Overpriced for what they offer. The AC was not working.",
            "Very rude staff at the reception. Would not recommend.",
            "Dirty bathroom and the wifi was extremely slow.",
            "The photos online are misleading. The hotel is very old.",
            "Worst stay of my life. The room was infested with bugs.",
            "Unacceptable noise level at night. Could not sleep.",
            "The staff was unhelpful and rude throughout my stay.",
            "Facilities are outdated and not well maintained.",
            "Food poisoning from the hotel restaurant. Terrible experience.",
            "The elevator was broken half of my stay. Very inconvenient.",
            "Overbooked hotel. They downgraded our room without notice.",
            "Mold in the bathroom. This is completely unacceptable.",
            "The heating system was broken and it was freezing.",
            "Would not recommend. Many hidden charges at checkout."
        ]
    }
    
    aspects = ['Staff', 'Cleanliness', 'Location', 'Food', 'Price', 'Amenities']
    reviews = []
    
    for i in range(n_reviews):
        sentiment = random.choices(['Positive', 'Neutral', 'Negative'], weights=[0.55, 0.25, 0.2])[0]
        text = random.choice(review_templates[sentiment])
        rating = {'Positive': random.randint(4, 5), 'Neutral': 3, 'Negative': random.randint(1, 2)}[sentiment]
        
        # Create more realistic aspect sentiments based on overall sentiment
        if sentiment == 'Positive':
            aspect_weights = {'Positive': 0.7, 'Neutral': 0.2, 'Negative': 0.1}
        elif sentiment == 'Negative':
            aspect_weights = {'Negative': 0.6, 'Neutral': 0.3, 'Positive': 0.1}
        else:
            aspect_weights = {'Neutral': 0.5, 'Positive': 0.25, 'Negative': 0.25}
        
        aspect_sent = {}
        for aspect in random.sample(aspects, random.randint(3, 5)):
            aspect_sent[aspect] = random.choices(['Positive', 'Neutral', 'Negative'], 
                                                 weights=[aspect_weights.get('Positive', 0.33), 
                                                         aspect_weights.get('Neutral', 0.33), 
                                                         aspect_weights.get('Negative', 0.34)])[0]
        
        reviews.append({
            'ReviewID': f'RV{2000+i}',
            'HotelID': f'H{random.randint(1, 20)}',
            'Date': start_date + timedelta(days=random.randint(0, 480)),
            'ReviewText': text,
            'Rating': rating,
            'Sentiment': sentiment,
            'Aspects': aspect_sent
        })
        
    df_reviews = pd.DataFrame(reviews)
    
    return df_bookings, df_reviews

if __name__ == "__main__":
    df_b, df_r = generate_hotel_data()
    df_b.to_csv('data/bookings.csv', index=False)
    df_r.to_csv('data/reviews.csv', index=False)
    print("Data generated successfully!")
