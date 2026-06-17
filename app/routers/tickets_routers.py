from typing import Annotated
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
    
    pass