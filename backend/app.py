from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, select, delete
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLite database setup
engine = create_engine("sqlite:///auth.db", echo=True)
metadata = MetaData()

# Define tables
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

# Create tables if not exist
metadata.create_all(engine)

# Pydantic model for region input
class RegionIn(BaseModel):
    Name: str

#  Add Region
@app.post("/nmm/addRegion")
async def add_region(region: RegionIn):
    try:
        with engine.begin() as conn:
            conn.execute(region_table.insert().values(RegionName=region.Name))
        return JSONResponse(content={"Message": "RegionAdded"}, status_code=201)
    except SQLAlchemyError as e:
        print("AddRegion failed:", e)
        raise HTTPException(status_code=500, detail="RegionAddFailed")

#  Delete Region by ID
@app.delete("/nmm/deleteRegion/{region_id}")
async def delete_region(region_id: int):
    try:
        with engine.begin() as conn:
            result = conn.execute(delete(region_table).where(region_table.c.RegionID == region_id))
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="RegionNotFound")
        return {"Message": "RegionDeleted"}
    except SQLAlchemyError as e:
        print("DeleteRegion failed:", e)
        raise HTTPException(status_code=500, detail="RegionDeleteFailed")
