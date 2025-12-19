import json
import logging
import random
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

    text = update.message.text.lower()

    # Проверяем, содержится ли хотя бы один триггер в сообщении
    for trigger, data in TRIGGERS.items():
        if isinstance(data, dict):
            chance = data.get("chance", 100)
            response = data["response"]
        else:
            # Совместимость со старым форматом
            chance = 100
            response = data

        if trigger.lower() in text:
            if random.randint(1, 100) <= chance:
                update.message.reply_text(response)
                logger.info(f'Сработал триггер: "{trigger}" (шанс {chance}%) в чате {update.effective_chat.title}')
            else:
                logger.info(f'Триггер "{trigger}" проигнорирован по шансу ({chance}%).')
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
