from django import forms
from django.forms import ModelForm
from classes.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class StudentForm(ModelForm):
	first_name = forms.CharField(label='First Name', max_length=50, strip=True)
	last_name = forms.CharField(label='Last Name', max_length=50, strip=True)
	bio = forms.CharField(label='Bio', strip=True, max_length=50, widget=forms.Textarea())
	birth_date = forms.DateField(label='Birthday', required=False)
	age = forms.IntegerField()
	grade = forms.IntegerField()
	color = forms.CharField(label='Represented Color', max_length=50, )

	class Meta:
		model = EndUser
		fields = '__all__'


class TodoForm(ModelForm):
	first_name = forms.CharField(label='First Name', max_length=50, strip=True)
	last_name = forms.CharField(label='Last Name', max_length=50, strip=True)
	bio = forms.CharField(label='Bio', strip=True, max_length=50, widget=forms.Textarea())
	birth_date = forms.DateField(label='Birthday', required=False)
	age = forms.IntegerField()
	grade = forms.IntegerField()
	color = forms.CharField(label='Represented Color', max_length=50, )

	class Meta:
		model = EndUser
		fields = '__all__'


class TeacherForm(forms.Form):
	name = forms.CharField(label='Name', strip=True)

	class Meta:
		model = EndUser
		fields = ['name']


class TopicForm(forms.Form):
	name = forms.CharField(label='Class', strip=True)

	class Meta:
		model = Topic
		fields = ['name']


class LessonForm(forms.Form):
	topic = forms.ChoiceField()
	visibility = forms.CharField()
	student = forms.CharField(label='Bio', strip=True)
	teacher = forms.DateField(label='Birthday', required=False)
	has_homework = forms.BooleanField(label='Homework')
	homework_description = forms.CharField(label='Homework')

	class Meta:
		model = Lesson
		fields = ['topic', 'visibility', 'student', 'teacher', 'title', 'description']
