# Generated by Django 5.0.3 on 2024-07-30 03:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_orderitems_purchased_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='purchased_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 30, 3, 36, 6, 426786, tzinfo=datetime.timezone.utc)),
        ),
    ]
