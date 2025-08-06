from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, select, delete
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse
import sqlite3
from datetime import datetime

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLite engine for auth.db
auth_engine = create_engine("sqlite:///auth.db", echo=True)
metadata = MetaData()

# --- Define tables ---
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
metadata.create_all(auth_engine)

# --- Pydantic models ---
class RegionIn(BaseModel):
    Name: str

class LoginIn(BaseModel):
    UserName: str
    UserPassword: str

class SignupIn(BaseModel):
    UserName: str
    UserPassword: str

# ---------- API Endpoints ----------

@app.post("/nmm/addRegion")
async def add_region(region: RegionIn):
    try:
        with auth_engine.begin() as conn:
            conn.execute(region_table.insert().values(RegionName=region.Name))
        return JSONResponse(content={"message": "RegionAdded"}, status_code=201)
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
        return {"message": "RegionDeleted"}
    except SQLAlchemyError as e:
        print("DeleteRegion failed:", e)
        raise HTTPException(status_code=500, detail="RegionDeleteFailed")

@app.post("/validate")
async def login(credentials: LoginIn):
    try:
        conn = sqlite3.connect("details.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM details WHERE username=? AND password=?", (credentials.UserName, credentials.UserPassword))
        user = cursor.fetchone()

        if user:
            # update last_login timestamp
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("UPDATE details SET last_login = ? WHERE username = ?", (now, credentials.UserName))
            conn.commit()
            conn.close()
            return {"message": "SuccessLogin"}
        else:
            conn.close()
            return {"message": "FailureLogin"}
    except Exception as e:
        print("Login error:", e)
        raise HTTPException(status_code=500, detail="LoginFailed")

@app.post("/signup")
async def signup(user: SignupIn):
    try:
        conn = sqlite3.connect("details.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM details WHERE username=?", (user.UserName,))
        if cursor.fetchone():
            return JSONResponse(content={"message": "UserAlreadyExists"}, status_code=409)

        cursor.execute("INSERT INTO details (username, password) VALUES (?, ?)", (user.UserName, user.UserPassword))
        conn.commit()
        conn.close()
        return {"message": "SuccessSignup"}
    except Exception as e:
        print("Signup error:", e)
        raise HTTPException(status_code=500, detail="SignupFailed")

@app.get("/user/{username}/lastlogin")
async def get_last_login(username: str):
    try:
        conn = sqlite3.connect("details.db")
        cursor = conn.cursor()
        cursor.execute("SELECT last_login FROM details WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"username": username, "last_login": row[0]}
        else:
            raise HTTPException(status_code=404, detail="UserNotFoundOrNoLogin")
    except Exception as e:
        print("Error fetching last login:", e)
        raise HTTPException(status_code=500, detail="FetchFailed")


