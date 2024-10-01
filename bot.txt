import asyncio
import logging
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

logging.basicConfig(level=logging.INFO)

bot = Bot(token='7804030886:AAFmqYAPW08gRlS6N6ASwqp5GXNPyifcS64')
dp = Dispatcher(storage=MemoryStorage())

class Form(StatesGroup):
    message = State()

last_message_time = {}

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Отправьте ваше предложение к посту NULL OWNS\n\nВы можете предложить пост по комьюнити BG, что там творится и т. д. (мы рассмотрим и возможно опубликуем в наш канал @nullowns)")
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

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
