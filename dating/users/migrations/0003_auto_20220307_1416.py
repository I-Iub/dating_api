# Generated by Django 3.2.12 on 2022-03-07 14:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220307_0620'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(verbose_name='Оценка')),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL, verbose_name='Кандидат')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matchings', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Оценка',
                'verbose_name_plural': 'Оценки',
                'ordering': ['user'],
            },
        ),
        migrations.AddConstraint(
            model_name='match',
            constraint=models.UniqueConstraint(fields=('user', 'candidate'), name='unique_matching'),
        ),
        migrations.AddConstraint(
            model_name='match',
            constraint=models.CheckConstraint(check=models.Q(('candidate', django.db.models.expressions.F('user')), _negated=True), name='user_is_not_candidate'),
        ),
    ]