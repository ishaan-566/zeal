# Generated by Django 3.0.6 on 2020-06-06 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='feature',
            field=models.BooleanField(default=False),
        ),
    ]
