import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from typing import Final

# 1. Render ထဲက Environment Variable ကနေ token ယူမယ်
BOT_TOKEN: Final[str | None] = os.getenv("BOT_TOKEN")

# token မရှိရင် ချက်ချင်း ရပ်မယ် (အမှားကို အလွယ်တကူ သိနိုင်အောင်)
if not BOT_TOKEN:
    # ဤအမှားသည် BOT_TOKEN ကို Render Environment ထဲတွင် မထည့်ရသေးခြင်းကို ဖော်ပြသည်။
    raise ValueError("❌ BOT_TOKEN မတွေ့ပါ! Render → Environment ထဲမှာ သေချာ ထည့်သွင်းပေးပါ။")

# 2. Webhook Configuration အတွက် လိုအပ်သော Render Variables
PORT: Final[int] = int(os.environ.get("PORT", 8080)) # Render default port 10000 ကို 8080 သို့ပြောင်းသည်
WEBHOOK_PATH: Final[str] = f"/{BOT_TOKEN}"
# Render မှ ချပေးသော Public URL
WEBHOOK_URL: Final[str | None] = os.getenv("RENDER_EXTERNAL_URL")

if not WEBHOOK_URL:
    raise ValueError("❌ RENDER_EXTERNAL_URL မတွေ့ပါ! Render ပေါ်မှာ run နေခြင်း သေချာပါစေ။")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 မင်္ဂလာပါ! ကျွန်တော်က Render ပေါ်က 24/7 အွန်လိုင်း Bot ပါ။\n"
        "ဘာပဲ ရိုက်ပို့ပို့ ကျွန်တော် ပြန်ပို့ပေးပါ့မယ်။ 😊"
    )

# Text message များအားလုံးကို ပြန်ပို့ရန်
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        await update.message.reply_text(f"သင်ပို့တာ → {update.message.text}")

def main():
    # Application ကို Build လုပ်မည်
    app = Application.builder().token(BOT_TOKEN).build()

    # Handlers များ ထည့်သွင်းခြင်း
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # 3. Render Webhook Setup (PTB 20.x အတွက်)
    print(f"✅ Bot စတင်နေပါသည်... Port: {PORT}")

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=WEBHOOK_PATH,
        webhook_url=f"https://{WEBHOOK_URL}{WEBHOOK_PATH}"
    )
    print(f"🔥 Webhook ကို စတင်ခဲ့ပါပြီ။ URL: https://{WEBHOOK_URL}{WEBHOOK_PATH}")

if __name__ == "__main__":
    main()

