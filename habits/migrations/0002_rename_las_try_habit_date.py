# Generated by Django 4.2.6 on 2023-10-20 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='habit',
            old_name='las_try',
            new_name='date',
        ),
    ]
