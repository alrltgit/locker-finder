"""
Set up the database connection
"""
from sqlmodel import SQLModel, create_engine, Session
import os

DATABASE_URL = os.getenv("POSTGRES_URL")

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    return Session(engine)
