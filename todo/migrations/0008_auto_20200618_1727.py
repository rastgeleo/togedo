# Generated by Django 3.0.3 on 2020-06-18 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0007_task_is_important'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-createdat']},
        ),
        migrations.AlterModelOptions(
            name='tasklist',
            options={'ordering': ['-createdat']},
        ),
        migrations.AlterField(
            model_name='task',
            name='slug',
            field=models.SlugField(max_length=63),
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together={('slug', 'tasklist')},
        ),
    ]
