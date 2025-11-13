import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv
import os
import json
from pathlib import Path

class HomeworkStates(StatesGroup):
    waiting_for_homework = State()
    editing_homework = State()

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN_BOT1")

if not TELEGRAM_TOKEN:
    raise RuntimeError("Не указан TELEGRAM_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

main_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Добавить домашнее задание'), KeyboardButton(text='Просмотр домашнее задание')]],
    resize_keyboard=True
)

DATA_FILE = Path(__file__).parent / "homeworks.json"

def load_homeworks():
    if DATA_FILE.exists():
        try:
            with DATA_FILE.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_homeworks(data):
    try:
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

homeworks = load_homeworks()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        'Приветствую в боте пользователя @rowapepe! \nДля начала нажми на интересующие кнопки над клавиатурой',
        reply_markup=main_kb
    )

@dp.message(F.text == 'Добавить домашнее задание')
async def add_homework(message: Message, state: FSMContext):
    await state.set_state(HomeworkStates.waiting_for_homework)

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Отмена')]],
        resize_keyboard=True
    )
    
    await message.answer(
        "Напиши твое домашнее задание в следующем формате:\n"
        "<название предмета>: <описание задания>, <дата>\n"
        "Пример:\n"
        "ЭлТех: сделать лабу №2, 10.10.2025\n"
        "Для отмены нажми 'Отмена'",
        reply_markup=kb
    )

@dp.message(HomeworkStates.waiting_for_homework)
async def save_homework(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.clear()
        await message.answer("Действие отменено", reply_markup=main_kb)
        return

    text = message.text.strip()
    try:
        subject_part, rest = text.split(':', 1)
        description_part, date_part = rest.split(',', 1)
        subject = subject_part.strip()
        description = description_part.strip()
        date = date_part.strip()
        entry = {"subject": subject, "description": description, "date": date}
        homeworks.append(entry)
        save_homeworks(homeworks)
        await state.clear()
        await message.answer(f"Добавлено: {subject}: {description} ({date})", reply_markup=main_kb)
    except Exception:
        await message.answer(
            "Неверный формат. Попробуй еще раз или нажми 'Отмена':\n"
            "<название предмета>: <описание задания>, <дата>"
        )

@dp.message(F.text == 'Просмотр домашнее задание')
async def view_homework(message: Message):
    if not homeworks:
        kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Нет добавленных заданий')],[KeyboardButton(text='Назад')]], resize_keyboard=True)
        await message.answer("Домашнее задание:", reply_markup=kb)
        return

    buttons = []
    for id, hw in enumerate(homeworks, start=1):
        text = f"{id}. {hw['subject']}: {hw['description']} ({hw['date']})"
        buttons.append([KeyboardButton(text=text)])
    buttons.append([KeyboardButton(text='Назад')])

    kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer("Домашнее задание:", reply_markup=kb)

@dp.message(F.text.regexp(r'^\d+\.'))
async def edit_homework_handler(message: Message, state: FSMContext):
    try:
        idx = int(message.text.split('.')[0]) - 1
        
        if idx >= 0 and idx < len(homeworks):
            homework = homeworks[idx]
            
            await state.update_data(edit_idx=idx)
            await state.set_state(HomeworkStates.editing_homework)
            
            kb = ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text='Отмена')]],
                resize_keyboard=True
            )
            
            await message.answer(
                f"Редактирование задания:\n"
                f"Текущее задание: {homework['subject']}: {homework['description']}, {homework['date']}\n"
                f"Введите новое задание в формате:\n"
                f"<предмет>: <описание>, <дата>",
                reply_markup=kb
            )
    except:
        pass

@dp.message(HomeworkStates.editing_homework)
async def process_edit(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.clear()
        await view_homework(message)
        return

    try:
        text = message.text.strip()
        subject_part, rest = text.split(':', 1)
        description_part, date_part = rest.split(',', 1)
        
        data = await state.get_data()
        idx = data.get('edit_idx')
        
        if idx is not None:
            homeworks[idx] = {
                "subject": subject_part.strip(),
                "description": description_part.strip(),
                "date": date_part.strip()
            }
            save_homeworks(homeworks)
            await message.answer("Задание успешно изменено!", reply_markup=main_kb)
            await state.clear()
        else:
            await message.answer("Произошла ошибка. Попробуй снова.", reply_markup=main_kb)
            await state.clear()
    except Exception:
        await message.answer(
            "Неверный формат. Используй формат:\n"
            "<предмет>: <описание>, <дата>",
            reply_markup=main_kb
        )

@dp.message(F.text == 'Назад')
async def go_back(message: Message):
    await message.answer("Главное меню:", reply_markup=main_kb)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())