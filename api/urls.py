from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.api_overview, name='api_overview'),
    path('topic-list/', views.topic_list, name='topic_list'),
    path('topic-detail/<str:pk>/', views.topic_detail, name='topic_detail'),
    path('topic-create/', views.topic_create, name='topic_create'),

    path('topic-update/<str:pk>/', views.topic_update, name='topic_update'),
    path('topic-delete/<str:pk>/', views.topic_delete, name='topic_delete'),

]
