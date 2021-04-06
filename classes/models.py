from django.db import models
from django.utils.text import slugify
import datetime
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.contrib.auth.models import User as User_model
from django.db.models.signals import post_save
from django.dispatch import receiver


class ColorChoices(models.TextChoices):
	Black = '#000000'
	Night = '#0C090A'
	Gunmetal = '#2C3539'
	Midnight = '#2B1B17'
	Charcoal = '#34282C'
	Dark_Slate_Gray = '#25383C'
	Oil = '#3B3131'
	Black_Cat = '#413839'
	Iridium = '#3D3C3A'
	Black_Eel = '#463E3F'
	Sky_Blue = '#6698FF'


class EndUser(models.Model):
	user = models.OneToOneField(User_model, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500, blank=True, null=True)
	birth_date = models.DateField(null=True, blank=True)
	age = models.IntegerField(blank=True, null=True)
	grade = models.CharField(max_length=20, blank=True, null=True)
	color = models.CharField(max_length=25, choices=ColorChoices.choices, default=ColorChoices.Black)
	slug = models.SlugField(max_length=100, blank=True, null=True)
	is_student = models.BooleanField(default=True)
	is_teacher = models.BooleanField(default=False)
	lesson = models.ManyToManyField('Lesson', related_name='user_lesson', blank=True)
	homework = models.ManyToManyField('Homework', blank=True, related_name='user_homework')

	@receiver(post_save, sender=User_model)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			EndUser.objects.create(user=instance)

	@receiver(post_save, sender=User_model)
	def save_user_profile(sender, instance, **kwargs):
		instance.enduser.save()

	def save(self, *args, **kwargs):
		name = self.user.first_name + ' ' + self.user.last_name
		if name and not self.slug:
			self.slug = slugify(name)
		super(type(self), self).save(*args, **kwargs)

	def __str__(self):
		return f"username - ({self.user}) - {self.user.first_name} {self.user.last_name}"


class Topic(models.Model):
	name = models.CharField(max_length=75, blank=True, null=True, unique=True)
	slug = models.SlugField(max_length=100, blank=True, null=True)

	def save(self, *args, **kwargs):
		if self.name and not self.slug:
			self.slug = slugify(self.name)
		super(type(self), self).save(*args, **kwargs)

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return self.name


class DayChoices(models.Model):
	choice = models.CharField(max_length=10, unique=True)

	def __str__(self):
		return self.choice


class Homework(models.Model):
	title = models.CharField(max_length=250, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	date_assigned = models.DateField(default=datetime.today)
	due_date = models.DateField(blank=True, null=True)
	completed = models.BooleanField(default=False)
	modified = models.DateField(auto_now_add=True)
	priority = models.IntegerField(default=2)

	def __str__(self):
		delta = str(self.due_date)
		return f"{self.title} -- {delta[:11]}"


class Lesson(models.Model):
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topic_lesson', null=True, blank=True)
	visibility = models.BooleanField(default=True)
	required_supplies = models.CharField(max_length=255, blank=True, null=True, default='No Supplies needed')
	# has_homework = models.BooleanField(default=False)
	# lesson = models.ForeignKey('Homework', null=True, blank=True, related_name='lesson_homework',  on_delete=models.CASCADE)

	def __str__(self):
		newline = "\n"
		return f'{self.topic.name} - Lesson'
		# return f'{newline.join(f"{self.topic.name}: {student}" for student in self.user_lesson.all())}'


class LessonSchedule(models.Model):
	class AM_PM(models.TextChoices):
		AM = 'am'
		PM = 'pm'

	week_number = models.IntegerField(default=0)
	weekday = models.ManyToManyField(DayChoices, related_name='day', default='Blank')
	lesson = models.ForeignKey(Lesson, related_name='lesson_schedules', on_delete=models.CASCADE)
	start_hr = models.IntegerField(default=8)
	start_min = models.IntegerField(default=00)
	am_pm = models.CharField(max_length=2, choices=AM_PM.choices, default=AM_PM.AM)
	duration = models.IntegerField(default=30)

	class Meta:
		ordering = ('week_number',)

	def __str__(self):
		return f'Week - {self.week_number}, Topic - {self.lesson.topic.name}'


# class Homework(models.Model):
# 	topic = models.ManyToManyField(Topic, related_name='homework_topic')
# 	student = models.ManyToManyField(Student, related_name='student_homework')
# 	has_homework = models.BooleanField(default=False)
# 	details = models.TextField(blank=True, null=True)
#
# 	def __str__(self):
# 		return f'{self.student} has homework in {self.topic}'


class SchoolYear(models.Model):
	year = models.CharField(max_length=10, blank=True, null=True)

	def __str__(self):
		return self.year


class SchoolSemester(models.Model):
	semester = models.CharField(max_length=50, blank=True, null=True)
	year = models.ManyToManyField(SchoolYear, related_name='school_semester', blank=True)
	start = models.DateField(blank=True, null=True)
	end = models.DateField(blank=True, null=True)

	def __str__(self):
		return self.semester


class Grade(models.Model):
	class Meta:
		unique_together = ('student', 'grade')

	student = models.ForeignKey(EndUser, related_name='student_grade', on_delete=models.CASCADE)
	semester = models.ForeignKey(SchoolSemester, related_name='semester_grade', on_delete=models.CASCADE)
	topic = models.ForeignKey(Topic, related_name='grades_topic', on_delete=models.CASCADE)
	grade = models.CharField(max_length=20, blank=True, null=True)

	def __str__(self):
		return f'{self.student} received an {self.grade} in {self.topic}'



# '#4C4646'
# '#504A4B'
# '#565051'
# '#5C5858'
# '#625D5D'
# '#666362'
# '#6D6968'
# '#726E6D'
# '#736F6E'
# '#837E7C'
# '#848482'
# B6B6B4
# D1D0CE
# E5E4E2
# BCC6CC
# 98AFC7
# 6D7B8D
# 657383
# 616D7E
# 646D7E
# 566D7E
# 737CA1
# 4863A0
# 2B547E
# 2B3856
# 151B54
# 000080
# 342D7E
# 15317E
# 151B8D
# 0000A0
# 0020C2
# 0041C2
# 2554C7
# 1569C7
# 2B60DE
# 1F45FC
# 6960EC
# 736AFF
# 357EC7
# 368BC1
# 488AC7
# 3090C7
# 659EC7
# 87AFC7
# 95B9C7
# 728FCE
# 2B65EC
# 306EFF
# 157DEC
# 1589FF
# 6495ED
# 6698FF
# 38ACEC
# 56A5EC
# 5CB3FF
# 3BB9FF
# 79BAEC
# 82CAFA
# 82CAFF
# A0CFEC
# B7CEEC
# B4CFEC
# C2DFFF
# C6DEFF
# AFDCEC
# ADDFFF
# BDEDFF
# CFECEC
# E0FFFF
# EBF4FA
# F0F8FF
# F0FFFF
# CCFFFF
# 93FFE8
# 9AFEFF
# 7FFFD4
# 00FFFF
# 7DFDFE
# 57FEFF
# 8EEBEC
# 50EBEC
# 4EE2EC
# 81D8D0
# 92C7C7
# 77BFC7
# 78C7C7
# 48CCCD
# 43C6DB
# 46C7C7
# 7BCCB5
# 43BFC7
# 3EA99F
# 3B9C9C
# 438D80
# 348781
# 307D7E
# 5E7D7E
# 4C787E
# 008080
# 4E8975
# 78866B
# 848b79
# 617C58
# 728C00
# 667C26
# 254117
# 306754
# 347235
# 437C17
# 387C44
# 347C2C
# 347C17
# 348017
# 4E9258
# 6AA121
# 4AA02C
# 41A317
# 3EA055
# 6CBB3C
# 6CC417
# 4CC417
# 52D017
# 4CC552
# 54C571
# 99C68E
# 89C35C
# 85BB65
# 8BB381
# 9CB071
# B2C248
# 9DC209
# A1C935
# 7FE817
# 59E817
# 57E964
# 64E986
# 5EFB6E
# 00FF00
# 5FFB17
# 87F717
# 8AFB17
# 6AFB92
# 98FF98
# B5EAAA
# C3FDB8
# CCFB5D
# B1FB17
# BCE954
# EDDA74
# EDE275
# FFE87C
# FFFF00
# FFF380
# FFFFC2
# FFFFCC
# FFF8C6
# FFF8DC
# F5F5DC
# FBF6D9
# FAEBD7
# F7E7CE
# FFEBCD
# F3E5AB
# ECE5B6
# FFE5B4
# FFDB58
# FFD801
# FDD017
# EAC117
# F2BB66
# FBB917
# FBB117
# FFA62F
# E9AB17
# E2A76F
# DEB887
# FFCBA4
# C9BE62
# E8A317
# EE9A4D
# C8B560
# D4A017
# C2B280
# C7A317
# C68E17
# B5A642
# ADA96E
# C19A6B
# CD7F32
# C88141
# C58917
# AF9B60
# AF7817
# B87333
# 966F33
# 806517
# 827839
# 827B60
# 786D5F
# 493D26
# 483C32
# 6F4E37
# 835C3B
# 7F5217
# 7F462C
# C47451
# C36241
# C35817
# C85A17
# CC6600
# E56717
# E66C2C
# F87217
# F87431
# E67451
# FF8040
# F88017
# FF7F50
# F88158
# F9966B
# E78A61
# E18B6B
# E77471
# F75D59
# E55451
# E55B3C
# FF0000
# FF2400
# F62217
# F70D1A
# F62817
# E42217
# E41B17
# DC381F
# C34A2C
# C24641
# C04000
# C11B17
# 9F000F
# 990012
# 8C001A
# 954535
# 7E3517
# 8A4117
# 7E3817
# 800517
# 810541
# 7D0541
# 7E354D
# 7D0552
# 7F4E52
# 7F5A58
# 7F525D
# B38481
# C5908E
# C48189
# C48793
# E8ADAA
# ECC5C0
# EDC9AF
# FDD7E4
# FCDFFF
# FFDFDD
# FBBBB9
# FAAFBE
# FAAFBA
# F9A7B0
# E7A1B0
# E799A3
# E38AAE
# F778A1
# E56E94
# F660AB
# FC6C85
# F6358A
# F52887
# E45E9D
# E4287C
# F535AA
# FF00FF
# E3319D
# F433FF
# D16587
# C25A7C
# CA226B
# C12869
# C12267
# C25283
# C12283
# B93B8F
# 7E587E
# 571B7E
# 583759
# 4B0082
# 461B7E
# 4E387E
# 614051
# 5E5A80
# 6A287E
# 7D1B7E
# A74AC7
# B048B5
# 6C2DC7
# 842DCE
# 8D38C9
# 7A5DC7
# 7F38EC
# 8E35EF
# 893BFF
# 8467D7
# A23BEC
# B041FF
# C45AEC
# 9172EC
# 9E7BFF
# D462FF
# E238EC
# C38EC7
# C8A2C8
# E6A9EC
# E0B0FF
# C6AEC7
# F9B7FF
# D2B9D3
# E9CFEC
# EBDDE2
# E3E4FA
# FDEEF4
# FFF5EE
# FEFCFF
# FFFFFF
