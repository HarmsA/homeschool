# Generated by Django 3.0 on 2021-03-26 21:58

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DayChoices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_assigned', models.DateTimeField(default=django.utils.timezone.now)),
                ('due_date', models.DateTimeField(default=datetime.datetime.today)),
                ('completed', models.BooleanField(default=False)),
                ('modified', models.DateField(auto_now_add=True)),
                ('priority', models.IntegerField(default=2)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visibility', models.BooleanField(default=True)),
                ('required_supplies', models.CharField(blank=True, default='No Supplies needed', max_length=255, null=True)),
                ('has_homework', models.BooleanField(default=False)),
                ('lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='lesson_homework', to='classes.Homework')),
            ],
        ),
        migrations.CreateModel(
            name='SchoolYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=75, null=True, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=100, null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(max_length=500, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('grade', models.CharField(max_length=20, null=True)),
                ('color', models.CharField(max_length=20, null=True)),
                ('slug', models.SlugField(blank=True, max_length=100, null=True)),
                ('is_student', models.BooleanField(default=True)),
                ('is_teacher', models.BooleanField(default=False)),
                ('lesson', models.ManyToManyField(blank=True, related_name='user_lesson', to='classes.Lesson')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolSemester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(blank=True, max_length=50, null=True)),
                ('start', models.DateField(blank=True, null=True)),
                ('end', models.DateField(blank=True, null=True)),
                ('year', models.ManyToManyField(blank=True, related_name='school_semester', to='classes.SchoolYear')),
            ],
        ),
        migrations.CreateModel(
            name='LessonSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_number', models.IntegerField(default=0)),
                ('start_hr', models.IntegerField(default=8)),
                ('start_min', models.IntegerField(default=0)),
                ('am_pm', models.CharField(choices=[('am', 'Am'), ('pm', 'Pm')], default='am', max_length=2)),
                ('duration', models.IntegerField(default=30)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_schedules', to='classes.Lesson')),
                ('weekday', models.ManyToManyField(default='Blank', related_name='day', to='classes.DayChoices')),
            ],
            options={
                'ordering': ('week_number',),
            },
        ),
        migrations.AddField(
            model_name='lesson',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='topic_lesson', to='classes.Topic'),
        ),
        migrations.AddField(
            model_name='homework',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='student_todo', to='classes.User'),
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(blank=True, max_length=20, null=True)),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semester_grade', to='classes.SchoolSemester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_grade', to='classes.User')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades_topic', to='classes.Topic')),
            ],
            options={
                'unique_together': {('student', 'semester', 'topic', 'grade')},
            },
        ),
    ]
