from app.database.models import async_session
from app.database.models import User, Purchase
from sqlalchemy import select
from datetime import datetime, timedelta


async def get_users():
    async with async_session() as session:
        return await session.scalars(select(User))


async def set_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def today(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            print('пользователь не найден')
            return

        return (await session.scalars(select(Purchase).where(Purchase.created_at > datetime.now() - timedelta(days=1), Purchase.user_id == user.id))).all()

async def week(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            print('пользователь не найден')
            return

        return (await session.scalars(select(Purchase).where(Purchase.created_at > datetime.now() - timedelta(days=7), Purchase.user_id == user.id))).all()

async def month(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            print('пользователь не найден')
            return

        return (await session.scalars(select(Purchase).where(Purchase.created_at > datetime.now() - timedelta(days=30), Purchase.user_id == user.id))).all()

async def create_purchase(title, price, tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            print('пользователь не найден')

        purchase = Purchase(title=title, price=price, user_id=user.id, created_at=datetime.now())

        session.add(purchase)
        await session.commit()