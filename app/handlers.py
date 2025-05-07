from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from datetime import datetime
from collections import defaultdict

from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

router = Router()


@router.message(CommandStart())
async def start(msg: Message):
    await rq.set_user(tg_id=msg.from_user.id)
    await msg.answer('Добро пожаловать в бота для управления покупками')

@router.message(Command('add'))
async def add(msg: Message):
    if msg.text.count(' ') < 2:
        await msg.answer('Недостаточно информации для расхода\nПример:/add 250 Транспорт')
        return
    price = int(msg.text.split(' ')[1])
    title = ' '.join(msg.text.split(' ')[2:])

    await rq.create_purchase(title, price, tg_id=msg.from_user.id)

    await msg.answer(f'✅ Добавлено: {price}₽ - {title}')

@router.message(Command('today'))
async def add(msg: Message):

    purchases = await rq.today(tg_id=msg.from_user.id)

    if len(purchases) == 0:
        await msg.answer('сегодня не было трат')
    else:
        result = 'Сегодняшние траты:\n\n'
        total_price = 0

        for purchase in purchases:
            result += f'{purchase.price}₽ - {purchase.title}\n'
            total_price += purchase.price
        result += f'\nИтого: {total_price}₽'

        await msg.answer(result)

@router.message(Command('week'))
async def add(msg: Message):

    purchases = await rq.week(tg_id=msg.from_user.id)

    if len(purchases) == 0:
        await msg.answer('За всю неделю не было трат')
    else:
        total_price = 0
        purchases_by_date = defaultdict(list)

        for p in purchases:
            date_str = p.created_at.strftime('%-d %B')
            purchases_by_date[date_str].append(p)
            total_price += p.price

        result = ''
        for date in sorted(purchases_by_date.keys(), key=lambda d: datetime.strptime(d, '%d %B')):
            result += f'{date}\n'

            for p in purchases_by_date[date]:
                result += f'{p.price}₽ - {p.title}\n'
            result += '\n'

        result += f'Итого: {total_price}₽'
        await msg.answer(result)


@router.message(Command('month'))
async def add(msg: Message):

    purchases = await rq.month(tg_id=msg.from_user.id)

    if len(purchases) == 0:
        await msg.answer('За весь месяц не было трат')
    else:
        total_price = 0
        purchases_by_date = defaultdict(list)

        for p in purchases:
            date_str = p.created_at.strftime('%-d %B')
            purchases_by_date[date_str].append(p)
            total_price += p.price

        result = ''
        for date in sorted(purchases_by_date.keys(), key=lambda d: datetime.strptime(d, '%d %B')):
            result += f'{date}\n'

            for p in purchases_by_date[date]:
                result += f'{p.price}₽ - {p.title}\n'
            result += '\n'

        result += f'Итого: {total_price}₽'
        await msg.answer(result)