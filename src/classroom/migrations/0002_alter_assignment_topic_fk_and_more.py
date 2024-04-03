# Generated by Django 5.0 on 2024-03-31 19:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='topic_fk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='classroom.topic'),
        ),
        migrations.AlterUniqueTogether(
            name='handin',
            unique_together={('assignment_fk', 'student_fk')},
        ),
    ]