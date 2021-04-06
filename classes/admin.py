from django.contrib import admin
from .models import *



class LessonScheduleInline(admin.TabularInline):
	model = LessonSchedule
	# raw_id_fields = ['weekday', 'lesson']


class UserInline(admin.TabularInline):
	model = EndUser


class HomeworkInline(admin.TabularInline):
	model = Homework


class TopicInline(admin.TabularInline):
	model = Topic


# class LessonInline(admin.TabularInline):
# 	model = Lesson.student.through

class UserAdmin(admin.ModelAdmin):
	search_fields = ['user.first_name', 'completed', 'priority', 'title']
	# inlines = [HomeworkInline]
	# fields = ['title', 'description', 'date_assigned', 'due_date',
	#           'completed', 'priority']


class LessionScheduleAdmin(admin.ModelAdmin):
	search_fields = ['week_number', 'weekday']
	# fields = ['week_number']
	list_filter = ['week_number', 'weekday']


class HomeworkAdmin(admin.ModelAdmin):
	search_fields = []
	# inlines = [UserInline]
	fields = []

admin.site.register(DayChoices)
admin.site.register(Topic)
admin.site.register(EndUser, UserAdmin)
admin.site.register(Homework, HomeworkAdmin)
# admin.site.register(Homework)
# admin.site.register(DailySchedule, DailyScheduleAdmin)
admin.site.register(Lesson)
admin.site.register(LessonSchedule, LessionScheduleAdmin)
admin.site.register(SchoolYear)
admin.site.register(SchoolSemester)
admin.site.register(Grade)
# admin.site.register(WeekSchedule)
