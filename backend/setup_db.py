import sqlite3
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, select

# --- Setup Login DB (details.db) ---
def setup_login_db():
    conn = sqlite3.connect("details.db")
    cursor = conn.cursor()

    # Check if 'details' table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='details'")
    table_exists = cursor.fetchone()

    if table_exists:
        # Check if last_login column exists
        cursor.execute("PRAGMA table_info(details)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'last_login' not in columns:
            cursor.execute("ALTER TABLE details ADD COLUMN last_login TEXT")
            print("Added 'last_login' column to details table.")
    else:
        # Create new table with last_login
        cursor.execute("""
            CREATE TABLE details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT,
                last_login TEXT
            )
        """)
        print("Created new details table with last_login column.")

    # Insert default admin user if not present
    cursor.execute("SELECT * FROM details WHERE username = ?", ("admin",))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO details (username, password, last_login) VALUES (?, ?, ?)", ("admin", "admin123", ""))
        print("Inserted default login user: admin / admin123")

    conn.commit()
    conn.close()


# --- Setup Auth DB (auth.db) ---
def setup_auth_db():
    engine = create_engine("sqlite:///auth.db", echo=True)
    metadata = MetaData()

    region_table = Table(
        "Region", metadata,
        Column("RegionID", Integer, primary_key=True, autoincrement=True),
        Column("RegionName", String, unique=True, nullable=False)
    )

    site_table = Table(
        "Site", metadata,
        Column("SiteID", Integer, primary_key=True, autoincrement=True),
        Column("RegionID", Integer, ForeignKey("Region.RegionID", ondelete="CASCADE"), nullable=False),
        Column("SiteName", String, nullable=False),
        Column("SiteStatus", String, default="active")
    )

    device_table = Table(
        "Device", metadata,
        Column("IP", String, primary_key=True),
        Column("SiteID", Integer, ForeignKey("Site.SiteID", ondelete="CASCADE"), nullable=False)
    )

    metadata.create_all(engine)

    with engine.begin() as conn:
        # Add initial regions
        region_names = ["North", "South"]
        region_ids = {}

        for name in region_names:
            result = conn.execute(select(region_table).where(region_table.c.RegionName == name)).fetchone()
            if not result:
                conn.execute(region_table.insert().values(RegionName=name))
                print(f"Inserted Region: {name}")
            result = conn.execute(select(region_table).where(region_table.c.RegionName == name)).fetchone()
            region_ids[name] = result.RegionID

        # Add sample sites
        sites = [
            {"SiteName": "NorthSiteA", "Region": "North", "SiteStatus": "active"},
            {"SiteName": "SouthSiteB", "Region": "South", "SiteStatus": "inactive"}
        ]
        site_ids = {}

        for site in sites:
            region_id = region_ids[site["Region"]]
            result = conn.execute(select(site_table).where(site_table.c.SiteName == site["SiteName"])).fetchone()
            if not result:
                conn.execute(site_table.insert().values(
                    SiteName=site["SiteName"],
                    RegionID=region_id,
                    SiteStatus=site["SiteStatus"]
                ))
                print(f"Inserted Site: {site['SiteName']}")
            result = conn.execute(select(site_table).where(site_table.c.SiteName == site["SiteName"])).fetchone()
            site_ids[site["SiteName"]] = result.SiteID

        # Add sample devices
        devices = [
            {"IP": "192.168.1.1", "SiteName": "NorthSiteA"},
            {"IP": "192.168.1.2", "SiteName": "SouthSiteB"}
        ]

        for device in devices:
            site_id = site_ids[device["SiteName"]]
            result = conn.execute(select(device_table).where(device_table.c.IP == device["IP"])).fetchone()
            if not result:
                conn.execute(device_table.insert().values(IP=device["IP"], SiteID=site_id))
                print(f"Inserted Device: {device['IP']}")

    print("Auth DB setup complete.")


# --- Run both setups ---
if __name__ == "__main__":
    setup_login_db()
    setup_auth_db()


# --- Run both setups ---
if __name__ == "__main__":
    setup_login_db()
    setup_auth_db()

