from app.db.trains import Trains
from app.db.seats import Seats
from app.db.stations import Stations
from app.db.train_routes import TrainRoute
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def create_trains (session : AsyncSession) :
    
    trains_list = ["Сапсан"]
    
    stmt = select(Trains).where(Trains.name.in_(trains_list))
    result = await session.execute(stmt)
    
    existing = result.scalars().all()
    existing_trains = [t.name for t in existing]
    
    new_trains = [
        Trains(name=name)
        for name in trains_list
        if name not in existing_trains
    ]
    
    if new_trains :
        session.add_all(new_trains)
        await session.commit()
        return  existing + new_trains
    
    return existing

async def create_seats (session : AsyncSession , train_id : int) :
    stmt = select(Seats).where(Seats.train_id == train_id)
    result = await session.execute(stmt)
    
    existing_seats = result.scalars().first()
    
    if existing_seats is not None :
        print(f"Места для поезда {train_id} уже существуте")
        return
    
    seats_to_add = []
    
    for i in range(1 , 13) :
        new_seats = Seats(
            train_id  = train_id,
            number = i
        )
        
        seats_to_add.append(new_seats)
        
    session.add_all(seats_to_add)
    await session.commit()
    
    
async def create_stations (session : AsyncSession) :
    
    stations_list = [
        "Москва" ,
        "Тверь",
        "Вышний Волочек",
        "Бологое",
        "Чудово",
        "Санкт-Петербург",
        "Великий Новгород"
    ]
    
    stmt = select(Stations).where(Stations.name.in_(stations_list))
    result = await session.execute(stmt)
    
    existing_station = result.scalars().all()
    existing_name = [s.name for s in existing_station]
    
    new_station = [
        Stations(name = name)
        for name in stations_list
        if name not in existing_name
    ]
    
    if new_station :
        session.add_all(new_station)
        await session.commit()
        return existing_station + new_station
    
    return existing_name

async def create_train_routes (session : AsyncSession , train_id , stations : list) :
    
    st = {
        s.name : s for s in stations
    }
    
    stmt = select(TrainRoute).where(TrainRoute.train_id == train_id)
    result = await session.execute(stmt)
    
    if result.scalars().first() is not None :
         return
     
    route = [
        TrainRoute(train_id=train_id , stations_id = st["Москва"].id , order=1),
        TrainRoute(train_id=train_id, stations_id=st["Тверь"].id, order=2),
        TrainRoute(train_id=train_id, stations_id=st["Вышний Волочек"].id, order=3),
        TrainRoute(train_id=train_id, stations_id=st["Бологое"].id, order=4),
        TrainRoute(train_id=train_id, stations_id=st["Чудово"].id, order=5),
        TrainRoute(train_id=train_id, stations_id=st["Санкт-Петербург"].id, order=6),
        TrainRoute(train_id=train_id, stations_id=st["Великий Новгород"].id, order=7)
    ]
    
    session.add_all(route)
    await session.commit()