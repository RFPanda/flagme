import asyncio
import emoji
import pycountry
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Напиши название страны на английском языке, и я покажу её флаг.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    await update.message.reply_text('Напиши название страны на английском языке, и я покажу её флаг.')
 #   await process_ip(update, context, user_message)

def get_country_code(country_name: str) -> str:
    """Возвращает код страны по её названию."""
    try:
        country = pycountry.countries.lookup(country_name)
        return country.alpha_2  # Возвращаем код страны в верхнем регистре
    except LookupError:
        return None


def country_flag(country_code: str) -> str:
    """Возвращает эмодзи флага по коду страны."""
    return chr(127397 + ord(country_code[0])) + chr(127397 + ord(country_code[1]))


async def convert_to_flag(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()

    # Получаем код страны по названию
    country_code = get_country_code(text)

    if country_code:
        flag = country_flag(country_code)  # Генерируем флаг с помощью функции
        await update.message.reply_text(flag)
    else:
        await update.message.reply_text('Страна не найдена. Попробуйте другую.')


def main() -> None:
    application = ApplicationBuilder().token("*****").build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_to_flag))
    application.add_handler(CommandHandler("help", handle_message))
    #application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()
    # Запуск бота
    application.run_polling()


if __name__ == '__main__':
    main()