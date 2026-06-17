from app.db.trains import Trains
from app.db.seats import Seats
from app.db.stations import Stations
from app.db.train_routes import TrainRoute
from app.db.tickets import Tickets
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException , status

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
    
    return existing_station

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
    
async def get_all_trains (session : AsyncSession) :
    result = await  session.execute(select(Trains))
    return result.scalars().all()


async def get_train_route (session : AsyncSession , train_id : int) :
    
    train = await session.get(Trains , train_id)
    
    if not train :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,
                            detail="Поезд не найден"
                            )
    result = await session.execute(
        select(TrainRoute , Stations)
        .join(Stations , TrainRoute.stations_id == Stations.id)
        .where(TrainRoute.train_id == train_id)
        .order_by(TrainRoute.order)
    )
    
    rows = result.all()
    
    return [
        {
            "order" : route.order ,  "station_id" : station.id , "station_name" : station.name
        }
        for route , station in rows
    ]
    
async def get_available_seats (session : AsyncSession ,  train_id , from_station_id, to_station_id) :
    
    from_route = await session.execute(
        select(TrainRoute)
        .where(TrainRoute.train_id == train_id)
        .where(TrainRoute.stations_id == from_station_id)
    )
    from_route = from_route.scalar_one_or_none()
    
    to_route = await session.execute(
        select(TrainRoute)
        .where(TrainRoute.train_id == train_id)
        .where(TrainRoute.stations_id == to_station_id)
    )
    to_route = to_route.scalar_one_or_none()
    
    if not from_route or not to_route :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= "Станция не найдена в марщруте"
                            )
    
    from_order = from_route.order
    to_order = to_route.order
    
    if from_order >= to_order :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail= "Станция прибытия должна быть дальше по маршруту, чем станция отправления"
                            )
    
    seats_result = await session.execute(
        select(Seats).where(Seats.train_id == train_id)
    )
    all_seats = seats_result.scalars().all()
    
    
    seat_ids = [seat.id for seat in all_seats]
    
    
    tickets_result = await session.execute(
        select(Tickets).where(Tickets.seat_id.in_(seat_ids))
    )
    
    all_tickets = tickets_result.scalars().all()
     
    route_result = await session.execute(
        select(TrainRoute).where(TrainRoute.train_id == train_id)
    )
    
    order_by_station = {
        r.stations_id : r.order
        for r in route_result.scalars().all()
    }
    
    available  = []
    
    for seat in all_seats:
        busy = False
        
        for ticket in all_tickets :
            if ticket.seat_id != seat.id :
                continue
            
            ticket_from_order = order_by_station[ticket.from_station_id]
            ticket_to_order = order_by_station[ticket.to_station_id]
            
            if ticket_from_order < to_order and ticket_to_order > from_order:
                busy = True
                break
            
        if not busy :
            available.append(seat)
            
    return available