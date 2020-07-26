# Generated by Django 3.0.8 on 2020-07-26 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20200725_1814'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('items_json', models.CharField(max_length=5000)),
                ('name', models.CharField(default='', max_length=70)),
                ('phone', models.CharField(max_length=14)),
                ('email', models.EmailField(default='', max_length=70)),
                ('amount', models.CharField(max_length=10)),
                ('address', models.CharField(default='', max_length=150)),
                ('address2', models.CharField(default='', max_length=150)),
                ('city', models.CharField(default='', max_length=50)),
                ('state', models.CharField(max_length=30)),
                ('zip_code', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='OrderUpdate',
            fields=[
                ('update_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_id', models.IntegerField(default='')),
                ('update_desc', models.CharField(max_length=5000)),
                ('timestamp', models.DateField(auto_now_add=True)),
            ],
        ),
    ]