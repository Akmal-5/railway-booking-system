from typing import Annotated
from app.db.data_manipulation import buy_ticket
from app.models.models import TicketCreate
from app.Depends.create_session import create_session
from fastapi import APIRouter , Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/trains" , tags=["Tickets"])

@router.post("/{train_id}/tickets" ,
             summary="Покупка билета"
            )
async def buy_ticket_route(
    train_id : int,
    ticket_data : TicketCreate,
    session : Annotated[AsyncSession , Depends(create_session)]) :
    
    return await buy_ticket(session ,  train_id , ticket_data)