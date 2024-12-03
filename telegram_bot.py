import asyncio
import logging
from aiogram import Bot, Dispatcher, types, html
from aiogram import F
from aiogram.filters.command import Command, CommandStart, CommandObject
from aiogram.utils.formatting import Bold
from aiogram.types import Message, Update
import config
from API import API



logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def command_start(message: Message, command: CommandObject) -> None:
    """
    Обработчик команды старт
    """
    token = command.args if command.args else None  # Получаем аргументы команды

    if token is None:
        await message.answer(
            f"Привет, *{message.from_user.full_name}* 👋 \n"
            "Кажется, что-то пошло не так, попробуй зарегистрироваться заново",
            parse_mode="Markdown"
        )
        return  # Завершаем выполнение функции

    data = {
        "token": str(token),
        "telegram_id": str(message.from_user.id),
        "username": str(message.from_user.username),
        "full_name": str(message.from_user.full_name)
    }
    try:
        sender = API.merge_telegram(data)
    except Exception as e:
        logging.error(f"Error: {e}")
        await message.answer(
            f"Привет, *{message.from_user.full_name}* 👋 \n"
            "Кажется, что-то пошло не так, попробуй зарегистрироваться заново",
            parse_mode="Markdown"
        )
        return

    if sender == 200:
        button = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
        keyboard = types.ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True, one_time_keyboard=True)
        await message.answer(
            f"Привет, *{message.from_user.full_name}* 👋 \n"
            "Ты успешно привязал свой телеграм к личному кабинету! \n"
            "Теперь ты можешь поделиться с нами номером телефона, чтобы получать бонусные баллы.",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    elif sender == 400:
        await message.answer(
            "Упс, кажется, время регистрации истекло. Перейди на сайт и зарегистрируйся заново.",
            parse_mode="Markdown"
        )


@dp.message(F.content_type == 'contact')
async def handle_contact(message: types.Message):
    """
    Обработчик для контактов, полученных от пользователя
    """
    data = {
        "telegram_id": str(message.from_user.id),
        "phone": str(message.contact.phone_number)
    }
    sender = API.merge_phone(data)
    if sender == 200:
        await message.answer(f"Ваш номер телефона: *{message.contact.phone_number}* - успешно зарегистрирован!", parse_mode="Markdown")
    if sender == 400:
        await message.answer(f"Ваш номер телефона: *{message.contact.phone_number}* - уже зарегистрирован!", parse_mode="Markdown")
    if sender == 500:
        await message.answer(f"Упс, что-то пошло не так, попробуйте позже.", parse_mode="Markdown")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())