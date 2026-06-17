from typing import Annotated
from app.db.data_manipulation import get_available_seats
from app.Depends.create_session import create_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter , Depends

router = APIRouter(prefix = "/trains" , tags=["Места"])

@router.get("{train_id}/seats")

async def available_seats(
    train_id :  int,
    from_station_id : int,
    to_station_id : int,
    session : Annotated[AsyncSession , Depends(create_session)]
    ) :
    
    return await get_available_seats(session ,  train_id , from_station_id , to_station_id)