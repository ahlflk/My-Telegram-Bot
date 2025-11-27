import os
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from typing import Final

# === 1. Environment Configuration ===
# Polling အတွက် Render Variables တွေ မလိုအပ်တော့ပါ။ BOT_TOKEN သာ လိုသည်။
BOT_TOKEN: Final[str | None] = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    sys.exit("❌ FATAL: BOT_TOKEN Environment Variable ကို Render တွင် မတွေ့ပါ!")

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
    print("✅ Polling Mode ဖြင့် Bot Application ကို စတင်တည်ဆောက်နေပါပြီ...")
    
    # Application ကို Build လုပ်မည်
    application = Application.builder().token(BOT_TOKEN).build()

    # Handlers များ ထည့်သွင်းခြင်း
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # --- PTB 20.x အတွက် Polling Mode Setup ---
    print("🚀 Bot ကို Polling Mode ဖြင့် စတင်နေပါပြီ... (Continuous Mode)")
    
    # run_polling() သည် ယခင်က Error တက်စေသော Webhook Logic များကို ရှောင်ရှားပေးသည်။
    # Polling သည် စက်က အမြဲတမ်း ဖွင့်ထားရန် လိုအပ်ပါသည်။
    application.run_polling(poll_interval=1.0) # 1.0 စက္ကန့်ခြား တစ်ခါ စစ်ဆေးမည်

if __name__ == "__main__":
    main()
