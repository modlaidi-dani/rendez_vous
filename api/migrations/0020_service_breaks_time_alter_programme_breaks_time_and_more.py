# Generated by Django 4.2.8 on 2024-02-28 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_rename_break_time_programme_breaks_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='breaks_time',
            field=models.ManyToManyField(related_name='programs', to='api.break_time'),
        ),
        migrations.AlterField(
            model_name='programme',
            name='breaks_time',
            field=models.ManyToManyField(related_name='programmes', to='api.break_time'),
        ),
        migrations.AlterField(
            model_name='service',
            name='programmes',
            field=models.ManyToManyField(related_name='service', to='api.programme'),
        ),
    ]
