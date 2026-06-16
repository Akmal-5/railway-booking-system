from app.db.config import AsyncSessionmaker

async def create_session() :
    async with AsyncSessionmaker() as session :
        yield session