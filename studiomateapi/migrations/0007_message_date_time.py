# Generated by Django 4.1.3 on 2022-12-13 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studiomateapi', '0006_remove_message_date_remove_message_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='date_time',
            field=models.DateTimeField(default='2022-12-13'),
            preserve_default=False,
        ),
    ]
