# Generated by Django 4.2 on 2024-02-13 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'verbose_name': 'Игра', 'verbose_name_plural': 'Игры'},
        ),
        migrations.AddField(
            model_name='game',
            name='mine_field',
            field=models.JSONField(default=list),
        ),
    ]
