# Generated by Django 3.0.8 on 2020-07-31 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_order_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.CharField(default='', max_length=500),
        ),
    ]
