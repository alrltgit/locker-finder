from typing import Optional
from sqlmodel import Field, SQLModel

class Lockers(SQLModel, table=True):
    __tablename__ = "lockers"
    __table_args__ = { "schema": "locker_finder" }

    id: Optional[str] = Field(default=None, primary_key=True)
    external_href: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None, unique=True)
    type: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)
    physical_type: Optional[str] = Field(default=None)
    lat: Optional[float] = Field(default=None)
    lon: Optional[float] = Field(default=None)
    address_line1: Optional[str] = Field(default=None)
    address_line2: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    province: Optional[str] = Field(default=None)
    post_code: Optional[str] = Field(default=None)
    open_hours: Optional[str] = Field(default=None)
    is_24_7: Optional[str] = Field(default=None)
