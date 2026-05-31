from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import selectinload

from core_database.models import Message, User
from core_database.models import db_helper
from sqlalchemy.exc import SQLAlchemyError

def connection(func):
    async def wrapper(*args, **kwargs):
        async with db_helper.Session_factory() as session:
            try:
                return await func(session, *args, **kwargs)
            except SQLAlchemyError as e:
                print(f"Ошибка: {e}")
                await session.rollback()
    return wrapper

@connection
async def get_messages(session: AsyncSession) -> list[Message]:
    stmt = select(Message).order_by(Message.message_id).options(selectinload(Message.user))
    result: Result = await session.execute(stmt)
    messages = result.scalars().all()
    return list(messages)

@connection
async def get_message(session: AsyncSession, message_id: int) -> Message | None:
    stmt = select(Message).where(Message.message_id == message_id).options(selectinload(Message.user))
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

@connection
async def create_message(session, **kwargs) -> Message | None:
    message = await session.scalar(select(Message).filter_by(message_id=kwargs.get('message_id')))
    new_message = Message(**kwargs)
    if not message:
        session.add(new_message)
        await session.commit()
        # await session.refresh(new_message)
        print(f"Сообщение {kwargs.get('message_id')} создано\n")
        return message
    else:
        message.text = kwargs.get('text')
        await session.commit()
        print(f"Сообщение {kwargs.get('message_id')} обновлено\n")
        return message

@connection
async def delete_message(session, **kwargs) -> Message | None:
    message_id = kwargs.get('message_id')
    if not message_id:
        print(f"Сообщение {kwargs.get('message_id')} не найдено\n")
        return None
    message = await session.scalar(select(Message).filter_by(message_id=message_id))
    if message:
        await session.delete(message)
        await session.commit()
        print(f"Сообщение {kwargs.get('message_id')} удалено\n")
        return message
    return None

@connection
async def create_user(session, **kwargs) -> User | None:
    user = await session.scalar(select(User).filter_by(tg_id=kwargs.get('tg_id')))
    if not user:
        new_user = User(**kwargs)
        session.add(new_user)
        await session.commit()
        # await session.refresh(new_message)
        print(f"Пользователь {kwargs.get('tg_id')} добавлен\n")
        return user

    else:
        user.username = kwargs.get('username')
        user.fullname = kwargs.get('fullname')
        print(f"Пользователь {kwargs.get('tg_id')} обновлен\n")
        await session.commit()

@connection
async def get_user(session: AsyncSession, tg_id: int) -> User| None:
    stmt = select(User).where(User.tg_id == tg_id).options(selectinload(User.messages))
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

@connection
async def get_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.tg_id).options(selectinload(User.messages))
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)




