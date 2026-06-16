from typing import Annotated
from app.db.data_manipulation import (get_all_trains , get_train_route)
from app.Depends.create_session import create_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter , Depends

router = APIRouter(prefix="/trains" , tags=['Trains'])

@router.get("/" ,
            summary="Список поездов"
            )
async def get_trains (session :  Annotated[AsyncSession , Depends(create_session)]) :
    return  await get_all_trains(session)
 
@router.get("{train_id}/route" ,
            summary="Маршрут поезда"
            )
async def train_route (train_id : int ,
                       session : Annotated[AsyncSession , Depends(create_session)]
                       ) :
    return get_train_route(session , train_id)