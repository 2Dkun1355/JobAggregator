# Generated by Django 5.1 on 2024-08-23 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0004_alter_rawvacancy_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vacancy',
            old_name='salary',
            new_name='salary_max',
        ),
        migrations.AddField(
            model_name='vacancy',
            name='salary_min',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]