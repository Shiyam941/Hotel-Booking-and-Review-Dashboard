import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DB_PATH = Path(__file__).with_name("hotel_manager.db")
st.set_page_config(page_title="StayWise | Hotel Management", page_icon="🏨", layout="wide")

ROOM_TYPES = {
    "Standard": {"price": 1800, "capacity": 2, "description": "Comfortable room for solo travellers and couples."},
    "Deluxe": {"price": 2800, "capacity": 2, "description": "Spacious room with upgraded amenities."},
    "Family": {"price": 4200, "capacity": 4, "description": "Larger room for families and small groups."},
    "Suite": {"price": 6500, "capacity": 3, "description": "Premium suite with a separate sitting area."},
}
HOTELS = [
    ("StayWise City Hotel", "Chennai", "Near the city centre", 4.4),
    ("StayWise Heritage Inn", "Madurai", "Near the temple district", 4.6),
    ("StayWise Hill Retreat", "Ooty", "Near the botanical garden", 4.5),
]
ATTRACTIONS = {
    "Chennai": [("Marina Beach", "Beach", "Popular city beach and promenade", 6.2),
                ("Government Museum", "Museum", "Art, archaeology and history collections", 4.8),
                ("Kapaleeshwarar Temple", "Heritage", "Historic Dravidian-style temple", 7.1)],
    "Madurai": [("Meenakshi Amman Temple", "Heritage", "Historic temple complex", 1.4),
                ("Thirumalai Nayakkar Mahal", "Palace", "Seventeenth-century palace", 2.2),
                ("Gandhi Memorial Museum", "Museum", "Museum on India's freedom movement", 3.5)],
    "Ooty": [("Government Botanical Garden", "Garden", "Terraced botanical gardens", 1.8),
             ("Ooty Lake", "Lake", "Lake with boating and walking areas", 2.6),
             ("Doddabetta Peak", "Viewpoint", "Panoramic hilltop viewpoint", 9.5)],
}

def connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_code TEXT UNIQUE NOT NULL,
            guest_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            hotel TEXT NOT NULL,
            city TEXT NOT NULL,
            room_type TEXT NOT NULL,
            rooms INTEGER NOT NULL,
            guests INTEGER NOT NULL,
            check_in TEXT NOT NULL,
            check_out TEXT NOT NULL,
            nights INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Booked',
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_code TEXT NOT NULL,
            guest_name TEXT NOT NULL,
            hotel TEXT NOT NULL,
            rating INTEGER NOT NULL,
            review_text TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS room_inventory (
            hotel TEXT NOT NULL,
            room_type TEXT NOT NULL,
            total_rooms INTEGER NOT NULL,
            PRIMARY KEY (hotel, room_type)
        );
        """)
        for hotel, city, location, rating in HOTELS:
            for room_type, spec in ROOM_TYPES.items():
                conn.execute(
                    "INSERT OR IGNORE INTO room_inventory(hotel, room_type, total_rooms) VALUES(?,?,?)",
                    (hotel, room_type, 10 if room_type in ("Standard", "Deluxe") else 5),
                )

def read_df(query, params=()):
    with connect() as conn:
        return pd.read_sql_query(query, conn, params=params)

def available_rooms(hotel, room_type, start, end):
    with connect() as conn:
        total = conn.execute(
            "SELECT total_rooms FROM room_inventory WHERE hotel=? AND room_type=?",
            (hotel, room_type),
        ).fetchone()
        if not total:
            return 0
        booked = conn.execute("""
            SELECT COALESCE(SUM(rooms), 0) AS n FROM bookings
            WHERE hotel=? AND room_type=? AND status IN ('Booked','Checked In')
              AND check_in < ? AND check_out > ?
        """, (hotel, room_type, end.isoformat(), start.isoformat())).fetchone()["n"]
        return max(0, int(total["total_rooms"]) - int(booked))

def money(value):
    return f"₹{float(value):,.0f}"

init_db()
st.title("StayWise")
st.caption("Hotel booking, front-desk operations, guest reviews and business analytics")
pages = st.tabs([
    "Overview", "Find & Book", "Bookings", "Check-in / Check-out",
    "Rooms & Hotels", "Nearby Attractions", "Guest Reviews", "Analytics"
])

# OVERVIEW
with pages[0]:
    bookings = read_df("SELECT * FROM bookings")
    reviews = read_df("SELECT * FROM reviews")
    today = date.today().isoformat()
    active = bookings[bookings["status"].isin(["Booked", "Checked In"])] if not bookings.empty else bookings
    arriving = bookings[(bookings["check_in"] == today) & (bookings["status"] == "Booked")] if not bookings.empty else bookings
    checked_in = bookings[bookings["status"] == "Checked In"] if not bookings.empty else bookings
    revenue = bookings.loc[bookings["status"].isin(["Checked In", "Checked Out"]), "total_amount"].sum() if not bookings.empty else 0
    cols = st.columns(5)
    for col, label, value in zip(cols, ["Total bookings", "Active reservations", "Arrivals today", "Currently checked in", "Revenue collected*"],
                                 [len(bookings), len(active), len(arriving), len(checked_in), money(revenue)]):
        col.metric(label, value)
    st.caption("*Revenue is a demo operational estimate based on checked-in and checked-out bookings.")
    left, right = st.columns(2)
    with left:
        st.subheader("Booking status")
        if not bookings.empty:
            st.plotly_chart(px.pie(bookings, names="status", hole=0.45), use_container_width=True)
        else:
            st.info("No bookings yet. Add a reservation from Find & Book.")
    with right:
        st.subheader("Bookings by room type")
        if not bookings.empty:
            st.plotly_chart(px.bar(bookings.groupby("room_type", as_index=False)["id"].count().rename(columns={"id":"bookings"}),
                                   x="room_type", y="bookings"), use_container_width=True)
        else:
            st.info("Room-type statistics will appear after bookings are created.")
    st.subheader("Today's front-desk arrivals")
    if not arriving.empty:
        st.dataframe(arriving[["booking_code","guest_name","hotel","room_type","check_out","status"]], use_container_width=True, hide_index=True)
    else:
        st.write("No scheduled arrivals today.")
    st.subheader("Latest reservations")
    if not bookings.empty:
        st.dataframe(bookings.sort_values("created_at", ascending=False).head(8)[
            ["booking_code","guest_name","hotel","room_type","check_in","check_out","total_amount","status"]],
            use_container_width=True, hide_index=True)

# FIND AND BOOK
with pages[1]:
    st.subheader("Search availability and create a reservation")
    with st.form("booking_form"):
        city = st.selectbox("Destination", sorted({h[1] for h in HOTELS}))
        hotel_options = [h[0] for h in HOTELS if h[1] == city]
        hotel = st.selectbox("Hotel", hotel_options)
        room_type = st.selectbox("Room type", list(ROOM_TYPES), format_func=lambda x: f"{x} — {money(ROOM_TYPES[x]['price'])}/night")
        spec = ROOM_TYPES[room_type]
        st.caption(f"{spec['description']} Sleeps up to {spec['capacity']} guests per room.")
        c1, c2, c3 = st.columns(3)
        check_in = c1.date_input("Check-in date", min_value=date.today(), value=date.today() + timedelta(days=1))
        check_out = c2.date_input("Check-out date", min_value=date.today() + timedelta(days=2), value=date.today() + timedelta(days=2))
        rooms = c3.number_input("Number of rooms", min_value=1, max_value=10, value=1)
        c4, c5 = st.columns(2)
        guests = c4.number_input("Number of guests", min_value=1, max_value=20, value=2)
        guest_name = c5.text_input("Guest full name")
        c6, c7 = st.columns(2)
        email = c6.text_input("Email address")
        phone = c7.text_input("Phone number")
        submitted = st.form_submit_button("Check availability & book", type="primary")
    if submitted:
        if check_out <= check_in:
            st.error("Check-out must be later than check-in.")
        elif guests > int(rooms) * spec["capacity"]:
            st.error(f"{room_type} rooms accommodate up to {int(rooms) * spec['capacity']} guests for this booking.")
        elif not guest_name.strip() or not email.strip() or not phone.strip():
            st.error("Enter the guest name, email and phone number.")
        else:
            available = available_rooms(hotel, room_type, check_in, check_out)
            if available < int(rooms):
                st.error(f"Only {available} {room_type} room(s) are available for those dates.")
            else:
                nights = (check_out - check_in).days
                total = nights * int(rooms) * spec["price"]
                code = "SW" + datetime.now().strftime("%y%m%d%H%M%S%f")[-10:]
                with connect() as conn:
                    conn.execute("""INSERT INTO bookings
                    (booking_code,guest_name,email,phone,hotel,city,room_type,rooms,guests,check_in,check_out,nights,total_amount,status,created_at)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,'Booked',?)""",
                    (code,guest_name.strip(),email.strip(),phone.strip(),hotel,city,room_type,int(rooms),int(guests),
                     check_in.isoformat(),check_out.isoformat(),nights,total,datetime.now().isoformat(timespec="seconds")))
                st.success(f"Reservation created. Booking reference: {code}. Total: {money(total)} for {nights} night(s).")
    st.subheader("Room rates")
    st.dataframe(pd.DataFrame([{"Room type": k, "Price/night": money(v["price"]), "Capacity per room": v["capacity"], "Description": v["description"]} for k,v in ROOM_TYPES.items()]),
                 use_container_width=True, hide_index=True)

# BOOKINGS
with pages[2]:
    st.subheader("Reservation management")
    q = st.text_input("Search by booking reference, guest name, phone, or email")
    df = read_df("SELECT * FROM bookings ORDER BY created_at DESC")
    if q and not df.empty:
        mask = df[["booking_code","guest_name","phone","email"]].astype(str).apply(lambda col: col.str.contains(q, case=False, na=False)).any(axis=1)
        df = df[mask]
    if df.empty:
        st.info("No matching bookings found.")
    else:
        st.dataframe(df[["booking_code","guest_name","hotel","room_type","rooms","check_in","check_out","total_amount","status"]],
                     use_container_width=True, hide_index=True)
        cancel_code = st.text_input("Booking reference to cancel")
        if st.button("Cancel reservation"):
            with connect() as conn:
                row = conn.execute("SELECT status FROM bookings WHERE booking_code=?", (cancel_code.strip(),)).fetchone()
                if not row:
                    st.error("Booking reference not found.")
                elif row["status"] != "Booked":
                    st.error("Only reservations that have not checked in can be cancelled.")
                else:
                    conn.execute("UPDATE bookings SET status='Cancelled' WHERE booking_code=?", (cancel_code.strip(),))
                    st.success("Reservation cancelled.")
                    st.rerun()
        st.download_button("Download booking report (CSV)", df.to_csv(index=False).encode("utf-8"),
                           file_name="staywise_bookings.csv", mime="text/csv")

# CHECK IN / OUT
with pages[3]:
    st.subheader("Front-desk check-in and check-out")
    code = st.text_input("Booking reference", key="frontdesk_code")
    if code:
        match = read_df("SELECT * FROM bookings WHERE booking_code=?", (code.strip(),))
        if match.empty:
            st.warning("Booking reference not found.")
        else:
            row = match.iloc[0]
            st.write(f"**{row['guest_name']}** · {row['hotel']} · {row['room_type']} · {row['check_in']} to {row['check_out']}")
            st.write(f"Status: **{row['status']}** · Total: **{money(row['total_amount'])}**")
            c1, c2 = st.columns(2)
            if c1.button("Confirm check-in", disabled=row["status"] != "Booked"):
                if date.today().isoformat() < row["check_in"]:
                    st.error("Check-in date has not arrived yet.")
                else:
                    with connect() as conn:
                        conn.execute("UPDATE bookings SET status='Checked In' WHERE booking_code=?", (code.strip(),))
                    st.success("Guest checked in.")
                    st.rerun()
            if c2.button("Confirm check-out", disabled=row["status"] != "Checked In"):
                with connect() as conn:
                    conn.execute("UPDATE bookings SET status='Checked Out' WHERE booking_code=?", (code.strip(),))
                st.success("Guest checked out.")
                st.rerun()
    st.caption("Demo workflow: payments, identity verification and real hotel PMS integrations are not connected.")

# ROOMS AND HOTELS
with pages[4]:
    st.subheader("Hotels and room inventory")
    st.dataframe(pd.DataFrame([{"Hotel": h[0], "City": h[1], "Location": h[2], "Sample rating": h[3]} for h in HOTELS]),
                 use_container_width=True, hide_index=True)
    inv = read_df("SELECT hotel, room_type, total_rooms FROM room_inventory ORDER BY hotel, room_type")
    st.dataframe(inv, use_container_width=True, hide_index=True)
    st.caption("The starter inventory is sample data. Adjust room counts in the room_inventory table for your property.")

# NEARBY ATTRACTIONS
with pages[5]:
    st.subheader("Tourist attractions near each hotel")
    city = st.selectbox("Choose city", sorted(ATTRACTIONS), key="attraction_city")
    hotel = next(h[0] for h in HOTELS if h[1] == city)
    st.write(f"Selected hotel: **{hotel}**")
    attractions = pd.DataFrame(ATTRACTIONS[city], columns=["Attraction","Category","Description","Distance (km)"])
    st.dataframe(attractions.sort_values("Distance (km)"), use_container_width=True, hide_index=True)
    st.caption("Distances and attractions are illustrative seed data, not live map results.")
    st.link_button("Explore this city on Google Maps", f"https://www.google.com/maps/search/tourist+attractions+in+{city.replace(' ','+')}")

# REVIEWS
with pages[6]:
    st.subheader("Guest reviews")
    review_bookings = read_df("SELECT booking_code, guest_name, hotel, status FROM bookings WHERE status='Checked Out' ORDER BY created_at DESC")
    if not review_bookings.empty:
        booking_codes = review_bookings["booking_code"].tolist()
        selected_code = st.selectbox("Select checked-out booking", booking_codes)
        guest = review_bookings[review_bookings["booking_code"] == selected_code].iloc[0]
        with st.form("review_form"):
            rating = st.slider("Rating", min_value=1, max_value=5, value=5)
            review_text = st.text_area("Write your review", max_chars=1000)
            save_review = st.form_submit_button("Submit review")
        if save_review:
            if not review_text.strip():
                st.error("Enter review text before submitting.")
            else:
                with connect() as conn:
                    exists = conn.execute("SELECT id FROM reviews WHERE booking_code=?", (selected_code,)).fetchone()
                    if exists:
                        st.error("A review already exists for this booking.")
                    else:
                        conn.execute("INSERT INTO reviews(booking_code,guest_name,hotel,rating,review_text,created_at) VALUES(?,?,?,?,?,?)",
                                     (selected_code,guest["guest_name"],guest["hotel"],int(rating),review_text.strip(),datetime.now().isoformat(timespec="seconds")))
                        st.success("Review submitted.")
                        st.rerun()
    else:
        st.info("Reviews can be submitted after a booking is checked out.")
    reviews = read_df("SELECT * FROM reviews ORDER BY created_at DESC")
    if not reviews.empty:
        st.subheader("Published reviews")
        st.dataframe(reviews[["guest_name","hotel","rating","review_text","created_at"]], use_container_width=True, hide_index=True)
        st.metric("Average rating", f"{reviews['rating'].mean():.1f} / 5")
        st.plotly_chart(px.histogram(reviews, x="rating", nbins=5, title="Review rating distribution"), use_container_width=True)

# ANALYTICS
with pages[7]:
    st.subheader("Management analytics")
    bookings = read_df("SELECT * FROM bookings")
    reviews = read_df("SELECT * FROM reviews")
    if bookings.empty:
        st.info("Create bookings to populate analytics.")
    else:
        valid = bookings[bookings["status"] != "Cancelled"]
        a,b,c,d = st.columns(4)
        a.metric("Bookings", len(bookings))
        b.metric("Cancellation rate", f"{(bookings['status'].eq('Cancelled').mean()*100):.1f}%")
        c.metric("Booked room nights", int((valid["rooms"] * valid["nights"]).sum()))
        d.metric("Average booking value", money(valid["total_amount"].mean() if not valid.empty else 0))
        left, right = st.columns(2)
        with left:
            st.plotly_chart(px.bar(bookings.groupby("hotel", as_index=False).size(), x="hotel", y="size", title="Bookings by hotel"), use_container_width=True)
        with right:
            st.plotly_chart(px.bar(bookings.groupby("room_type", as_index=False)["total_amount"].sum(), x="room_type", y="total_amount", title="Booking value by room type"), use_container_width=True)
        st.plotly_chart(px.line(bookings.groupby("check_in", as_index=False).size(), x="check_in", y="size", title="Reservations by check-in date"), use_container_width=True)
    if not reviews.empty:
        st.subheader("Guest satisfaction")
        left, right = st.columns(2)
        left.metric("Reviews", len(reviews))
        left.metric("Average guest rating", f"{reviews['rating'].mean():.2f}/5")
        right.plotly_chart(px.bar(reviews.groupby("hotel", as_index=False)["rating"].mean(), x="hotel", y="rating", title="Average rating by hotel", range_y=[0,5]), use_container_width=True)
