# Generated by Django 4.2.6 on 2023-10-23 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0004_alter_habit_periodicity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='periodicity',
            field=models.SmallIntegerField(default=1, verbose_name='периодичность выполнения в днях'),
        ),
    ]