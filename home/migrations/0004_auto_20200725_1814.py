# Generated by Django 3.0.8 on 2020-07-25 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20200725_1646'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='mrp_price',
            new_name='price',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='productName',
            new_name='product_name',
        ),
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.ImageField(upload_to='home/images'),
        ),
    ]
