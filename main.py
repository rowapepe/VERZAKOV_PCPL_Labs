import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart, Command
from typing import Optional

import requests

from dotenv import load_dotenv
import os

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN_BOT2")
GIPHY_KEY = os.getenv("GIPHY_KEY")

if not TELEGRAM_TOKEN:
    raise RuntimeError("Не указан TELEGRAM_TOKEN")
if not GIPHY_KEY:
    raise RuntimeError("Не указан GIPHY_KEY")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


def get_random_gif(tag: str, rating: str) -> Optional[str]:
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
    
def get_gif(title: str) -> Optional[str]:
    url = "https://api.giphy.com/v1/gifs/search"
    params = {
        "api_key": GIPHY_KEY,
        "q": title,
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        gif_data = data.get("data")
        if gif_data:
            return gif_data[0]["images"]["original"]["url"]
        return None
    except (requests.RequestException, KeyError):
        return None


@dp.message(CommandStart())
async def start_command(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Рандомная гифка"), KeyboardButton(text="Найти гифку")]],resize_keyboard=True)
    await message.answer(
        text="Привет! Я бот, который может присылать тебе гифки. \n" \
        "Нажми кнопку ниже, чтобы получить гифку.",
        reply_markup=keyboard
    )
    

@dp.message(F.text == "Рандомная гифка")
async def send_gif(message: Message):
    gif_url = get_random_gif(tag="funny", rating="pg-13")
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Еще гифку", callback_data="more_gif")]])
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


@dp.message(Command("malkov"))
async def pashalka(message:Message):
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Рандомная гифка"), KeyboardButton(text="Найти гифку")]],resize_keyboard=True)
    await message.answer_animation(animation="https://media1.tenor.com/m/spgJsx_4cdoAAAAC/me-atrapaste-es-cine.gif", reply_markup=kb)


@dp.message(F.text == "Найти гифку")
async def find_gif(message: Message):
    await message.answer("Напиши название гифки, которую хочешь найти.")

@dp.message()
async def search_gif(message: Message):
    title = message.text
    gif_url = get_gif(title=title)
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Рандомная гифка"), KeyboardButton(text="Найти гифку")]],resize_keyboard=True)
    if gif_url:
        await message.answer_animation(animation=gif_url, reply_markup=kb)
    else:
        await message.answer("Извини, не удалось найти гифку по твоему запросу(", reply_markup=kb)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())