from classes.models import *


def ContextProcessor(request):
	menu_item_classes = Topic.objects.all()
	students = EndUser.objects.filter(is_student=True)

	# menu_item_students = Student.objects.all()

	return {
		"menu_item_classes": menu_item_classes,
		# "menu_item_students": menu_item_students,
	}