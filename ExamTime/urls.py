"""ExamTime URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from quiz import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_request),
    path('signup/',views.signup),
    path('examformsubmit/', views.addExam),
    path('formsubmit/', views.addQuestion),
    path('studentpanel/',views.showStudent),
    path('startexam/',views.startExam),
    path('exitexam/',views.showExamForm),
    path('login/',views.login_request),
    path('logout/',views.logout_request),
]
