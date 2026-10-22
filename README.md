# StayWise — Salem Hotel Booking & Management Dashboard

A Streamlit prototype for Salem, Tamil Nadu hotel discovery, sample reservations, front-desk workflows, guest reviews, and operations analytics.

## Features

- **Overview dashboard:** reservation totals, arrivals, checked-in guests, status charts, and recent reservations.
- **Find & Book:** choose from a seed directory of Salem hotels, select a room category and dates, check prototype inventory, and calculate a sample total.
- **Reservation management:** search by booking reference, guest name, phone, or email; cancel eligible reservations and export reports to CSV.
- **Check-in / Check-out:** update a reservation's operational status.
- **Salem hotel directory:** public-listing examples with addresses, rating/review-count snapshots when available, and links to current Google Maps listings/reviews.
- **Nearby attractions:** browse sample Salem and Yercaud-area attractions and open Google Maps searches.
- **Guest reviews:** accept local reviews after checkout and show ratings from bookings created in this app.
- **Analytics:** booking trends, room-type performance, cancellation rate, room nights, booking value, and guest satisfaction.

## Technology

Python, Streamlit, SQLite, Pandas, Plotly

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

## Important limitations

- The Salem hotel directory is a seed list of public listings, not a verified exhaustive list of every hotel. Verify current addresses, ratings, review counts, and availability before relying on it.
- Rating and review-count values are snapshots from available business-search results and may change; a value of 0 means no snapshot was available, not necessarily that a property has zero reviews.
- The app links to Google Maps for current review pages. It does **not** download, embed, or preserve the full historical review archive for each third-party hotel. Google's Places API only exposes a limited set of reviews per place; paginated Google Business Profile review access is for verified locations the authenticated user manages. See the official [Business Profile reviews API](https://developers.google.com/my-business/reference/rest/v4/accounts.locations.reviews/list) and [Places API review fields](https://developers.google.com/maps/documentation/places/web-service/reference/rest/v1/places).
- Room inventory and rates are demo data, not live availability or official hotel rates. Reservations created here are local demo reservations, not bookings made with the hotels.
- No payment gateway, hotel PMS, identity verification, SMS/email notifications, or authenticated admin/customer roles are connected. Add authentication, privacy controls, live inventory and a supported booking integration before production deployment.
- The app creates `hotel_manager.db` beside `app.py`; local SQLite storage is for a demo, not multi-instance public hosting.

## Repository

https://github.com/Shiyam941/Hotel-Booking-and-Review-Dashboard
