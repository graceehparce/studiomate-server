# Generated by Django 4.1.3 on 2023-01-05 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studiomateapi', '0009_remove_notification_user_notification_receiver_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
