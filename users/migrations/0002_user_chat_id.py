# Generated by Django 4.2.6 on 2023-10-19 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='chat_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='id чата'),
        ),
    ]
