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
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Match(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='matchings',
        verbose_name='Пользователь'
    )
    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Кандидат'
    )
    like = models.BooleanField(verbose_name='Оценка')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'candidate'],
                name='unique_matching'
            ),
            models.CheckConstraint(
                check=~models.Q(candidate=models.F('user')),
                name='user_is_not_candidate'
            )
        ]
        ordering = ['user']
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    def __str__(self):
        return (f'Оценка пользователем {self.user.email} кандидата '
                f'{self.candidate.email}')
