from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('upload/', views.upload_resume, name='upload_resume'),

    path('resumes/', views.resume_list, name='resume_list'),

    # 👇 ADD THESE
    path('resume/<int:pk>/', views.resume_detail, name='resume_detail'),
    path('resume/delete/<int:pk>/', views.delete_resume, name='delete_resume'),

    path('analytics/', views.analytics, name='analytics'),
]