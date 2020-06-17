# Generated by Django 3.0.3 on 2020-06-17 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_tasklist'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='tasklist',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='todo.TaskList'),
            preserve_default=False,
        ),
    ]
