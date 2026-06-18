from app.db.create_db import create_tables
from app.db.config import AsyncSessionmaker
from app.db.data_manipulation import create_trains , create_seats , create_stations , create_train_routes
from app.routers.trains_router import router as train_get_router
from app.routers.seats_router import router as seats_get_router
from app.routers.tickets_routers import router as tickets_get_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup () :
    await create_tables()
    
    async with AsyncSessionmaker() as session :
        trains = await create_trains(session)
        stations = await create_stations(session)
        
        for train in trains :
            await create_seats(session , train.id)
            await create_train_routes(session , train.id , stations)

app.include_router(train_get_router)
app.include_router(seats_get_router)
app.include_router(tickets_get_router)

if __name__ == "__main__" :
    # uvicorn.run("main:app" , reload=True) 
    uvicorn.run("main:app" , host="0.0.0.0", port=8000)