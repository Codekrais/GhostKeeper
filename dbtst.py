from core_database.main_func import create_tables
import asyncio

from core_database.models import message
from core_database.work.crud import *

async def main():
    await create_tables()
asyncio.run(main())