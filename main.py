import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart
from typing import Optional

import requests

from dotenv import load_dotenv
import os

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GIPHY_KEY = os.getenv("GIPHY_KEY")

if not TELEGRAM_TOKEN:
    raise RuntimeError("Не указан TELEGRAM_TOKEN")
if not GIPHY_KEY:
    raise RuntimeError("Не указан GIPHY_KEY")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


def get_random_gif(tag: str = "", rating: str = "pg-13") -> Optional[str]:
    url = "https://api.giphy.com/v1/gifs/random"
    params = {
        "api_key": GIPHY_KEY,
        "tag": tag,
        "rating": rating
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        gif_data = data.get("data")
        return gif_data["images"]["original"]["url"]
    except (requests.RequestException, KeyError):
        return None

@dp.message(CommandStart())
async def start_command(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Прислать гифку")]],resize_keyboard=True)
    await message.answer(
        text="Привет! Я бот, который может присылать тебе гифки. \n" \
        "Нажми кнопку ниже, чтобы получить гифку.",
        reply_markup=keyboard
    )
    
@dp.message(F.text == "Прислать гифку")
async def send_gif(message: Message):
    gif_url = get_random_gif(tag="funny", rating="pg-13")
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Еще гифку", callback_data="more_gif")]]
    )
    if gif_url:
        await message.answer_animation(animation=gif_url, reply_markup=kb)
    else:
        await message.answer("Извини, не удалось получить гифку(")

@dp.callback_query(F.data == "more_gif")
async def more_gif(callback: CallbackQuery):
    gif_url = get_random_gif(tag="funny", rating="pg-13")
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Еще гифку", callback_data="more_gif")]])
    if gif_url:
        await callback.message.answer_animation(animation=gif_url, reply_markup=kb)
    else:
        await callback.message.answer("Извини, не удалось получить гифку(")
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())