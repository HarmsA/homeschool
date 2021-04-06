from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import HomeworkSerializer, TopicSerializer
from classes.models import *


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'List': '/topic-list/',
        'Details': '/topic-detail/<str:pk>/',
        'Create': '/topic-create/',
        'Update': '/topic-update/<str:pk>/',
        'Delete': '/topic-delete/<str:pk>/',
    }

    return Response(api_urls)


@api_view(['GET'])
def topic_list(request):
    topic = Topic.objects.all()
    serializer = TopicSerializer(topic, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def topic_detail(request, pk):
    topic = Topic.objects.get(id=pk)
    serializer = TopicSerializer(topic)
    return Response(serializer.data)


@api_view(['POST'])
def topic_create(request):
    serializer = TopicSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def topic_update(request, pk):
    topic = Topic.objects.get(id=pk)
    serializer = TopicSerializer(instance=topic, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def topic_delete(request, pk):
    topic = Topic.objects.get(id=pk)
    topic.delete()

    return Response()
