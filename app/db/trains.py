from app.db.config import Base
from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy import String 

class Trains (Base) :
    __tablename__ = "trains"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(20) , unique=True)