# Generated by Django 4.2.8 on 2024-02-25 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_alter_programme_break_time_alter_service_programme'),
    ]

    operations = [
        migrations.RenameField(
            model_name='programme',
            old_name='break_time',
            new_name='breaks_time',
        ),
        migrations.RenameField(
            model_name='service',
            old_name='programme',
            new_name='programmes',
        ),
    ]