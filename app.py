import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DB_PATH = Path(__file__).with_name("hotel_manager.db")
st.set_page_config(page_title="StayWise | Hotel Management", page_icon="🏨", layout="wide")

# Global UI polish
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
:root { --sw-ink:#172033; --sw-muted:#64748b; --sw-blue:#3157d5; --sw-pale:#f3f6ff; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background:linear-gradient(180deg,#f7f9ff 0%,#ffffff 36%,#f8fafc 100%); color:var(--sw-ink); }
.block-container { max-width:1440px; padding-top:1.6rem; padding-bottom:3rem; }
h1,h2,h3 { font-family:'Manrope',sans-serif !important; letter-spacing:-.035em; color:#172033; }
h2 { font-size:1.45rem !important; margin-top:1.1rem !important; }
[data-testid="stHeader"] { background:rgba(255,255,255,.8); }
[data-testid="stTabs"] [data-baseweb="tab-list"] { gap:7px; padding:9px; background:#eef2ff; border-radius:16px; }
[data-testid="stTabs"] button[data-baseweb="tab"] { border-radius:11px; padding:10px 14px; font-weight:600; color:#536078; border:1px solid transparent; }
[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] { background:#fff; color:#294bc1; box-shadow:0 3px 12px rgba(32,52,110,.09); }
[data-testid="stMetric"] { background:#fff; border:1px solid #e7ebf4; border-radius:18px; padding:18px 18px 14px; box-shadow:0 6px 20px rgba(30,50,100,.045); }
[data-testid="stMetricLabel"] { color:#65718a; font-weight:600; }
[data-testid="stMetricValue"] { color:#18233a; font-family:'Manrope',sans-serif; font-weight:800; }
[data-testid="stForm"], [data-testid="stDataFrame"], [data-testid="stPlotlyChart"], [data-testid="stAlert"] { border-radius:16px; }
[data-testid="stForm"] { background:#fff; border:1px solid #e5eaf4; padding:20px; }
.stButton button, .stFormSubmitButton button, .stDownloadButton button, .stLinkButton a { border-radius:11px; font-weight:700; min-height:2.7rem; transition:all .18s ease; }
.stButton button[kind="primary"], .stFormSubmitButton button[kind="primary"] { background:linear-gradient(135deg,#365be0,#2444b8); border:0; box-shadow:0 6px 14px rgba(49,87,213,.2); }
.stButton button:hover, .stFormSubmitButton button:hover, .stDownloadButton button:hover { transform:translateY(-1px); }
input, textarea, [data-baseweb="select"] > div { border-radius:10px !important; }
[data-testid="stDataFrame"] { border:1px solid #e7ebf4; overflow:hidden; }
hr { border-color:#e7ebf4; }
.sw-hero { position:relative; overflow:hidden; padding:30px 32px; margin:0 0 22px; border-radius:24px; color:#fff; background:radial-gradient(circle at 90% 15%,rgba(132,164,255,.65),transparent 30%),linear-gradient(120deg,#172b65 0%,#3157d5 58%,#6485ee 100%); box-shadow:0 18px 40px rgba(37,67,163,.18); }
.sw-eyebrow { display:inline-block; padding:6px 10px; border:1px solid rgba(255,255,255,.3); border-radius:999px; background:rgba(255,255,255,.12); font-size:.76rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase; }
.sw-hero h1 { color:#fff !important; font-size:clamp(2rem,4vw,3.1rem) !important; margin:.7rem 0 .4rem !important; line-height:1.08; }
.sw-hero p { color:rgba(255,255,255,.82); font-size:1.02rem; max-width:720px; margin:0; line-height:1.65; }
.sw-hero-foot { display:flex; gap:9px; flex-wrap:wrap; margin-top:18px; }
.sw-chip { display:inline-block; color:#fff; background:rgba(255,255,255,.13); border:1px solid rgba(255,255,255,.2); padding:7px 11px; border-radius:10px; font-size:.82rem; font-weight:600; }
.sw-section-note { color:#64748b; font-size:.92rem; margin-top:-.3rem; margin-bottom:1rem; }
@media (max-width: 700px) { .block-container { padding:1rem .8rem 2rem; } .sw-hero { padding:23px 20px; border-radius:18px; } [data-testid="stTabs"] [data-baseweb="tab-list"] { gap:3px; } [data-testid="stTabs"] button[data-baseweb="tab"] { padding:8px 10px; } }
</style>
""", unsafe_allow_html=True)

ROOM_TYPES = {
    "Standard": {"price": 1800, "capacity": 2, "description": "Comfortable room for solo travellers and couples."},
    "Deluxe": {"price": 2800, "capacity": 2, "description": "Spacious room with upgraded amenities."},
    "Family": {"price": 4200, "capacity": 4, "description": "Larger room for families and small groups."},
    "Suite": {"price": 6500, "capacity": 3, "description": "Premium suite with a separate sitting area."},
}
# Seeded public directory examples for Salem, Tamil Nadu. Listings and ratings should be re-verified.
# The review count/rating snapshot is informational; use the Google Maps link to see the current source reviews.
HOTELS = [
    ("Radisson Hotel Salem", "Salem", "157/3-A, Bangalore Highway, Mamangam, Salem 636302", 4.7),
    ("Zibe Salem by GRT Hotels", "Salem", "GRT Jewellery Building, 14/1 Omalur Main Road, Four Roads, Salem 636009", 4.7),
    ("NM Hotels", "Salem", "42 Post Office Road, Junction Main Road, Suramangalam, Salem 636005", 4.8),
    ("Sivaraj Inn", "Salem", "603 Junction Main Road, Nedunchalai Nagar, Salem 636005", 4.8),
    ("Hotel Shrie Shaanth", "Salem", "2/217 Manivannan Road, Swarnapuri, Salem 636004", 4.0),
    ("Hotel Cenneys Gateway", "Salem", "97/4 Saradha College Main Road, Five Roads, Salem 636016", 4.2),
    ("Grand Estancia", "Salem", "349/3 Bangalore Bypass Road, Narasothipatti, Salem 636004", 4.5),
    ("Hotel Rathna Residency", "Salem", "17/14 Three Roads, Suramangalam Main Road, Salem 636009", 3.7),
    ("Hotel Pearls", "Salem", "12/278A Raman Road, near New Bus Stand, Salem 636004", 3.0),
    ("Sri K Residency", "Salem", "182 Tamil Sangam Road, Hasthampatti, Salem 636007", 0.0),
    ("JMJ Comfort - Service Apartment", "Salem", "4/2 Sarada College Road, Sona Nagar, Salem 636016", 3.5),
    ("Forest Meadows", "Salem", "Udayapatti area, Salem 636140", 4.5),
    ("Selvamathi Farm Resorts", "Salem", "Meenagkadu, Masinaikanpatti, Salem 636103", 0.0),
    ("CM Residency", "Salem", "105 Dr Subbarayan Road, Salem 636001", 5.0),
    ("Hotel Urban Nest", "Salem", "Mayor Nagar, Chennakrishna Puram, Salem 636007", 0.0),
]
HOTEL_REVIEW_COUNTS = {
    "Radisson Hotel Salem": 3001, "Zibe Salem by GRT Hotels": 624,
    "NM Hotels": 264, "Sivaraj Inn": 1193, "Hotel Shrie Shaanth": 1417,
    "Hotel Cenneys Gateway": 174, "Grand Estancia": 1112,
    "Hotel Rathna Residency": 19, "Hotel Pearls": 1,
    "Sri K Residency": 0, "JMJ Comfort - Service Apartment": 6,
    "Forest Meadows": 8, "Selvamathi Farm Resorts": 0, "CM Residency": 1,
    "Hotel Urban Nest": 0,
}
def google_maps_reviews_url(hotel_name):
    from urllib.parse import quote_plus
    return "https://www.google.com/maps/search/?api=1&query=" + quote_plus(hotel_name + ", Salem, Tamil Nadu")
ATTRACTIONS = {
    "Salem": [("Salem Government Museum", "Museum", "Local history and heritage exhibits", 2.0),
             ("Kottai Mariamman Temple", "Heritage", "Historic local temple", 2.5),
             ("Mookaneri Lake", "Lake", "Lake and walking area", 5.5),
             ("Kurumbapatti Zoological Park", "Nature", "Small zoological park and green space", 10.0),
             ("1008 Lingam Temple", "Heritage", "Temple complex near Ariyanoor", 12.0),
             ("Yercaud Lake", "Lake", "Boating and hill-station promenade", 30.0),
             ("Pagoda Point, Yercaud", "Viewpoint", "Hill viewpoint over the surrounding landscape", 35.0)],
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
st.markdown("""
<div class="sw-hero">
  <span class="sw-eyebrow">STAYWISE · HOTEL OPERATIONS</span>
  <h1>Your stay, beautifully managed.</h1>
  <p>A modern workspace for reservations, front-desk operations, Salem hotel discovery, guest feedback and clear business insights.</p>
  <div class="sw-hero-foot">
    <span class="sw-chip">✦ Smart reservations</span>
    <span class="sw-chip">⌂ Front-desk workspace</span>
    <span class="sw-chip">↗ Live dashboard from your demo data</span>
  </div>
</div>
""", unsafe_allow_html=True)
pages = st.tabs([
    "◈ Overview", "⌕ Find & Book", "▤ Bookings", "✓ Check-in / Check-out",
    "⌂ Rooms & Hotels", "⌖ Nearby Attractions", "☆ Guest Reviews", "▥ Analytics"
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
    st.subheader("Salem hotel directory")
    st.caption("Directory seed data compiled from public business listings. It is not guaranteed to include every hotel; verify current details before booking.")
    hotel_rows = []
    for name, city_name, address, rating in HOTELS:
        hotel_rows.append({
            "Hotel": name, "City": city_name, "Address": address,
            "Public rating snapshot": f"{rating:.1f}/5" if rating else "Not available",
            "Review count snapshot": HOTEL_REVIEW_COUNTS.get(name, 0),
            "Review history / current listing": google_maps_reviews_url(name),
        })
    st.dataframe(pd.DataFrame(hotel_rows), use_container_width=True, hide_index=True,
                 column_config={"Review history / current listing": st.column_config.LinkColumn("Review history / current listing", display_text="Open Google Maps")})
    st.info("Google Maps opens the hotel's current listing and available reviews. This app does not copy or store every historical Google review. The Places API exposes only a limited set of reviews per place; full historical archives are not generally available for third-party hotels.")
    st.subheader("Room inventory used by this demo booking system")
    inv = read_df("SELECT hotel, room_type, total_rooms FROM room_inventory ORDER BY hotel, room_type")
    st.dataframe(inv, use_container_width=True, hide_index=True)
    st.caption("Room counts and prices are demo inventory, not live availability or official hotel rates. Adjust them for a real property.")

# NEARBY ATTRACTIONS
with pages[5]:
    st.subheader("Tourist attractions near each hotel")
    city = st.selectbox("Choose city", sorted(ATTRACTIONS), key="attraction_city")
    hotel = next(h[0] for h in HOTELS if h[1] == city)
    st.write(f"Selected hotel: **{hotel}**")
    attractions = pd.DataFrame(ATTRACTIONS[city], columns=["Attraction","Category","Description","Distance (km)"])
    st.dataframe(attractions.sort_values("Distance (km)"), use_container_width=True, hide_index=True)
    st.caption("Attraction distances are approximate illustrative values, not live routing distances.")
    st.link_button("Explore tourist attractions on Google Maps", f"https://www.google.com/maps/search/tourist+attractions+in+{city.replace(' ','+')}")

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
