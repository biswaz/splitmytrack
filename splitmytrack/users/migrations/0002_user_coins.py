# Generated by Django 3.0.5 on 2020-05-18 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='coins',
            field=models.PositiveIntegerField(default=0),
        ),
    ]