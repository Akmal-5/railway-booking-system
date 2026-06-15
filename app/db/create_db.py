from app.db.config import engine , Base
from app.db.tickets import Tickets
from app.db.trains import Trains
from app.db.seats import Seats
from app.db.stations import Stations
from app.db.train_routes import TrainRoute

async def create_tables () :
    async with engine.begin() as con :
        await con.run_sync(Base.metadata.create_all)