# Generated by Django 4.2.8 on 2024-02-25 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_break_time_remove_programme_name_progamme_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programme',
            name='break_time',
            field=models.ManyToManyField(to='api.break_time'),
        ),
        migrations.AlterField(
            model_name='service',
            name='programme',
            field=models.ManyToManyField(to='api.programme'),
        ),
    ]
