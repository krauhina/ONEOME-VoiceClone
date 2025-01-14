from aiogram.types import update
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext, filters
import os
from model import make_voice  #функция имортируется из файла с инициализацией модели

API_TOKEN = '7597763427:AAG8gOyyD4OJDetO_4EXArYzElQm6E9P8V8'
voice_dir = 'VOICE'  # Папка для сохранения голосовых сообщений
text_dir = 'TEXT'  # Папка для сохранения тектовых сообщений
result_dir = 'RESULT'  # Папка для сохранения сгенерированных аудиофайлов

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Данный бот создан для генерации текста вашим голосом. Для начала отправьте голосовое сообщение длиной 20 секунд,'
                                    'чтобы мы смогли учесть все особенности вашего голоса и в дальнейшем с помощью него генерировать аудиофайлы')

async def handle_voice(update: Update, context: CallbackContext) -> None:

    user_id = update.message.from_user.id
    voice = update.message.voice

    file = await voice.get_file()
    file_path = os.path.join(voice_dir, f'voice_message_user_{user_id}.ogg')

    await file.download_to_drive(file_path)
    await update.message.reply_text('Ваше голосовое сообщение было успешно сохранено! '
                                    'Теперь отправьте текст, который хотели бы озвучить')


async def handle_text(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_input = update.message.text

    file_path = os.path.join(text_dir, f'text_message_user_{user_id}.txt')
    with open(file_path, 'w', encoding='utf-8') as text_file:
        text_file.write(user_input)

    await update.message.reply_text('Ваш текст было успешно сохранен!')

    voice_file_path = os.path.join(voice_dir, f'user_{user_id}.ogg')
    if os.path.exists(voice_file_path):
        await process_files(user_id)


async def process_files(user_id):
    text_file_path = os.path.join(text_dir, f'text_message_user_{user_id}.txt')
    voice_file_path = os.path.join(voice_dir, f'user_{user_id}.ogg')
    voice_file_path_result = os.path.join(result_dir, f'user_{user_id}.ogg')

    with open(text_file_path, 'r', encoding='utf-8') as text_file:
        text_content = text_file.read()

    await make_voice(text_content, voice_file_path, voice_file_path_result)

    with open(voice_file_path_result, 'rb') as audio_file:  # Открываем аудиофайл в бинарном режиме
        await update.message.reply_audio(chat_id=user_id, audio=audio_file, caption='Ваш аудиофайл готов!Если вам нужно озвучить другой текст, то присылайте его ниже')




def main() -> None:
    application = ApplicationBuilder().token("7597763427:AAG8gOyyD4OJDetO_4EXArYzElQm6E9P8V8").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    application.run_polling()


if __name__ == '__main__':
    main()