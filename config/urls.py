"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView 
from django.conf import settings
from django.conf.urls.static import static
from quiz import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", TemplateView.as_view(template_name='index.html'), name="home"),
    path("", include("quiz.urls"), name="quiz"),
    path('auth/', include('authentication.urls'), name='auth'),
    path('contest/<int:contest_id>/leaderboard/', views.contest_leaderboard, name='contest_leaderboard'),
    path('leaderboard/global/', views.global_leaderboard, name='global_leaderboard'),
    # path("contest/", TemplateView.as_view(template_name='contest.html'), name="contest"),
    # path("login/", TemplateView.as_view(template_name='login.html'), name="about"),
    # path("signup/", TemplateView.as_view(template_name='register.html'), name="register"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)