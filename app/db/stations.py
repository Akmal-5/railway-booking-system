from app.db.config import Base
from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy import String


class Stations (Base) :
    __tablename__ = "stations"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(50) , unique=True)