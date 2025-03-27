# main.py
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from keep_alive import keep_alive
import os

BOT_TOKEN = os.getenv("7906649563:AAFWaoUAHjYtd1Bcw0UWX0FDgIJ3vOMZOKk")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def get_okx_top_tokens():
    try:
        url = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"
        response = requests.get(url)
        data = response.json()

        if data["code"] != "0":
            print("\u274c Ошибка OKX:", data)
            return []

        tickers = data["data"]
        usdt_pairs = [t for t in tickers if t["instId"].endswith("USDT")]

        top = sorted(usdt_pairs, key=lambda x: float(x.get("volCcy24h", 0)), reverse=True)[:10]

        result = []
        for item in top:
            price = float(item.get("last", 0))
            open_price = float(item.get("open24h", price))
            change_percent = ((price - open_price) / open_price) * 100 if open_price else 0

            result.append({
                "symbol": item.get("instId", "???"),
                "price": price,
                "change": change_percent,
                "volume": float(item.get("volCcy24h", 0))
            })

        return result

    except Exception as e:
        print("\u274c Ошибка запроса к OKX:", e)
        return []

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tokens = get_okx_top_tokens()
    if tokens:
        msg = "\ud83d\udcca *TOP-10 tokens by volume (OKX)*\n\n"
        for i, t in enumerate(tokens, 1):
            msg += (
                f"#{i}: *{t['symbol']}*\n"
                f"\ud83d\udcb0 Price: ${t['price']:,.6f}\n"
                f"\ud83d\udcc8 24h: {t['change']:+.2f}%\n"
                f"\ud83d\udcb5 Volume (24h): ${t['volume']:,.0f}\n\n"
            )
        await update.message.reply_text(msg, parse_mode="Markdown")
    else:
        await update.message.reply_text("\u26a0\ufe0f Failed to get data from OKX.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi Pafnuтий! Send /top to get trending tokens from OKX.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("top", top))
    print("\u2705 Bot is running on Replit. Waiting for /top...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
