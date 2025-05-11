
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = "7825237686:AAEHGbWwhHEFn7i_fqiU2v0yBmTUoORX1_I"
CHANNEL_USERNAME = "@Alex_prolager34"  # Юзернейм канала

USERS_FILE = "users.txt"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Сохраняем ID в файл, если ещё не сохранён
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            f.write(f"{user_id}\n")
    else:
        with open(USERS_FILE, "r+", encoding="utf-8") as f:
            users = f.read().splitlines()
            if str(user_id) not in users:
                f.write(f"{user_id}\n")

    keyboard = [[InlineKeyboardButton("Поехали", callback_data="subscribe")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = (
        "👋 Привет! Меня зовут Александр Алёшечкин.\n\n"
        "Я — директор детского научного лагеря «Интеграл». 15 лет управляю командами, запускаю смены, "
        "заключаю партнёрства с детскими центрами по всей стране.\n\n"
        "Этот бот — про то, как не терять сотни тысяч на управленческих ошибках.\n\n"
        "👇 Жми «Поехали»"
    )
    await update.message.reply_text(text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "subscribe":
        keyboard = [
            [InlineKeyboardButton("✅ Подписался", callback_data="check_subscription")],
            [InlineKeyboardButton("🔄 Открыть канал", url="https://t.me/Alex_prolager34")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            text=(
                "Перед тем как скину PDF, подпишись на мой канал:\n"
                "👉 https://t.me/Alex_prolager34\n\n"
                "Когда подпишешься — нажми кнопку ниже:"
            ),
            reply_markup=reply_markup
        )

    elif query.data == "check_subscription":
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ("member", "administrator", "creator"):
            await query.message.reply_photo(
                photo="https://example.com/leadmagnet_preview.jpg",
                caption="✅ Подписка подтверждена! Отправляю файл...",
            )
            with open("leadmagnet.pdf", "rb") as pdf:
                await query.message.reply_document(
                    document=pdf,
                    caption=(
                        "📘 *5 ошибок руководителя, которые обходятся компании в сотни тысяч*\n\n"
                        "Прочитай внимательно — это сэкономит тебе кучу денег и нервов."
                    ),
                    parse_mode="Markdown"
                )
        else:
            await query.message.reply_text("❗️Ты ещё не подписан на канал. Подпишись и попробуй снова.")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            users = f.read().splitlines()
            count = len(users)
    else:
        count = 0
    await update.message.reply_text(f"Всего пользователей в боте: {count}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    app.run_polling()
