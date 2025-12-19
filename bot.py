import json
import logging
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Загружаем триггерные фразы из JSON
with open('triggers.json', 'r', encoding='utf-8') as f:
    TRIGGERS = json.load(f)

def check_message(update: Update, context: CallbackContext) -> None:
    # Игнорируем сообщения от каналов
    if update.effective_chat.type not in ['group', 'supergroup']:
        return

    text = update.message.text.lower().strip()

    # Проверяем, есть ли текст в триггерах
    for trigger, response in TRIGGERS.items():
        if trigger in text:
            update.message.reply_text(response)
            logger.info(f'Сработал триггер: "{trigger}" в чате {update.effective_chat.title}')
            break

def main() -> None:
    from dotenv import load_dotenv
    import os

    load_dotenv()

    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    if not TOKEN:
        raise ValueError("Токен бота не указан. Установите TELEGRAM_BOT_TOKEN в .env")

    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    # Обрабатываем только текстовые сообщения (не команды)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check_message))

    logger.info("Бот запущен...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
