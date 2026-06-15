from app.db.config import Base
from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy import ForeignKey


class TrainRoute (Base) :
    
    __tablename__ = "train_routes"
    id : Mapped[int] = mapped_column(primary_key=True)
    train_id : Mapped[int] = mapped_column(ForeignKey("trains.id"))
    stations_id : Mapped[int] = mapped_column(ForeignKey("stations.id"))
    order : Mapped[int] = mapped_column()