# Generated by Django 5.0.7 on 2024-12-22 03:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_assign_task_is_completed_assign_task_is_deleted_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assign_task',
            old_name='due_date',
            new_name='ddate',
        ),
    ]
