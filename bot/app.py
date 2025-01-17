import os
from telegram import Update, Bot, InputMediaPhoto
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import numpy as np
import cv2
from Detector.main import Detector

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        bot: Bot = context.bot
        message = update.message

        file_id = message.photo[-1].file_id
        img_file = await bot.get_file(file_id)
        img_buf = await img_file.download_as_bytearray()
        np_arr = np.frombuffer(img_buf, np.uint8)
        cv2_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        detector = Detector(cv2_img)
        result = detector.get_license_plate()

        images = []
        text = []

        img_buf = bytes(cv2.imencode('.png', detector.img)[1])
        images.append(img_buf)

        text.append(f'Обнаружено номеров: {detector.detected}')
        text.append(f'Распознано номеров: {detector.recognized}')

        for plate_img, plate_text, confidence, (x, y), (w, h) in result:
            plate_img_buf = bytes(cv2.imencode('.png', plate_img)[1])
            images.append(plate_img_buf)

            text.append('')
            text.append(f'Номер: {plate_text or "?"}')
            text.append(f'Точность: {confidence:.2%}')
            text.append(f'Координаты: {x}, {y}')
            text.append(f'Размеры: {w} x {h}')

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
