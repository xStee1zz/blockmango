import asyncio
import logging
from datetime import datetime, timedelta
import random

import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

logging.basicConfig(level=logging.INFO)

bot = Bot(token='7804030886:AAFmqYAPW08gRlS6N6ASwqp5GXNPyifcS64')
dp = Dispatcher(storage=MemoryStorage())

class Form(StatesGroup):
    message = State()
    user_id = State()

last_message_time = {}

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Отправьте ваше предложение к посту NULL OWNS\n\nВы можете предложить пост по комьюнити BG, что там творится и т. д. (мы рассмотрим и возможно опубликуем в наш канал @nullowns)\n\n«в чате @darkgo_official имеется функция спама в друзья»")
    await state.set_state(Form.message)

@dp.message(Form.message)
async def message_handler(message: Message, state: FSMContext):
    user_id_send = "6278506570"
    user_id = message.from_user.id
    current_time = datetime.now()

    if message.text or message.voice:
        if user_id in last_message_time:
            last_time = last_message_time[user_id]
            time_diff = current_time - last_time
            if time_diff < timedelta(minutes=5):
                remaining_time = timedelta(minutes=5) - time_diff
                minutes, seconds = divmod(remaining_time.seconds, 60)
                await message.answer(f"Вы можете отправлять предложения раз в 5 минут\n\nОсталось {minutes} минут {seconds} секунд")
                return
        last_message_time[user_id] = current_time

    if message.text:
        text = f"by tg://openmessage?user_id={message.from_user.id}\n\n{message.text}"
        await bot.send_message(user_id_send, text)
        await message.answer("Ваше предложение было успешно отправлено (чтобы отправить еще предложение, введите /start)")
    elif message.voice:
        await bot.send_voice(user_id_send, voice=message.voice.file_id, caption=f"by tg://openmessage?user_id={message.from_user.id}")
        await message.answer("Ваше предложение было успешно отправлено (чтобы отправить еще предложение, введите /start)")
    else:
        await message.answer("Я принимаю только сообщения и голосовые сообщения (введите /start чтобы повторить попытку)")
    await state.clear()

def get_bots():
    url = "https://raw.githubusercontent.com/xStee1zz/blockmango/refs/heads/main/bot.txt"
    response = requests.get(url)
    return response.text

def send_post_request(data: dict, headers: dict):
    url = "https://gw.sandboxol.com/friend/api/v1/friends"
    response = requests.post(url, headers=headers, json=data).json()
    return response

@dp.message(Command("spam"))
async def spam(message: Message, state: FSMContext):
    if message.chat.type in ["group", "supergroup"]:
        await message.answer("Введите ID игрока")
        await state.set_state(Form.user_id)
    else:
        await message.answer("Команда доступна в чате @darkgo_official")

@dp.message(Form.user_id)
async def spam_send(message: Message, state: FSMContext):
    player_id = message.text

    bot_list_text = get_bots()
    bot_list = bot_list_text.splitlines()

    success_count = 0

    for _ in range(30):
        random_bot = random.choice(bot_list)
        bot_id, bot_token = random_bot.split(":")

        data = {
            "friendId": player_id,
            "msg": ""
        }

        headers = {
            "userId": bot_id,
            "Access-Token": bot_token,
            "User-Agent": "okhttp/3.12.1"
        }

        response_text = send_post_request(data, headers)

        if response_text['message'] == "SUCCESS":
            success_count += 1

    await message.answer(f"Отправлено {success_count} заявок\n\nВозможные проблемы:\n • Заявки заполнены\n • Заявки отключены\n • Неверный ID")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
