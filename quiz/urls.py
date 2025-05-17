from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import contest, rewardsachievement, contestprizes, register_contest, my_registered_contests, attempt_contest

urlpatterns = [
    path("my-contests/", my_registered_contests, name="my_registered_contests"),
    path("contest/", contest, name="contest"),
    path("achievement/", rewardsachievement, name="achievement"),
    path("feedback/", contest, name="feedback"),
    path("notification/", contest, name="notification"),
    path("leaderboard/", contest, name="leaderboard"),
    path("profile/", contest, name="profile"),
    path("navigation/", contest, name="navigation"),
    path('register-contest/', register_contest, name='register_contest'),
    path('contest/<int:contest_id>/attempt/', attempt_contest, name='attempt_contest'),
]