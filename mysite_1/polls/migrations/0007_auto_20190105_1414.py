# Generated by Django 2.1.2 on 2019-01-05 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20190105_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='media/img/extra.png', upload_to='img/users'),
        ),
    ]
