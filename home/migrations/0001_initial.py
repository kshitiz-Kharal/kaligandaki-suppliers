# Generated by Django 3.0.8 on 2020-07-25 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50)),
                ('email', models.TextField(max_length=50)),
                ('phone', models.TextField(max_length=50)),
                ('message', models.TextField(max_length=50)),
            ],
        ),
    ]
