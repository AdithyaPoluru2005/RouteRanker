# Module 2: Feature Engineering

## Cities Covered
Delhi, Hyderabad, Bengaluru, Chennai, Mumbai and Pune.

## Features Created
- Total trips per route.
- Total distinct stops per route.
- Arrival and departure hours and minutes.
- Time categories: Morning, Afternoon, Evening and Night.
- Scheduled trip counts by route and service hour.

## Time Categories
- Morning: 5 AM–12 PM
- Afternoon: 12 PM–5 PM
- Evening: 5 PM–9 PM
- Night: Remaining hours.

## Data Quality
- Checked missing values and duplicate route/trip IDs.
- Checked invalid arrival and departure times.
- Some routes in Bengaluru, Chennai and Mumbai had no matching trip records.

## Assumptions and Limitations
- GTFS data represents scheduled services, not actual vehicle operations.
- Trip counts do not represent passenger demand or occupancy.
- Route length was not calculated because suitable shape data was not verified.
- Operating-day analysis and headway analysis require further validation.

## Output Files
Each city's processed folder contains:
- route_profile.csv
- hourly_trip_counts.csv
- time_features.csv
