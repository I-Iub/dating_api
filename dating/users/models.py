from django.contrib.auth.models import AbstractUser
from django.db import models


GENDERS = (
    ('Male', 'Мужчина'),
    ('Female', 'Женщина'),
)


class User(AbstractUser):
    avatar = models.ImageField(
        upload_to='users/',
        max_length=250,
        verbose_name='Аватарка'
    )
    gender = models.CharField('Пол', max_length=100, choices=GENDERS)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта'
    )

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
