import os
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from typing import Final

# === 1. Environment Configuration ===
# Render မှ BOT_TOKEN ကို ရယူခြင်း
BOT_TOKEN: Final[str | None] = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    # BOT_TOKEN မရှိရင် ချက်ချင်း ရပ်မယ်
    sys.exit("❌ FATAL: BOT_TOKEN Environment Variable ကို Render တွင် မတွေ့ပါ! ကျေးဇူးပြု၍ သေချာ ထည့်သွင်းပါ။")

# Render မှ ချပေးသော Webhook နှင့် Port
PORT: Final[int] = int(os.environ.get("PORT", 8080))
WEBHOOK_PATH: Final[str] = f"/{BOT_TOKEN}"
# Render မှ ပေးသော Public URL
WEBHOOK_URL: Final[str | None] = os.getenv("RENDER_EXTERNAL_URL")

if not WEBHOOK_URL:
    # RENDER_EXTERNAL_URL မရှိရင် ချက်ချင်း ရပ်မယ်
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

# === 3. Main Function ===

def main():
    print("✅ Bot စတင်တည်ဆောက်နေပါပြီ...")
    
    # Application ကို Build လုပ်မည်
    app = Application.builder().token(BOT_TOKEN).build()

    # Handlers များ ထည့်သွင်းခြင်း
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # --- PTB 20.x အတွက် Webhook Setup ---
    # Polling mode ကို လုံးဝ မသုံးဘဲ Webhook ဖြင့်သာ Run ရန်
    
    print(f"🔥 Webhook Setup: {FULL_WEBHOOK_URL} (Port: {PORT})")

    # Webhook ကို စတင်ခြင်း
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=WEBHOOK_PATH,
        webhook_url=FULL_WEBHOOK_URL
    )

if __name__ == "__main__":
    main()
