import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from config import BOT_TOKEN
from database import SheetDB
from ai_helper import generate_task

logging.basicConfig(level=logging.INFO)

# Состояния для диалога
ASK_MOOD, ASK_TASK_RESULT = range(2)

db = SheetDB()

# Клавиатуры
def main_menu():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("🌤 Оценить настроение")]],
        resize_keyboard=True
    )

def mood_buttons():
    return ReplyKeyboardMarkup(
        [[f"{i}"] for i in range(1, 11)],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def yes_no_buttons():
    return ReplyKeyboardMarkup(
        [["✅ Да, сделал", "❌ Нет, не сделал"]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

# === СТАРТ ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Проверяем, есть ли пользователь в базе
    existing = db.get_user_data(user.id)
    if existing:
        await update.message.reply_text(
            f"С возвращением, {user.first_name}! 👋\n\n"
            "Твоё утреннее задание уже ждёт тебя.\n"
            "Нажми «Оценить настроение», чтобы начать день.",
            reply_markup=main_menu()
        )
        return
    
    # НОВЫЙ ПОЛЬЗОВАТЕЛЬ — отправляем ссылку на анкету (только одно сообщение!)
    form_link = "https://docs.google.com/forms/d/e/1FAIpQLSdQTb0uuRIw5oREazVFO82AsiVnFuj9Mw3aTTPHNYz3KvTYpA/viewform?fbzx=7145173308504976576"
    
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        "Ты в числе первых тестировщиков **Nudge24Bot** — бота, который помогает дизайнерам быть продуктивнее и не выгорать.\n\n"
        "📝 **Чтобы начать, заполни небольшую анкету:**\n"
        f"👉 [Заполнить анкету]({form_link})\n\n"
        "⏳ Это займёт 2 минуты.\n"
        "После заполнения я дам тебе доступ к боту.\n\n"
        "✅ Уже заполнил? Просто нажми /start ещё раз!",
        reply_markup=main_menu(),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

# === УТРЕННИЙ ОПРОС ===
async def ask_mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌤 **Как твоё настроение сегодня утром?**\n"
        "Оцени от 1 (ужасно) до 10 (превосходно):",
        reply_markup=mood_buttons()
    )
    return ASK_MOOD

async def save_morning_mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mood = int(update.message.text)
    user_id = update.effective_user.id
    
    db.save_mood(user_id, mood, "morning")
    
    user_data = db.get_user_data(user_id)
    if not user_data:
        form_link = "https://docs.google.com/forms/d/e/1FAIpQLSdQTb0uuRIw5oREazVFO82AsiVnFuj9Mw3aTTPHNYz3KvTYpA/viewform?fbzx=7145173308504976576"
        await update.message.reply_text(
            "❌ Я не нашёл тебя в базе данных.\n\n"
            "Сначала заполни анкету по ссылке, а потом нажми /start снова:\n"
            f"👉 [Заполнить анкету]({form_link})",
            parse_mode="Markdown"
        )
        return ConversationHandler.END
    
    profession = user_data.get("profession", "дизайнер")
    goal = user_data.get("goal", "повысить продуктивность")
    
    task = generate_task(mood, profession, goal)
    
    context.user_data['current_task'] = task
    db.save_current_task(user_id, task)
    
    await update.message.reply_text(
        f"✨ **Твоё задание на сегодня:**\n\n{task}\n\n"
        "Сделай это в течение дня, а вечером я спрошу как дела.",
        reply_markup=main_menu()
    )
    return ConversationHandler.END

# === ВЕЧЕРНИЙ ЧЕК ===
async def evening_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌙 **Вечерний чекап!**\n\n"
        "Сделал ли ты сегодняшнее задание?",
        reply_markup=yes_no_buttons()
    )
    return ASK_TASK_RESULT

async def save_evening_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    completed = update.message.text == "✅ Да, сделал"
    user_id = update.effective_user.id
    
    db.save_task_result(user_id, completed)
    
    await update.message.reply_text(
        "📊 **А теперь оцени настроение вечером**\n"
        "От 1 до 10:",
        reply_markup=mood_buttons()
    )
    return ASK_MOOD

async def save_evening_mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mood = int(update.message.text)
    user_id = update.effective_user.id
    
    db.save_mood(user_id, mood, "evening")
    
    user_data = db.get_user_data(user_id)
    morning_mood = user_data.get("morning_mood", 0)
    
    if morning_mood and mood > morning_mood:
        await update.message.reply_text(
            "📈 **Отличный прогресс!**\n"
            f"Твоё настроение выросло с {morning_mood} до {mood}.\n"
            "Так держать! 🎉\n\n"
            "Завтра в 9:00 жду тебя снова.",
            reply_markup=main_menu()
        )
    elif morning_mood and mood < morning_mood:
        await update.message.reply_text(
            "💪 **День был непростой, но ты молодец!**\n"
            f"Настроение изменилось с {morning_mood} до {mood}.\n"
            "Завтра будет лучше. Отдыхай.",
            reply_markup=main_menu()
        )
    else:
        await update.message.reply_text(
            "🌿 **Хороший день!**\n"
            "Ты справился. Увидимся завтра!",
            reply_markup=main_menu()
        )
    return ConversationHandler.END

# === ОБРАБОТЧИК ГЛАВНОГО МЕНЮ ===
async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "Оценить настроение" in text:
        return await ask_mood(update, context)
    elif "Вечерний чек" in text:
        return await evening_check(update, context)
    else:
        await update.message.reply_text(
            "Используй кнопки меню 👇",
            reply_markup=main_menu()
        )
        return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            MessageHandler(filters.Regex('Оценить настроение'), ask_mood),
            MessageHandler(filters.Regex('Вечерний чек'), evening_check),
        ],
        states={
            ASK_MOOD: [MessageHandler(filters.Regex(r'^[1-9]|10$'), save_morning_mood)],
            ASK_TASK_RESULT: [MessageHandler(filters.Regex('^(✅ Да, сделал|❌ Нет, не сделал)$'), save_evening_result)],
        },
        fallbacks=[CommandHandler('start', start)],
    )
    
    app.add_handler(conv_handler)
    
    print("🤖 Бот запущен!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
