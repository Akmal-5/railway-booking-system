from app.db.config import Base
from sqlalchemy.orm import Mapped ,mapped_column
from sqlalchemy import ForeignKey

class Seats (Base) :
    
    __tablename__ = "seats"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    train_id : Mapped[int] = mapped_column(ForeignKey("trains.id"))
    number : Mapped[int] = mapped_column()    