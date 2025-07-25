from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, select

# Connect to the SQLite DB
engine = create_engine('sqlite:///auth.db', echo=True)
metadata = MetaData()

# Define updated tables
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

# Create tables if they don’t exist
metadata.create_all(engine)

# Begin seeding
with engine.begin() as conn:

    # 1. Insert Regions if not exist
    region_names = ["North", "South"]
    region_ids = {}

    for name in region_names:
        result = conn.execute(select(region_table).where(region_table.c.RegionName == name)).fetchone()
        if not result:
            conn.execute(region_table.insert().values(RegionName=name))
            print(f"Inserted Region: {name}")
        result = conn.execute(select(region_table).where(region_table.c.RegionName == name)).fetchone()
        region_ids[name] = result.RegionID

    # 2. Insert Sites
    sites = [
        {"SiteName": "NorthSiteA", "Region": "North", "SiteStatus": "active"},
        {"SiteName": "SouthSiteB", "Region": "South", "SiteStatus": "maintenance"}
    ]

    site_ids = {}

    for site in sites:
        region_id = region_ids[site["Region"]]
        result = conn.execute(select(site_table).where(site_table.c.SiteName == site["SiteName"])).fetchone()
        if not result:
            conn.execute(site_table.insert().values(SiteName=site["SiteName"], RegionID=region_id, SiteStatus=site["SiteStatus"]))
            print(f"Inserted Site: {site['SiteName']}")
        result = conn.execute(select(site_table).where(site_table.c.SiteName == site["SiteName"])).fetchone()
        site_ids[site["SiteName"]] = result.SiteID

    # 3. Insert Devices
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

print("Seeding complete.")
