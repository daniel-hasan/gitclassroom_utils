# Generated by Django 3.2.7 on 2023-12-27 21:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acronym', models.CharField(max_length=4)),
                ('name', models.CharField(max_length=50)),
                ('assignment_url', models.CharField(max_length=255, unique=True)),
                ('invitation_url', models.CharField(max_length=255, unique=True)),
                ('deadline', models.DateTimeField()),
                ('total_auto_grade', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_grade', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('code', models.CharField(max_length=10)),
                ('url', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('class_id', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acronym', models.CharField(max_length=4)),
                ('name', models.CharField(max_length=100, null=True)),
                ('discipline_fk', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='classroom.discipline')),
            ],
            options={
                'unique_together': {('discipline_fk', 'acronym')},
            },
        ),
        migrations.CreateModel(
            name='Handin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_url', models.CharField(blank=True, max_length=255, null=True)),
                ('auto_grade', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('final_grade', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('complementar_grade', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('assignment_fk', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='classroom.assignment')),
                ('student_fk', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='classroom.student')),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='discipline_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='classroom.discipline'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='topic_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='classroom.topic'),
        ),
        migrations.AlterUniqueTogether(
            name='assignment',
            unique_together={('discipline_fk', 'acronym')},
        ),
    ]