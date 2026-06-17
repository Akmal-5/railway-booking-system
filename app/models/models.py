from pydantic import BaseModel


class TicketCreate (BaseModel) :
    seat_id : int
    from_station_id : int
    to_station_id : int 
    passenger_name : str