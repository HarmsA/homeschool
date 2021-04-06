from django.shortcuts import render, redirect
from classes.models import *
from .forms import StudentForm
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from datetime import date


def register_page(request):
	form = CreateUserForm

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			form = CreateUserForm
	context = {
		'form' : form
	}
	return render(request, 'classes/register.html', context)

def login_page(request):
	context = {}
	return render(request, 'classes/login.html', context)

def home(request):
	# students = User.objects.filter(is_student=True)
	if not request.user:
		user = 'Not logged in'
	else:
		user = EndUser.objects.filter(is_student=True)
	all_classes = Topic.objects.all()
	print(user)
	form = StudentForm()
	#
	# if request.method == 'POST':
	# 	filled_form = StudentForm(request.POST)
	# 	print(filled_form)
	# 	if filled_form.is_valid():
	# 		Profile = Profile()
	# 		Profile.first_name = filled_form.cleaned_data['first_name']
	# 		Profile.last_name = filled_form.cleaned_data['last_name']
	# 		Profile.bio = filled_form.cleaned_data['bio']
	# 		Profile.birth_date = filled_form.cleaned_data['birth_date']
	# 		Profile.age = filled_form.cleaned_data['age']
	# 		Profile.grade = filled_form.cleaned_data['grade']
	# 		Profile.color = filled_form.cleaned_data['color']
	#
	# 		Profile.save()
	#
	# 		return redirect('home')

	# form = StudentForm()
	#
	# if request.method == 'POST':
	# 	filled_form = StudentForm(request.POST)
	# 	print(filled_form)
	# 	if filled_form.is_valid():
	# 		filled_form.save()
	# 		return redirect('/')

	context = {
		'title': 'HomeSchool',
		# 'students': students,
		'classes': all_classes,
		'form': form,
	}
	return render(request, 'classes/home.html', context)


def all_classes(request):
	topics = Topic.objects.all()
	context = {
		'title': "Classes Topic List",
		'classes': topics,
	}
	return render(request, 'classes/all_classes.html', context)


def class_info(request, slug):
	topic = Topic.objects.get(name__iexact=slug)
	lessons = Lesson.objects.filter(topic=topic)

	context = {
		'title': "Class Detail",
		'class': topic,
		'lessons': lessons,
	}
	return render(request, 'classes/class_info.html', context)


def all_students(request):
	students = EndUser.objects.all()

	context = {
		'title': 'All Students',
		'students': students,
	}
	return render(request, 'classes/all_students.html', context)


def student_info(request, slug):
	user = EndUser.objects.get(slug=slug)
	form = StudentForm(instance=user)

	if request.method == 'POST':
		filled_form = StudentForm(request.POST, instance=user)
		print(filled_form)
		if filled_form.is_valid():
			filled_form.save()
			return redirect('/user/'+slug)

	context = {
		'title': 'User Info',
		'user': user,
		'form': form,
	}
	return render(request, 'classes/student_info.html', context)


def schedule(request, slug=''):
	total_weeks = range(1, 41)
	week_list = list(total_weeks)
	now = date.today()
	# lesson_schedule = LessonSchedule.objects.filter(start__lte=now, end__gte=now)
	lesson_schedule = LessonSchedule.objects.all().order_by('week_number')
	days = DayChoices.objects.all()
	# raise Exception(lesson_schedule)
	# print(lesson_schedule)
	week_schedule = ''
	if slug:
		week_schedule = LessonSchedule.objects.filter(week_number=int(slug))

	context = {
		'title': 'Schedule',
		'lesson_schedule': lesson_schedule,
		'total_weeks': week_list,
		'week_schedule': week_schedule,
		'slug': slug,
		'days': days,
	}
	return render(request, 'classes/schedule.html', context)


def homework(request):
	print(request.user, "8"*80)
	user = EndUser.objects.get(user=request.user)
	# for work in User.homework.all():
	# 	print(work)
	homework = Homework.objects.filter(user_homework__user=request.user).order_by('priority')
	print(homework)
	context = {
		'title': 'Homework',
		'user': user,
		'homework':homework
	}
	return render(request, 'classes/homework.html', context)
