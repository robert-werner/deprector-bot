import aiofiles
from aiogram import types
from aiogram.utils import executor
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from bot import dp, bot
import deprector as deprector

from config import DATABASE_URI


async def write_result(speech, is_depression):
    engine = create_async_engine(DATABASE_URI)
    async with engine.connect() as conn:
        async with aiofiles.open('./deprector_bot/sql/insert_result.sql', 'r', encoding='utf-8') as f:
            insert_result = await f.read()
        is_depression = 'TRUE' if is_depression else 'FALSE'
        speech = f"'{speech}'"
        insert_result = insert_result.format(speech=speech, is_depression=is_depression)
        await conn.execute(text(insert_result))
        await conn.commit()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply('''
    Здравствуйте! Я бот центра ментального здоровья "Эмпатия". 
    
    Моя функция - помочь распознавать Вам признаки депрессии у себя, основываясь на вашем описании своего состояния.
    
    Все данные, поступающие в бот лишены какой-либо идентификации, позволяющие опознать Вас.
    Данные могут быть использованы для улучшения точности бота.
    
    *ВНИМАНИЕ! Использование бота не отменяет визитов к врачу!*
    ''', parse_mode='Markdown')


@dp.message_handler()
async def echo(message: types.Message):
    speech = message.text
    is_depression = deprector.deprect(speech)
    await write_result(speech, is_depression)
    if is_depression:
        await bot.send_message(chat_id=message.chat.id, text=f'''
        В вашем сообщении определены признаки депрессии. 
        Рекомендуем записаться к врачу-психиатру на сайте https://empathycenter.ru/
        ''')
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text='В Вашем сообщении не было определено признаков депрессии. Так держать! =)')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
