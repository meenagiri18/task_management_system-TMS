# Generated by Django 5.0.7 on 2024-12-09 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_create_task_delete_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assign_task',
            name='is_completed',
        ),
        migrations.RemoveField(
            model_name='assign_task',
            name='is_deleted',
        ),
    ]
