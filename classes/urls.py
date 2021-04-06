from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('', views.home, name='home'),
    path('classes/', views.all_classes, name='all_classes'),
    path('classes/<slug:slug>/', views.class_info, name='class_info'),
    path('students/', views.all_students, name='all_students'),
    path('student/<slug:slug>/', views.student_info, name='student_info'),
    path('schedule/', views.schedule, name='schedule'),
    path('homework/', views.homework, name='homework'),
    path('schedule/<slug:slug>/', views.schedule, name='schedule'),

    # path('create', views.create, name='create'),
    # path('profile/<str:name>/', views.profile, name='profile'),

]
