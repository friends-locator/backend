# Generated by Django 4.1 on 2023-07-28 15:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_alter_customuser_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="friendsrelationship",
            name="friend_category",
            field=models.CharField(
                choices=[
                    ("none_category", "Без категории"),
                    ("friends", "Близкие друзья"),
                    ("family", "Семья"),
                ],
                default="none_category",
                help_text="Укажите категорию друга",
                max_length=50,
                verbose_name="Название категории",
            ),
        ),
    ]