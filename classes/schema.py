import graphene
from graphene_django import DjangoObjectType

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .models import Student, Teacher, Topic, TopicLesson, Homework


class StudentType(DjangoObjectType):
	class Meta:
		model = Student


# class UserType(DjangoObjectType):
# 	class Meta:
# 		model = get_user_model()


class TeacherType(DjangoObjectType):
	class Meta:
		model = Teacher


class TopicType(DjangoObjectType):
	class Meta:
		model = Topic


class TopicLessonType(DjangoObjectType):
	class Meta:
		model = TopicLesson


class HomeworkType(DjangoObjectType):
	class Meta:
		model = Homework


# class DailyScheduleType(DjangoObjectType):
# 	class Meta:
# 		model = DailySchedule


# class WeekScheduleType(DjangoObjectType):
# 	class Meta:
# 		model = WeekSchedule


class Query(graphene.ObjectType):
	students = graphene.List(StudentType)
	student = graphene.Field(StudentType, username=graphene.String())
	teachers = graphene.List(TeacherType)
	teacher = graphene.Field(TeacherType, username=graphene.String())
	topics = graphene.List(TopicType)
	topic = graphene.Field(TopicType, title=graphene.String())
	topicLessons = graphene.List(TopicLessonType, day=graphene.String())
	topicLesson = graphene.Field(TopicLessonType)
	# dailySchedule = graphene.List(DailyScheduleType)

	def resolve_students(self, info):
		return Student.objects.all()

	def resolve_Users(self, info):
		return User.objects.all()

	def resolve_student(self, info, username):
		return Student.objects.get(user__username=username)

# -------------- Teacher -----------------------------

	def resolve_teachers(self, info):
		return Teacher.objects.all()

	def resolve_teacher(self, info, username):
		return Teacher.objects.get(user__username=username)


# -------------- Topics -----------------------------

	def resolve_topics(self, info):
		return Topic.objects.all()

	def resolve_topic(self, info, title):
		return Topic.objects.get(title=title)


# -------------- Topic Schedule -----------------------------

	def resolve_topicLesson(self, info, day):
		return TopicLesson.objects.filter(day=day)

	def resolve_topicLessons(self, info, title, day):
		return TopicLesson.objects.filter(topic__title__icontains=title).order_by('-day')


# -------------- Daily Schedule -----------------------------

	# def resolve_dailySchedule(self, info, day):
	# 	return DailySchedule.objects.filter(week_of_school=dat)


class CreateStudent(graphene.Mutation):
	student = graphene.Field(StudentType)
	# user = graphene.Field(UserType)

	class Arguments:
		bio = graphene.String()
		color = graphene.String()
		birth_date = graphene.Date()
		age = graphene.Int()
		grade = graphene.Int()
		user_id = graphene.Int()

	def mutate(self, info, bio, color, birth_date, age, grade, user_id):
		user = get_user_model().objects.get(id=user_id)
		student = Student(
			user=user,
			bio=bio,
			color=color,
			birth_date=birth_date,
			age=age,
			grade=grade,
		)

		student.save()
		return CreateStudent(student=student)


class CreateTeacher(graphene.Mutation):
	teacher = graphene.Field(TeacherType)
	# user = graphene.Field(UserType)

	class Arguments:
		name = graphene.String()
		user_id = graphene.Int()

	def mutate(self, info, name, user_id):
		user = get_user_model().objects.get(id=user_id)
		teacher = Teacher(
			user=user,
			name=name,

		)

		teacher.save()
		return CreateTeacher(teacher=teacher)


# class CreateTopic(graphene.Mutation):
# 	topic = graphene.Field(TopicType)
#
# 	class Arguments:
# 		student_id = graphene.Int()
# 		teacher_id = graphene.Int()
# 		title = graphene.String()
# 		supplies = graphene.String()
# 		location = graphene.String()
#
# 	def mutate(self, student_id, teacher_id, title, supplies, location):
# 		student = Student.objects.get(id=student_id)
# 		teacher = Teacher.objects.get(id=teacher_id)
# 		topic = Topic(student_id=student, teacher_id=teacher)


class Mutation(graphene.ObjectType):
	# create_topic = CreateTopic.Field()
	create_student = CreateStudent.Field()
	create_teacher = CreateTeacher.Field()