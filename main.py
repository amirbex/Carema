# main.py

import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode
import google.generativeai as genai

# 🔹 بارگذاری توکن‌ها از متغیرهای محیطی
TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 🔹 تنظیمات Gemini
genai.configure(api_key=GEMINI_API_KEY)

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# کیبورد منو
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📌 رسپی غذا و خوراک")],
        [KeyboardButton(text="🥤 رسپی نوشیدنی‌های سرد")],
        [KeyboardButton(text="☕ تنظیم کردن قهوه")],
        [KeyboardButton(text="💰 مدیریت مالی")],
        [KeyboardButton(text="👥 مدیریت منابع انسانی")],
        [KeyboardButton(text="📈 مدیریت مارکتینگ")],
        [KeyboardButton(text="❓ سوال آزاد")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(f"سلام {message.from_user.first_name}! 👋")
    await asyncio.sleep(1)
    await message.answer("من دستیار هوشمند کافه و رستوران هستم. 🍽️☕")
    await asyncio.sleep(1)
    await message.answer(
        "می‌تونم در این موارد کمکت کنم:\n\n"
        "📌 رسپی غذا و خوراک\n🥤 رسپی نوشیدنی‌های سرد\n☕ تنظیم کردن قهوه\n"
        "💰 مدیریت مالی\n👥 مدیریت منابع انسانی\n📈 مدیریت مارکتینگ\n\n"
        "یکی از گزینه‌ها رو انتخاب کن یا سوال خاصی بپرس! 😊",
        reply_markup=menu_keyboard
    )

@dp.message(lambda message: message.text in [
    "📌 رسپی غذا و خوراک", "🥤 رسپی نوشیدنی‌های سرد", "☕ تنظیم کردن قهوه",
    "💰 مدیریت مالی", "👥 مدیریت منابع انسانی", "📈 مدیریت مارکتینگ"
])
async def handle_category(message: types.Message):
    category = message.text
    prompts = {
        "📌 رسپی غذا و خوراک": "شما یک سرآشپز حرفه‌ای هستید...",
        "🥤 رسپی نوشیدنی‌های سرد": "شما یک متخصص نوشیدنی‌های سرد...",
        "☕ تنظیم کردن قهوه": "شما یک باریستای حرفه‌ای هستید...",
        "💰 مدیریت مالی": "شما یک متخصص مالی هستید...",
        "👥 مدیریت منابع انسانی": "شما یک متخصص منابع انسانی هستید...",
        "📈 مدیریت مارکتینگ": "شما یک مشاور مارکتینگ هستید..."
    }
    prompt_text = prompts[category] + "\nسه سوال حرفه‌ای بپرس که به کاربر کمک کند نیازش را بهتر مشخص کند."

    thinking_message = await message.answer("🤔 در حال فکر کردن هستم...")
    response = await get_gemini_response(prompt_text)
    await bot.delete_message(chat_id=message.chat.id, message_id=thinking_message.message_id)
    await message.answer(f"لطفاً به این سوالات پاسخ بده:\n\n{response}")

@dp.message(lambda message: message.text == "❓ سوال آزاد")
async def free_question(message: types.Message):
    await message.answer("💡 سوالت رو بپرس، من کمکت می‌کنم!")

@dp.message()
async def handle_free_question(message: types.Message):
    user_input = message.text
    thinking_message = await message.answer("🤔 در حال فکر کردن هستم...")
    response = await get_gemini_response(f"سوال کاربر: {user_input}\nپاسخ دقیق بده.")
    await bot.delete_message(chat_id=message.chat.id, message_id=thinking_message.message_id)
    await message.answer(response)

async def get_gemini_response(prompt_text):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt_text)
        return response.text if hasattr(response, "text") else "پاسخی دریافت نشد."
    except Exception as e:
        logging.error(f"خطا: {e}")
        return "متأسفم، مشکلی پیش آمد."

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
