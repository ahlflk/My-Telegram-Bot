import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN env var not defined")

# Render provides PORT env var for web services
PORT = int(os.getenv("PORT", "10000"))
# PUBLIC_URL should be your Render service HTTPS URL e.g. https://my-bot.onrender.com
PUBLIC_URL = os.getenv("PUBLIC_URL")  # set this in Render env vars
if not PUBLIC_URL:
    raise RuntimeError("PUBLIC_URL env var not defined — set it to your onrender.com url")

WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"        # path on your server (keeps it secret-ish)
WEBHOOK_URL = f"{PUBLIC_URL}{WEBHOOK_PATH}"  # final webhook URL to register with Telegram

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 မင်္ဂလာပါ — Webhook နဲ့ အလုပ်လုပ်နေတဲ့ Bot ဖြစ်ပါတယ်!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        await update.message.reply_text(f"သင်ပို့တာ → {update.message.text}")

def main():
    logger.info("Building Application")
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

    # Start webhook server (built-in aiohttp-based)
    logger.info("Setting webhook to %s", WEBHOOK_URL)
    # run_webhook will:
    #  - bind to 0.0.0.0:PORT
    #  - register webhook with Telegram
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=WEBHOOK_PATH.lstrip("/"),   # run_webhook expects path without leading slash
        webhook_url=WEBHOOK_URL,
    )

if __name__ == "__main__":
    main()