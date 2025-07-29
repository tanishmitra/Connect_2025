from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, select, delete
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse
import sqlite3

app = FastAPI()

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this to specific domain(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
auth_engine = create_engine("sqlite:///auth.db", echo=True)
metadata = MetaData()

# Define schema for auth.db
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

# Create all tables in auth.db if not already present
metadata.create_all(auth_engine)

# Pydantic input model for Region
class RegionIn(BaseModel):
    Name: str

# ---------- API Routes ----------

@app.post("/nmm/addRegion")
async def add_region(region: RegionIn):
    try:
        with auth_engine.begin() as conn:
            conn.execute(region_table.insert().values(RegionName=region.Name))
        return JSONResponse(content={"Message": "RegionAdded"}, status_code=201)
    except SQLAlchemyError as e:
        print("AddRegion failed:", e)
        raise HTTPException(status_code=500, detail="RegionAddFailed")

@app.delete("/nmm/deleteRegion/{region_id}")
async def delete_region(region_id: int):
    try:
        with auth_engine.begin() as conn:
            result = conn.execute(delete(region_table).where(region_table.c.RegionID == region_id))
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="RegionNotFound")
        return {"Message": "RegionDeleted"}
    except SQLAlchemyError as e:
        print("DeleteRegion failed:", e)
        raise HTTPException(status_code=500, detail="RegionDeleteFailed")

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        conn = sqlite3.connect("details.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM details WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return {"message": "Login successful"}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        print("Login error:", e)
        raise HTTPException(status_code=500, detail="Login failed")

