# Generated by Django 4.1 on 2023-01-11 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat_users', '0004_alter_friendrequest_status'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='friendrequest',
            unique_together={('sender', 'receiver')},
        ),
    ]
