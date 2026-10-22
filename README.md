# StayWise — Hotel Booking & Management Dashboard

A Streamlit application for managing hotel reservations, room availability, front-desk check-in/check-out, tourist attractions, guest reviews, and hotel operations analytics.

## Features

- **Overview dashboard:** booking totals, active reservations, arrivals today, checked-in guests, estimated revenue, booking status charts, and recent reservations.
- **Find & Book:** choose a destination, hotel, room category, dates, number of rooms, and guests; validate availability and calculate the total cost.
- **Reservation management:** search by booking reference, guest name, phone, or email; cancel eligible reservations and export bookings to CSV.
- **Check-in / Check-out:** look up a reservation and update its operational status.
- **Rooms & Hotels:** browse sample hotels, room categories, room capacity, rates, and inventory.
- **Nearby Attractions:** explore example tourist attractions near hotels and open city searches in Google Maps.
- **Guest Reviews:** allow reviews after checkout, enforce one review per booking, display ratings, and summarize guest feedback.
- **Analytics:** booking trends, room-type performance, cancellation rate, room nights, booking value, and guest satisfaction.

## Technology

- Python
- Streamlit
- SQLite (local persistent database)
- Pandas
- Plotly

## Run locally

Python 3.10 or newer is recommended.

```bash
git clone https://github.com/Shiyam941/Hotel-Booking-and-Review-Dashboard.git
cd Hotel-Booking-and-Review-Dashboard
python -m venv .venv
```

Windows:

```powershell
.venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit, normally http://localhost:8501.

## Data and demo limitations

- The app creates `hotel_manager.db` beside `app.py` on first run. SQLite data persists across local restarts.
- Hotel names, room inventory, room rates, and attraction distances are sample data for demonstration. Update `HOTELS`, `ROOM_TYPES`, `ATTRACTIONS`, and `room_inventory` for a real property.
- The attractions list is not a live geospatial service; distances are illustrative. The Google Maps link opens a city-level attraction search.
- This is a prototype, not a production booking/payment platform. It does not integrate payment gateways, identity verification, email/SMS notifications, live inventory from a hotel PMS, or authenticated customer/admin roles.
- Before public deployment, add authentication and authorization, protect personal data, configure backups and database hosting, use transactions for concurrent inventory reservations, and validate all operational policies.
- The existing `engine.py` and `data_manager.py` analytics prototype remain in the repository for reference; the current `app.py` focuses on hotel operations and management dashboards.

## GitHub

Repository: https://github.com/Shiyam941/Hotel-Booking-and-Review-Dashboard
