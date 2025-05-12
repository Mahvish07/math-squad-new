from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class Contest(models.Model):
    name = models.CharField(max_length=255)  # Name of the contest
    description = models.TextField(blank=True, null=True)  # Optional description
    start_date = models.DateTimeField()  # Start date and time of the contest
    end_date = models.DateTimeField()  # End date and time of the contest
    is_active = models.BooleanField(default=True)  # Whether the contest is currently active
    category = models.CharField(max_length=100)  # Category of the contest
    duration = models.IntegerField(help_text="Duration in minutes")  # Duration of the contest in minutes
    number_of_participants = models.PositiveIntegerField(default=0)  # Number of participants
    image = models.ImageField(upload_to='contest_images/', blank=True, null=True)  # Image for the contest

    def __str__(self):
        return self.name

class Question(models.Model):
    text = models.TextField()  # The question text
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the question was created
    contest = models.ForeignKey('Contest', on_delete=models.CASCADE, related_name='questions')  # Link to a contest

    def __str__(self):
        return self.text[:50]  # Return the first 50 characters of the question

class Category(models.Model):
    name = models.CharField(max_length=100)  # Name of the category
    description = models.TextField(blank=True, null=True)  # Optional description of the category

    def __str__(self):
        return self.name


class Prizes(models.Model):
    title = models.CharField(max_length=255)  # Title of the prize
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Prize amount
    description = models.TextField(blank=True, null=True)  # Optional description of the prize
    rank = models.PositiveIntegerField()  # Rank for the prize (e.g., 1 for First Prize)
    contest = models.ForeignKey('Contest', on_delete=models.CASCADE, related_name='prizes')  # Link to a contest

    def __str__(self):
        return f"{self.title} - {self.contest.name}"


class Browse(models.Model):
    title = models.CharField(max_length=255)  # Title of the browse item
    description = models.TextField(blank=True, null=True)  # Optional description
    link = models.URLField()  # Link to the resource or page

    def __str__(self):
        return self.title


class Community(models.Model):
    name = models.CharField(max_length=255)  # Name of the community
    description = models.TextField(blank=True, null=True)  # Optional description
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the community was created
    members_count = models.PositiveIntegerField(default=0)  # Number of members in the community

    def __str__(self):
        return self.name


class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contest = models.ForeignKey('Contest', on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.contest.name}"


@login_required
def contest(request):
    message = None
    registered_contest_id = None
    if request.method == 'POST':
        contest_id = request.POST.get('contest')
        if contest_id:
            contest_obj = Contest.objects.get(id=contest_id)
            # Prevent duplicate registration
            if not Registration.objects.filter(user=request.user, contest=contest_obj).exists():
                Registration.objects.create(
                    user=request.user,
                    contest=contest_obj
                )
                message = "Registration successful!"
            else:
                message = "You are already registered for this contest."
            registered_contest_id = int(contest_id)
        else:
            message = "Contest not found."
    contests = Contest.objects.all()
    return render(request, "contest.html", {
        "contests": contests,
        "message": message,
        "registered_contest_id": registered_contest_id
    })