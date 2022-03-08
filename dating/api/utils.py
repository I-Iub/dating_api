import io
import os

from django.conf import settings
from django.core.mail import send_mail
from PIL import Image
from PIL import ImageEnhance

ENCHANCE_FACTOR = 0.1
ROTATE = -30


def watermark(source):
    """Получает картинку в виде bytes-like-object, накладывает водяной знак и
    возвращает её в виде bytes-like-object.
    """
    image = Image.open(io.BytesIO(source))
    mark = Image.open(
        os.path.join(settings.BASE_DIR, 'media/watermark/heart-love-red.jpg')
    )
    mark = mark.resize(image.size)
    alpha = ImageEnhance.Brightness(mark.split()[2]).enhance(ENCHANCE_FACTOR)
    mark.putalpha(alpha)
    mark = mark.rotate(ROTATE, Image.BICUBIC)
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    if mark.mode != 'RGBA':
        mark = mark.convert('RGBA')
    watermark_image = Image.alpha_composite(image, mark)
    buffer = io.BytesIO()
    watermark_image.save(buffer, format='PNG')
    return buffer.getvalue()


def send_email(name, email):
    subject = 'Dating'
    message = (f'Вы понравились {name}!'
               f'Почта участника: {email}')
    return send_mail(subject, message, settings.ADMIN_EMAIL, [email])
