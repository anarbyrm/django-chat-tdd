# Generated by Django 4.1 on 2023-01-11 14:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat_users', '0002_alter_user_managers_user_friends'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('D', 'Declined'), ('A', 'Accepted'), ('NA', 'No Answer')], default=('NA', 'No Answer'), max_length=2)),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='awaiting_requests', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests_sent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
