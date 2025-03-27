import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот пампов. Используй /top или /today.")

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Тут будет список токенов.")

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Тут будут сигналы за сегодня.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("top", top))
    app.add_handler(CommandHandler("today", today))
    print("Бот запущен!")
    await app.run_polling()

import asyncio
asyncio.run(main())
