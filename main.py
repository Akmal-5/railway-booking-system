from app.db.create_db import create_tables
from app.db.config import AsyncSessionmaker
from app.db.data_manipulation import create_trains , create_seats , create_stations , create_train_routes
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.on_event("startup")
async def startup () :
    await create_tables()
    
    async with AsyncSessionmaker() as session :
        trains = await create_trains(session)
        stations = await create_stations(session)
        
        for train in trains :
            await create_seats(session , train.id)
            await create_train_routes(session , train.id , stations)
    
if __name__ == "__main__" :
    uvicorn.run("main:app" , reload=True)    