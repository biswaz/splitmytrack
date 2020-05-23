# Generated by Django 3.0.5 on 2020-05-18 15:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_coins'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('coins', models.PositiveIntegerField()),
                ('receipt', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('buyer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]