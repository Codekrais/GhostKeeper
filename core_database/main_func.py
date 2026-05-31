from .models import db_helper, Base

async def create_tables():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

