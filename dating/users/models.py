from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


GENDERS = (
    ('Male', 'Мужчина'),
    ('Female', 'Женщина'),
)


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


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
    latitude = models.DecimalField(
        'Широта', max_digits=12, decimal_places=9, blank=True, null=True
    )
    longitude = models.DecimalField(
        'Долгота', max_digits=12, decimal_places=9, blank=True, null=True
    )
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

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
