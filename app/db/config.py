import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession , create_async_engine 
from sqlalchemy.orm import DeclarativeBase , sessionmaker

load_dotenv()

engine = create_async_engine(
    url = os.getenv("DATABASE_URL"),
    echo = False
)

AsyncSessionmaker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
) 

class Base (DeclarativeBase) :
    pass