# Generated by Django 3.2.3 on 2021-06-06 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_ambassador',
            field=models.BooleanField(max_length=255),
        ),
    ]