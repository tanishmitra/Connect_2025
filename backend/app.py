from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Table, Column, String, MetaData, select
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLite DB connection
engine = create_engine('sqlite:///auth.db', echo=True)
metadata = MetaData()

# Define AuthTable schema
auth_table = Table('AuthTable', metadata,
                   Column('UserName', String, primary_key=True),
                   Column('UserPassword', String))

# Create the table if it doesn't exist
metadata.create_all(engine)

# Pydantic schema for input validation
class User(BaseModel):
    UserName: str
    UserPassword: str

# POST /signup endpoint
@app.post("/signup")
async def signup(user: User):
    try:
        with engine.begin() as conn:  # auto-commits
            conn.execute(auth_table.insert().values(
                UserName=user.UserName,
                UserPassword=user.UserPassword
            ))
        return JSONResponse(content={"Message": "SignupSuccess"}, status_code=201)

    except SQLAlchemyError as e:
        print("Signup failed:", e)
        return JSONResponse(content={"Message": "SignupFailed"}, status_code=500)

