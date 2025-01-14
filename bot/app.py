import os
from telegram import Update, Bot, InputMediaPhoto
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        bot: Bot = context.bot
        message = update.message

        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id)
        img_buf = bytes(await file.download_as_bytearray())

        result = {
            'image': img_buf,
            'detected': 2,
            'recognized': 2,
            'plates': [
                {
                    'image': img_buf,
                    'number': 'T212YT02',
                    'accuracy': 0.9,
                    'x': 10,
                    'y': 20,
                    'width': 30,
                    'height': 40,
                },
                {
                    'image': img_buf,
                    'number': 'M567MA797',
                    'accuracy': 0.9,
                    'x': 40,
                    'y': 30,
                    'width': 20,
                    'height': 10,
                },
            ],
        }

        images = []
        text = []

        images.append(result['image'])
        text.append(f'Обнаружено номеров: {result['detected']}')
        text.append(f'Распознано номеров: {result['recognized']}')

        for plate in result['plates']:
            images.append(plate['image'])
            text.append('')
            text.append(f'Номер: {plate['number'] or '?'}')
            text.append(f'Точность: {plate['accuracy']:.2%}')
            text.append(f'Координаты: {plate['x']}, {plate['y']}')
            text.append(f'Размеры: {plate['width']} x {plate['height']}')

        media = [InputMediaPhoto(image) for image in images]
        caption = '\n'.join(text)
        await bot.send_media_group(update.effective_chat.id, media, caption=caption)

    except Exception as e:
        await bot.send_message(update.effective_chat.id, 'Произошла ошибка при обработке изображения')
        raise e

def run_bot():
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    if BOT_TOKEN is None:
        raise Exception('BOT_TOKEN is not set')

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()
