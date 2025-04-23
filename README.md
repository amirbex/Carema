# 🤖 Aiogram + Gemini Bot

این پروژه یک ربات تلگرامی با استفاده از Aiogram و مدل‌های Gemini است.

## 💡 امکانات:
- ارائه رسپی غذا، نوشیدنی و قهوه
- مشاوره مالی، منابع انسانی و مارکتینگ
- پاسخ به سوالات آزاد با کمک Gemini

## ⚙️ اجرا در Render.com

1. این ریپازیتوری را به GitHub ارسال کنید.
2. وارد [Render.com](https://render.com) شوید.
3. روی **New Web Service** کلیک کنید و GitHub repo را انتخاب کنید.
4. **Start Command:** `python main.py`
5. متغیرهای محیطی را از `.env.example` اضافه کنید.

## 🧪 تست محلی

```bash
pip install -r requirements.txt
export BOT_TOKEN=...
export GEMINI_API_KEY=...
python main.py
