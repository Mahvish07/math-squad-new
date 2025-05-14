from django.db import models
from django.contrib.auth.models import User

class Contest(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    category = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Duration in minutes")
    number_of_participants = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='contest_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    contest = models.ForeignKey('Contest', on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.text[:50]

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Prizes(models.Model):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    rank = models.PositiveIntegerField()
    contest = models.ForeignKey('Contest', on_delete=models.CASCADE, related_name='prizes')

    def __str__(self):
        return f"{self.title} - {self.contest.name}"

class Browse(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    link = models.URLField()

    def __str__(self):
        return self.title

class Community(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    members_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contest = models.ForeignKey('Contest', on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.contest.name}"