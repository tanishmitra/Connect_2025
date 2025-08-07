from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, select, delete, update
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse
import sqlite3
from datetime import datetime

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLite for auth & site/region/device
auth_engine = create_engine("sqlite:///auth.db", echo=True)
metadata = MetaData()

# ------------------- DB Table Definitions -------------------

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

network_element_table = Table(
    "NetworkElement", metadata,
    Column("NetworkElementID", Integer, primary_key=True, autoincrement=True),
    Column("ElementName", String, nullable=False),
    Column("ElementType", String, nullable=False),
    Column("IPAddress", String, nullable=False)
)

# Create all tables
metadata.create_all(auth_engine)

# ------------------- Models -------------------

class RegionIn(BaseModel):
    Name: str

class SiteIn(BaseModel):
    RegionID: int
    SiteName: str
    SiteStatus: str = "active"

class SiteUpdateIn(BaseModel):
    SiteName: str
    SiteStatus: str

class LoginIn(BaseModel):
    UserName: str
    UserPassword: str

class SignupIn(BaseModel):
    UserName: str
    UserPassword: str

class NetworkElementIn(BaseModel):
    ElementName: str
    ElementType: str
    IPAddress: str

class NetworkElementUpdate(BaseModel):
    ElementName: str
    ElementType: str
    IPAddress: str

# ------------------- Region APIs -------------------

@app.post("/regions")
async def add_region(region: RegionIn):
    try:
        with auth_engine.begin() as conn:
            conn.execute(region_table.insert().values(RegionName=region.Name))
        return JSONResponse(content={"message": "RegionAdded"}, status_code=201)
    except SQLAlchemyError as e:
        print("AddRegion failed:", e)
        raise HTTPException(status_code=500, detail="RegionAddFailed")

@app.delete("/regions/{region_id}")
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

# ------------------- Site APIs -------------------

@app.post("/Sites")
async def add_site(site: SiteIn):
    try:
        with auth_engine.begin() as conn:
            conn.execute(site_table.insert().values(
                RegionID=site.RegionID,
                SiteName=site.SiteName,
                SiteStatus=site.SiteStatus
            ))
        return JSONResponse(content={"message": "SiteAdded"}, status_code=201)
    except SQLAlchemyError as e:
        print("AddSite failed:", e)
        raise HTTPException(status_code=500, detail="SiteAddFailed")

@app.get("/sites")
async def get_sites():
    try:
        with auth_engine.connect() as conn:
            result = conn.execute(select(site_table)).fetchall()
            sites = [dict(row._mapping) for row in result]
        return sites
    except SQLAlchemyError as e:
        print("GetSites failed:", e)
        raise HTTPException(status_code=500, detail="SiteFetchFailed")

@app.put("/sites/{site_id}")
async def update_site(site_id: int, site: SiteUpdateIn):
    try:
        with auth_engine.begin() as conn:
            result = conn.execute(update(site_table).where(site_table.c.SiteID == site_id).values(
                SiteName=site.SiteName,
                SiteStatus=site.SiteStatus
            ))
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="SiteNotFound")
        return {"message": "SiteUpdated"}
    except SQLAlchemyError as e:
        print("UpdateSite failed:", e)
        raise HTTPException(status_code=500, detail="SiteUpdateFailed")

@app.delete("/sites/{site_id}")
async def delete_site(site_id: int):
    try:
        with auth_engine.begin() as conn:
            result = conn.execute(delete(site_table).where(site_table.c.SiteID == site_id))
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="SiteNotFound")
        return {"message": "SiteDeleted"}
    except SQLAlchemyError as e:
        print("DeleteSite failed:", e)
        raise HTTPException(status_code=500, detail="SiteDeleteFailed")

# ------------------- Auth APIs -------------------

@app.post("/validate")
async def login(credentials: LoginIn):
    try:
        conn = sqlite3.connect("details.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM details WHERE username=? AND password=?", (credentials.UserName, credentials.UserPassword))
        user = cursor.fetchone()

        if user:
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

# ------------------- Network Element APIs -------------------

@app.get("/network-elements")
async def list_network_elements():
    try:
        with auth_engine.connect() as conn:
            result = conn.execute(select(network_element_table)).fetchall()
            elements = [dict(row._mapping) for row in result]
        return elements
    except SQLAlchemyError as e:
        print("List Network Elements failed:", e)
        raise HTTPException(status_code=500, detail="ListFailed")

@app.post("/network-elements")
async def add_network_element(element: NetworkElementIn):
    try:
        with auth_engine.begin() as conn:
            conn.execute(network_element_table.insert().values(
                ElementName=element.ElementName,
                ElementType=element.ElementType,
                IPAddress=element.IPAddress
            ))
        return {"message": "NetworkElementAdded"}
    except SQLAlchemyError as e:
        print("Add Network Element failed:", e)
        raise HTTPException(status_code=500, detail="AddFailed")

@app.put("/network-elements/{element_id}")
async def update_network_element(element_id: int, element: NetworkElementUpdate):
    try:
        with auth_engine.begin() as conn:
            result = conn.execute(update(network_element_table).where(
                network_element_table.c.NetworkElementID == element_id
            ).values(
                ElementName=element.ElementName,
                ElementType=element.ElementType,
                IPAddress=element.IPAddress
            ))
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="ElementNotFound")
        return {"message": "NetworkElementUpdated"}
    except SQLAlchemyError as e:
        print("Update Network Element failed:", e)
        raise HTTPException(status_code=500, detail="UpdateFailed")

@app.delete("/network-elements/{element_id}")
async def delete_network_element(element_id: int):
    try:
        with auth_engine.begin() as conn:
            result = conn.execute(delete(network_element_table).where(
                network_element_table.c.NetworkElementID == element_id
            ))
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="ElementNotFound")
        return {"message": "NetworkElementDeleted"}
    except SQLAlchemyError as e:
        print("Delete Network Element failed:", e)
        raise HTTPException(status_code=500, detail="DeleteFailed")
