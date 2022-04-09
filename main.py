import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, utils, types
from aiogram.types import ParseMode
from config import TOKEN, URL
from db import process_search_model, init_db, find_id_search, find_all_cards
from parser_main import ParseSneakers

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="list")
async def send_list(message: types.Message):
    search_models = find_id_search(message.chat.id)
    cards = find_all_cards()

    for card in cards:
        card_title = card.title
        for search_model in search_models:
            search_title = search_model.title
            if card_title.find(search_model.title) >= 0:
                message_text = 'Строка поиска {} \r\n найдена {} найдена: '.format(search_title, utils.markdown.hlink(
                                                                                   card_title, card.url))
                await message.answer(text=message_text, parse_mode= ParseMode.HTML)


@dp.message_handler(commands="search")
async def send_search(message: types.Message):
    search_models = find_id_search(message.chat.id)
    for search_model in search_models:
        await message.answer(text=search_model.title)


@dp.message_handler()
async def echo(message: types.Message):
    # message_text = 'Serhc string {}'.format('789')
    await process_search_model(message)


async def scheduled(wait_for, parser_main):
    while True:
        await asyncio.sleep(wait_for)
        await parser_main.parse()


if __name__ == '__main__':
    init_db()
    parser = ParseSneakers(url=URL, bot=bot)
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(10, parser))
    executor.start_polling(dp, skip_updates=True)
