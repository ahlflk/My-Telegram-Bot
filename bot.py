import os
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# ApplicationHook Import ကို ဖြုတ်လိုက်သည်။
from typing import Final
from waitress import serve

# === 1. Environment Configuration ===
BOT_TOKEN: Final[str | None] = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    sys.exit("❌ FATAL: BOT_TOKEN Environment Variable ကို Render တွင် မတွေ့ပါ!")

PORT: Final[int] = int(os.environ.get("PORT", 8080))
WEBHOOK_PATH: Final[str] = f"/{BOT_TOKEN}"
WEBHOOK_URL: Final[str | None] = os.getenv("RENDER_EXTERNAL_URL")

if not WEBHOOK_URL:
    sys.exit("❌ FATAL: RENDER_EXTERNAL_URL မတွေ့ပါ! Render ပေါ်မှာ run နေကြောင်း သေချာပါစေ။")

FULL_WEBHOOK_URL: Final[str] = f"https://{WEBHOOK_URL}{WEBHOOK_PATH}"

# === 2. Handlers (Functions) ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start command ကို ဖြေကြားခြင်း"""
    await update.message.reply_text(
        "👋 မင်္ဂလာပါ! ကျွန်တော်က Render ပေါ်က 24/7 အွန်လိုင်း Bot ပါ။\n"
        "ဘာပဲ ရိုက်ပို့ပို့ ကျွန်တော် ပြန်ပို့ပေးပါ့မယ်။ 😊"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Text message များကို ပြန်လည်ပို့ပေးခြင်း"""
    if update.message and update.message.text:
        await update.message.reply_text(f"သင်ပို့တာ → {update.message.text}")

# === 3. Application Setup Function ===
def setup_application() -> Application:
    """Application ကို တည်ဆောက်ပြီး Handlers များ ထည့်သွင်းပေးသည်။"""
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    return app

# === 4. Main Function ===

def main():
    print("✅ Bot Application ကို တည်ဆောက်နေပါပြီ...")
    
    application = setup_application()
    
    # Webhook URL ကို သတ်မှတ်ခြင်း (Telegram Server သို့)
    print(f"🔥 Webhook URL ကို သတ်မှတ်နေပါသည်... {FULL_WEBHOOK_URL}")
    application.bot.set_webhook(url=FULL_WEBHOOK_URL)

    # PTB Webhook Handler (WSGI compatible) ကို ရယူခြင်း
    webhook_handler = application.get_webhook_handler()

    # application ကို စတင်ရန် post_init hook ကို ခေါ်ဆိုခြင်း (Webhook Server Run မလုပ်ခင် လိုအပ်သည်)
    application.post_init() # Parameter မပါဘဲ ခေါ်လိုက်ပါပြီ။

    print(f"🚀 Waitress Server ကို {PORT} တွင် စတင်နေပါပြီ...")
    # Waitress server ကို အသုံးပြုပြီး Webhook Handler ကို Run ခြင်း
    serve(webhook_handler, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    main()
