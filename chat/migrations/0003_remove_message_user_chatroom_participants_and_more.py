# Generated by Django 4.2.6 on 2023-10-13 11:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chatroom_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='user',
        ),
        migrations.AddField(
            model_name='chatroom',
            name='participants',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='recipient',
            field=models.ForeignKey(default='12', on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(default='12', on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
