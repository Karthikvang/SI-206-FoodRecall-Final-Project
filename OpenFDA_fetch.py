import requests
import sqlite3

API_KEY = "xmlDEL0okHlfnLCqKDM4Pj0LhxeE2u44lZ6dnh1O"

def get_recall_data(api_key, start_date, end_date, limit=25):
    base_url = "https://api.fda.gov/food/enforcement.json"
    search_query = f"recall_initiation_date:[{start_date} TO {end_date}]"
    params = {
        "api_key": api_key,
        "search":  search_query,
        "limit":   limit * 4 
    }
    resp = requests.get(base_url, params=params)
    return resp.json().get("results", []) if resp.ok else []

def create_recall_table(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # States table to avoid repeating values
    cur.execute("""
      CREATE TABLE IF NOT EXISTS states (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        abbreviation TEXT UNIQUE
      )
    """)

    # Create recalls table
    cur.execute("""
      CREATE TABLE IF NOT EXISTS food_recalls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recall_number TEXT UNIQUE,
        product_description TEXT,
        recall_initiation_month INTEGER,
        state_id INTEGER,
        FOREIGN KEY (state_id) REFERENCES states(id)
      )
    """)
    conn.commit()
    conn.close()

def insert_recall_data(db, data, limit=25):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    inserted = 0

    for r in data:
        if inserted >= limit:
            break

        rn = r.get("recall_number")
        state_abbr = r.get("state")

        # Skip if recall already exists
        cur.execute("SELECT 1 FROM food_recalls WHERE recall_number = ?", (rn,))
        if cur.fetchone():
            continue

        # Insert state if it doesn't exist and fetch its id
        cur.execute("SELECT id FROM states WHERE abbreviation = ?", (state_abbr,))
        row = cur.fetchone()
        if row:
            state_id = row[0]
        else:
            cur.execute("INSERT INTO states (abbreviation) VALUES (?)", (state_abbr,))
            state_id = cur.lastrowid

        # Insert the recall
        cur.execute("""
          INSERT INTO food_recalls (
            recall_number,
            product_description,
            recall_initiation_month,
            state_id
          ) VALUES (?, ?, ?, ?)
        """, (
          rn,
          r.get("product_description"),
          int(r["recall_initiation_date"][4:6]),
          state_id
        ))

        if cur.rowcount == 1:
            inserted += 1

    conn.commit()
    conn.close()
    print(f"{inserted} new recalls inserted this run.")

def main():
        create_recall_table("FoodRecall.db")

        seasons = [
        ("20241202", "20250301"),  # winter
        ("20240302", "20240601"),  # spring
        ("20240602", "20240901"),  # summer
        ("20240902", "20241201"),  # fall
    ]

        all_recalls = []
        for start, end in seasons:
            batch = get_recall_data(API_KEY, start, end, limit=25)
            if batch:
                all_recalls.extend(batch)

        insert_recall_data("FoodRecall.db", all_recalls)

if __name__ == "__main__":
        main()