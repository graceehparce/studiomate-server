# Generated by Django 4.1.3 on 2022-12-14 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studiomateapi', '0007_message_date_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='name',
            field=models.CharField(default='Suzuki', max_length=1000),
            preserve_default=False,
        ),
    ]