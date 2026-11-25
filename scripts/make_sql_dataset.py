"""Generate the FICTIONAL "RideNest" ride-hailing dataset used on the /sql page.

Everything here is made up. Same seed -> same data, every time.

    py -3 scripts/make_sql_dataset.py

Writes:
    public/sql/rideshare.sqlite   the database the browser loads
    docs/sql-dataset.md           a description of every table and column

Deliberate patterns to find with SQL:
    - Weekend peaks: Friday and Saturday evenings are the busiest times.
    - Promo period: WINTER20 (20% off, 2 to 29 June 2025) lifts trips and sign-ups.
    - Churn: some riders stop riding part-way through the year; riders who
      signed up through the promo churn more often.
    - Cancelled trips have NULL fare, distance, duration and rating.
"""
from __future__ import annotations

import random
import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

SEED = 2025
START = date(2025, 1, 1)
END = date(2025, 12, 31)
N_RIDERS = 700
N_DRIVERS = 120
BASE_TRIPS_PER_DAY = 12.6  # tuned so the year has about 5,000 trips

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "public" / "sql" / "rideshare.sqlite"
DOC_PATH = ROOT / "docs" / "sql-dataset.md"

ZONES = ["CBD", "North", "South", "East", "West", "Airport"]
ZONE_WEIGHTS = [0.30, 0.17, 0.17, 0.15, 0.15, 0.06]

PROMOS = [
    # promo_id, code, description, discount_pct, start, end, min_fare_aud
    (1, "WELCOME10", "10% off a new rider's first completed trip", 10, date(2025, 1, 1), date(2025, 12, 31), 0.0),
    (2, "WINTER20", "20% off all trips during the winter campaign", 20, date(2025, 6, 2), date(2025, 6, 29), 8.0),
    (3, "FRIDAYNIGHT", "15% off Friday trips from 6 pm in October", 15, date(2025, 10, 1), date(2025, 10, 31), 10.0),
]
WINTER_START, WINTER_END = PROMOS[1][4], PROMOS[1][5]

# Table and column descriptions: used for CREATE TABLE and for docs/sql-dataset.md.
SCHEMA = {
    "about": {
        "description": "One row explaining that this dataset is fictional.",
        "columns": [
            ("name", "TEXT", "Dataset name."),
            ("note", "TEXT", "States that the data is made up."),
            ("generated_by", "TEXT", "Script that produced the file."),
        ],
    },
    "riders": {
        "description": "People who request trips.",
        "columns": [
            ("rider_id", "INTEGER PRIMARY KEY", "Unique rider ID."),
            ("signup_date", "TEXT", "Date the rider created an account (YYYY-MM-DD). Some signed up before 2025."),
            ("home_zone", "TEXT", "Zone the rider lives in: CBD, North, South, East, West or Airport."),
            ("age_band", "TEXT", "Age group: 18-24, 25-34, 35-44, 45-54 or 55+."),
            ("referral_source", "TEXT", "How they found RideNest: organic, friend, social_ad or promo."),
            ("marketing_opt_in", "INTEGER", "1 if they agreed to marketing emails, else 0."),
        ],
    },
    "drivers": {
        "description": "People who complete trips.",
        "columns": [
            ("driver_id", "INTEGER PRIMARY KEY", "Unique driver ID."),
            ("join_date", "TEXT", "Date the driver joined (YYYY-MM-DD)."),
            ("vehicle_type", "TEXT", "economy, comfort, xl (6+ seats) or ev (electric)."),
            ("home_zone", "TEXT", "Zone the driver is based in."),
            ("is_active", "INTEGER", "1 if still driving at the end of 2025, 0 if they stopped part-way through the year."),
        ],
    },
    "promos": {
        "description": "Discount codes.",
        "columns": [
            ("promo_id", "INTEGER PRIMARY KEY", "Unique promo ID."),
            ("code", "TEXT", "Code shown to riders, e.g. WINTER20."),
            ("description", "TEXT", "What the promo offers."),
            ("discount_pct", "INTEGER", "Percentage taken off the fare."),
            ("start_date", "TEXT", "First day the code works (YYYY-MM-DD)."),
            ("end_date", "TEXT", "Last day the code works (YYYY-MM-DD)."),
            ("min_fare_aud", "REAL", "Minimum fare for the code to apply, in AUD."),
        ],
    },
    "trips": {
        "description": "Every trip requested in 2025, including cancelled ones.",
        "columns": [
            ("trip_id", "INTEGER PRIMARY KEY", "Unique trip ID, in time order."),
            ("rider_id", "INTEGER", "Rider who requested the trip (riders.rider_id)."),
            ("driver_id", "INTEGER", "Driver assigned (drivers.driver_id)."),
            ("requested_at", "TEXT", "Local date and time of the request (YYYY-MM-DD HH:MM:SS)."),
            ("pickup_zone", "TEXT", "Zone where the trip starts."),
            ("dropoff_zone", "TEXT", "Zone where the trip ends."),
            ("status", "TEXT", "completed, cancelled_rider or cancelled_driver."),
            ("distance_km", "REAL", "Trip distance in km. NULL if cancelled."),
            ("duration_min", "INTEGER", "Trip duration in minutes. NULL if cancelled."),
            ("fare_aud", "REAL", "Fare before discount, in AUD. NULL if cancelled."),
            ("discount_aud", "REAL", "Discount applied, in AUD (0 if none)."),
            ("promo_id", "INTEGER", "Promo used (promos.promo_id), or NULL."),
            ("payment_method", "TEXT", "card or wallet."),
            ("rider_rating", "INTEGER", "Rider's rating of the trip, 1 to 5. NULL if not rated or cancelled."),
        ],
    },
}


def daterange(a: date, b: date):
    d = a
    while d <= b:
        yield d
        d += timedelta(days=1)


def make_riders(rng: random.Random):
    riders = []
    for rider_id in range(1, N_RIDERS + 1):
        roll = rng.random()
        if roll < 0.55:  # existing customers from before 2025
            signup = date(2023, 1, 1) + timedelta(days=rng.randrange(730))
            source = rng.choices(["organic", "friend", "social_ad"], [0.5, 0.3, 0.2])[0]
        elif roll < 0.72:  # joined during the WINTER20 campaign
            signup = WINTER_START + timedelta(days=rng.randrange((WINTER_END - WINTER_START).days + 1))
            source = rng.choices(["promo", "organic", "friend"], [0.75, 0.15, 0.10])[0]
        else:  # joined at some other point in 2025
            signup = START + timedelta(days=rng.randrange(330))
            source = rng.choices(["organic", "friend", "social_ad"], [0.45, 0.3, 0.25])[0]

        # Activity: some riders are heavy users, most are occasional.
        weight = rng.lognormvariate(0, 0.8)
        active_from = max(signup, START)
        active_to = END
        churn_p = 0.55 if source == "promo" else 0.18
        if rng.random() < churn_p:
            # Churners stop 3 to 20 weeks after they start riding in 2025.
            active_to = min(END, active_from + timedelta(days=rng.randint(21, 140)))
        riders.append({
            "rider_id": rider_id,
            "signup_date": signup.isoformat(),
            "home_zone": rng.choices(ZONES, ZONE_WEIGHTS)[0],
            "age_band": rng.choices(["18-24", "25-34", "35-44", "45-54", "55+"], [0.22, 0.34, 0.2, 0.14, 0.1])[0],
            "referral_source": source,
            "marketing_opt_in": 1 if rng.random() < 0.42 else 0,
            "_weight": weight,
            "_from": active_from,
            "_to": active_to,
        })
    return riders


def make_drivers(rng: random.Random):
    drivers = []
    for driver_id in range(1, N_DRIVERS + 1):
        join = date(2022, 6, 1) + timedelta(days=rng.randrange(1000))
        join = min(join, date(2025, 11, 1))
        active = rng.random() > 0.15
        leave = END if active else max(join, START) + timedelta(days=rng.randint(30, 200))
        drivers.append({
            "driver_id": driver_id,
            "join_date": join.isoformat(),
            "vehicle_type": rng.choices(["economy", "comfort", "xl", "ev"], [0.5, 0.2, 0.1, 0.2])[0],
            "home_zone": rng.choices(ZONES[:5], [0.3, 0.18, 0.18, 0.17, 0.17])[0],
            "is_active": 1 if active else 0,
            "_from": max(join, START),
            "_to": min(leave, END),
        })
    return drivers


WEEKDAY_FACTOR = [0.8, 0.82, 0.86, 0.95, 1.35, 1.5, 1.0]  # Mon..Sun


def hour_weights(weekday: int):
    """Requests by hour: commute peaks on weekdays, late-evening peaks on Fri/Sat."""
    w = [0.3] * 24
    for h in range(6, 23):
        w[h] = 1.0
    if weekday < 5:
        for h, v in {7: 2.2, 8: 2.8, 9: 1.6, 16: 1.6, 17: 2.6, 18: 2.4}.items():
            w[h] = v
    if weekday in (4, 5):  # Friday, Saturday nights
        for h, v in {19: 2.0, 20: 2.6, 21: 3.0, 22: 3.2, 23: 2.6, 0: 1.4, 1: 1.0}.items():
            w[h] = v
    return w


def trip_distance(rng, a, b):
    if a == b:
        km = rng.uniform(1.5, 6)
    elif "Airport" in (a, b):
        km = rng.uniform(11, 24)
    elif "CBD" in (a, b):
        km = rng.uniform(4, 12)
    else:
        km = rng.uniform(7, 18)
    return round(km, 1)


def make_trips(rng: random.Random, riders, drivers):
    trips = []
    first_trip_done: set[int] = set()
    for day in daterange(START, END):
        wd = day.weekday()
        expected = BASE_TRIPS_PER_DAY * WEEKDAY_FACTOR[wd]
        if WINTER_START <= day <= WINTER_END:
            expected *= 1.55
        if day.month == 12:
            expected *= 1.12
        n = max(0, round(rng.gauss(expected, expected ** 0.5)))

        eligible = [r for r in riders if r["_from"] <= day <= r["_to"]]
        drivers_today = [d for d in drivers if d["_from"] <= day <= d["_to"]]
        if not eligible or not drivers_today:
            continue
        weights = [r["_weight"] for r in eligible]
        hours = hour_weights(wd)

        for _ in range(n):
            rider = rng.choices(eligible, weights)[0]
            driver = rng.choice(drivers_today)
            hour = rng.choices(range(24), hours)[0]
            ts = datetime(day.year, day.month, day.day, hour, rng.randrange(60), rng.randrange(60))
            pickup = rider["home_zone"] if rng.random() < 0.55 else rng.choices(ZONES, ZONE_WEIGHTS)[0]
            dropoff = rng.choices(ZONES, ZONE_WEIGHTS)[0]

            late_weekend = wd in (4, 5) and (hour >= 21 or hour <= 1)
            r = rng.random()
            cancel_driver = 0.07 if late_weekend else 0.035
            status = "cancelled_rider" if r < 0.06 else "cancelled_driver" if r < 0.06 + cancel_driver else "completed"

            trip = {
                "rider_id": rider["rider_id"], "driver_id": driver["driver_id"],
                "requested_at": ts, "pickup_zone": pickup, "dropoff_zone": dropoff, "status": status,
                "distance_km": None, "duration_min": None, "fare_aud": None,
                "discount_aud": 0.0, "promo_id": None,
                "payment_method": "wallet" if rng.random() < 0.3 else "card",
                "rider_rating": None,
            }
            if status == "completed":
                km = trip_distance(rng, pickup, dropoff)
                peak = (wd < 5 and hour in (7, 8, 17, 18)) or late_weekend
                minutes = max(4, round(km * rng.uniform(1.8, 2.6) * (1.3 if peak else 1.0)))
                surge = 1.25 if late_weekend else 1.0
                fare = round((3.5 + 1.55 * km + 0.42 * minutes) * surge, 2)
                trip.update(distance_km=km, duration_min=minutes, fare_aud=fare)

                promo = None
                rid = rider["rider_id"]
                if rid not in first_trip_done and rider["signup_date"] >= "2025-01-01":
                    promo = PROMOS[0]
                elif WINTER_START <= day <= WINTER_END and fare >= PROMOS[1][6] and rng.random() < 0.7:
                    promo = PROMOS[1]
                elif day.month == 10 and wd == 4 and hour >= 18 and fare >= PROMOS[2][6] and rng.random() < 0.6:
                    promo = PROMOS[2]
                if promo:
                    trip.update(promo_id=promo[0], discount_aud=round(fare * promo[3] / 100, 2))
                first_trip_done.add(rid)

                if rng.random() < 0.7:
                    trip["rider_rating"] = rng.choices([1, 2, 3, 4, 5], [0.02, 0.03, 0.08, 0.27, 0.6])[0]
            trips.append(trip)

    trips.sort(key=lambda t: t["requested_at"])
    for i, t in enumerate(trips, 1):
        t["trip_id"] = i
        t["requested_at"] = t["requested_at"].strftime("%Y-%m-%d %H:%M:%S")
    return trips


def write_db(riders, drivers, trips):
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()
    con = sqlite3.connect(DB_PATH)
    for table, spec in SCHEMA.items():
        cols = ", ".join(f"{name} {typ}" for name, typ, _ in spec["columns"])
        con.execute(f"CREATE TABLE {table} ({cols})")

    def insert(table, rows):
        names = [c[0] for c in SCHEMA[table]["columns"]]
        con.executemany(
            f"INSERT INTO {table} ({', '.join(names)}) VALUES ({', '.join('?' * len(names))})",
            [[row[n] for n in names] for row in rows],
        )

    con.execute(
        "INSERT INTO about VALUES (?, ?, ?)",
        ("RideNest (fictional)", "All data in this database is made up for SQL practice. It does not describe any real company, person or trip.", "scripts/make_sql_dataset.py"),
    )
    insert("riders", riders)
    insert("drivers", drivers)
    con.executemany(
        "INSERT INTO promos VALUES (?, ?, ?, ?, ?, ?, ?)",
        [(p[0], p[1], p[2], p[3], p[4].isoformat(), p[5].isoformat(), p[6]) for p in PROMOS],
    )
    insert("trips", trips)
    con.execute("CREATE INDEX idx_trips_requested_at ON trips (requested_at)")
    con.execute("CREATE INDEX idx_trips_rider ON trips (rider_id)")
    con.commit()
    con.execute("VACUUM")
    con.close()


def write_docs(counts):
    lines = [
        "# RideNest SQL dataset (fictional)",
        "",
        "> **All data is made up.** RideNest is not a real company, and no row describes a real person or trip.",
        "> It exists for SQL practice on the `/sql` page.",
        "",
        "Generated by `scripts/make_sql_dataset.py` with a fixed random seed, so it is identical every time:",
        "",
        "```sh",
        "py -3 scripts/make_sql_dataset.py",
        "```",
        "",
        "Output: `public/sql/rideshare.sqlite` (SQLite). Period: 1 January to 31 December 2025.",
        "",
        "## Patterns built into the data",
        "",
        "- **Weekend peaks:** Friday and Saturday evenings are the busiest times; weekday mornings and evenings have commute peaks.",
        "- **Promo period:** `WINTER20` (20% off, 2 to 29 June 2025) lifts trip volume and new sign-ups.",
        "- **Churn:** some riders stop riding part-way through the year. Riders who signed up through the promo churn more often.",
        "- **Missing values:** cancelled trips have `NULL` distance, duration, fare and rating. Late Friday/Saturday requests are cancelled by drivers more often.",
        "",
        "## Tables",
        "",
    ]
    for table, spec in SCHEMA.items():
        lines += [f"### `{table}` ({counts[table]:,} rows)", "", spec["description"], "", "| Column | Type | Description |", "|---|---|---|"]
        for name, typ, desc in spec["columns"]:
            lines.append(f"| `{name}` | {typ.replace(' PRIMARY KEY', ' (primary key)')} | {desc} |")
        lines.append("")
    lines += [
        "## How the tables connect",
        "",
        "- `trips.rider_id` → `riders.rider_id`",
        "- `trips.driver_id` → `drivers.driver_id`",
        "- `trips.promo_id` → `promos.promo_id` (NULL when no promo was used)",
        "",
    ]
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main():
    rng = random.Random(SEED)
    riders = make_riders(rng)
    drivers = make_drivers(rng)
    trips = make_trips(rng, riders, drivers)
    write_db(riders, drivers, trips)
    counts = {"about": 1, "riders": len(riders), "drivers": len(drivers), "promos": len(PROMOS), "trips": len(trips)}
    write_docs(counts)
    size_kb = DB_PATH.stat().st_size / 1024
    print(f"Wrote {DB_PATH.relative_to(ROOT)} ({size_kb:.0f} KB): " + ", ".join(f"{k} {v:,}" for k, v in counts.items()))
    print(f"Wrote {DOC_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
