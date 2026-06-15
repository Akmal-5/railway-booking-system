from app.db.config import Base
from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy import ForeignKey , String


class Tickets (Base) :
    __tablename__ = "tickets"
    id : Mapped[int] = mapped_column(primary_key=True)
    seat_id : Mapped[int] = mapped_column(ForeignKey("seats.id"))
    from_station_id  : Mapped[int] = mapped_column(ForeignKey("stations.id"))
    to_station_id : Mapped[int] = mapped_column(ForeignKey("stations.id"))
    passenger_name : Mapped[str] = mapped_column(String(30))