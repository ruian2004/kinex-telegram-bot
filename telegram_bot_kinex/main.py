import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

TOKEN = "7840985987:AAEXYxFK-RHWKKEUfKFUZxBPj1LXj5j438A"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# 状态按钮与对应话术（中英）
messages = {
    "未回复": ["请问您是否还对这份远程工作感兴趣？", "Just checking if you're still interested in this remote job?"],
    "资金不足": ["没关系，我们可以等您准备好资金，工作机会随时欢迎您。", "No worries, we’ll wait until you're ready. The opportunity remains open."],
    "想多份收入": ["确实，这份远程工作适合兼职，每天都有佣金结算。", "Exactly! This remote job is perfect for earning extra income daily."],
    "担心是骗局": ["完全理解您的担心，我们的平台已有数千用户正常领取收益。", "Understandable. Thousands of users are earning daily on this legit platform."],
    "提现问题": ["我们支持多种提现方式，收益每日可查，如遇问题请随时反馈。", "We support various withdrawal methods and daily income tracking."],
    "考虑中": ["好的，您随时可以回来继续了解，我们将为您保留名额。", "No problem! Take your time. Your spot is saved."],
    "想了解工作": ["这份工作不收取费用，远程操作，支持培训，每日佣金结算。", "This job is free to start, remote, with daily commission and full training."]
}

# 中文按钮
cn_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text=k, callback_data=f"cn|{k}")] for k in messages.keys()]
)

# 英文按钮
en_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text=k, callback_data=f"en|{k}")] for k in messages.keys()]
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("请选择语言 / Please select language:", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("中文", callback_data="lang_cn")],
        [InlineKeyboardButton("English", callback_data="lang_en")]
    ]))

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "lang_cn":
        await query.edit_message_text("请选择客户状态：", reply_markup=cn_keyboard)
    elif data == "lang_en":
        await query.edit_message_text("Please select customer status:", reply_markup=en_keyboard)
    else:
        lang, key = data.split("|")
        msg = messages.get(key, ["无匹配话术", "No matching message"])
        await query.edit_message_text(msg[0] if lang == "cn" else msg[1])

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.run_polling()
