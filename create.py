from core_database.main_func import create_tables
import asyncio

async def main():
    await create_tables()
asyncio.run(main())