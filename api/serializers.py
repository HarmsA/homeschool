from rest_framework import serializers
from classes.models import *


class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = '__all__'



