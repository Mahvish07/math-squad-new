from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseForbidden
from .models import Contest, Question, Prizes, Registration, Choice, Answer
from .forms import RegistrationForm
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.models import User

# Create your views here. 
    
def adminPanel(request):

    return render(request, "admin_panel.html")
# Create your views here. 
    
def categoryPage(request):

    return render(request, "category-page.html")


def communityDiscussion(request):

    return render(request, "community_discussion.html")

# Create your views here.

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
    # Get IDs of contests the user is already registered for
    user_registered_ids = set(Registration.objects.filter(user=request.user).values_list('contest_id', flat=True))
    return render(request, "contest.html", {
        "contests": contests,
        "message": message,
        "registered_contest_id": registered_contest_id,
        "user_registered_ids": user_registered_ids
    })


# Create your views here. 
    
def index(request):

    return render(request, "index.html")

# Create your views here. 
    
def instancefeadback(request):

    return render(request, "instance_feadback.html")

# Create your views here. 
    
def notificationreminder(request):

    return render(request, "notification-reminder.html")


# Create your views here. 
    
def profilemanagment(request):

    return render(request, "profile_management.html")

# Create your views here. 
    
def rewardsachievement(request):

    return render(request, "rewards_achievement.html")

# Create your views here. 
    
def updateleaderboard(request):

    return render(request, "update_leaderboard.html")

def questions(request):
    questions = Question.objects.all()  # Fetch all questions from the database
    return render(request, "contest_questions.html", {"questions": questions})

def contestprizes(request, contest_id):
    contest = get_object_or_404(Contest, id=contest_id)
    prizes = Prizes.objects.filter(contest=contest)
    return render(request, "contest_prizes.html", {"contest": contest, "prizes": prizes})

def register_contest(request):
    message = None
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Registration successful!"
        else:
            message = "There was an error with your registration."
    else:
        form = RegistrationForm()

    contests = Contest.objects.all()
    return render(request, "register_contest.html", {
        "contests": contests,
        "form": form,
        "message": message
    })

@login_required
def my_registered_contests(request):
    registrations = Registration.objects.filter(user=request.user).select_related('contest')
    contests = [
        {
            'id': reg.contest.id,
            'name': reg.contest.name,
            'date': reg.contest.start_date.strftime('%Y-%m-%d'),
            'description': reg.contest.description,
            'category': reg.contest.category,
            'image': reg.contest.image,
        }
        for reg in registrations
    ]
    context = {
        'contests': contests
    }
    return render(request, 'my_registered_contests.html', context)

@login_required
def attempt_contest(request, contest_id):
    contest = get_object_or_404(Contest, id=contest_id)
    questions = contest.questions.all()
    duration = contest.duration  # in minutes

    # Track start time in session
    session_key = f'contest_{contest_id}_start_time'
    if session_key not in request.session:
        request.session[session_key] = timezone.now().isoformat()

    start_time = timezone.datetime.fromisoformat(request.session[session_key])
    elapsed = (timezone.now() - start_time).total_seconds() / 60  # in minutes

    if elapsed > duration:
        return render(request, "attempt_contest.html", {
            "contest": contest,
            "questions": [],
            "time_left": 0,
            "expired": True,
            "submitted": False,
        })

    time_left = max(0, int(duration - elapsed))
    submitted = False
    score = 0

    if request.method == 'POST':
        # Evaluate answers and save them
        for question in questions:
            choice_id = request.POST.get(f'answer_{question.id}')
            if choice_id:
                selected_choice = Choice.objects.filter(id=choice_id, question=question).first()
                Answer.objects.update_or_create(
                    user=request.user,
                    question=question,
                    defaults={'selected_choice': selected_choice}
                )
                if selected_choice and selected_choice.is_correct:
                    score += question.score
        # Save score in Registration
        registration, _ = Registration.objects.get_or_create(user=request.user, contest=contest)
        registration.score = score
        registration.save()
        submitted = True
        messages.success(request, f"Your answers have been submitted! Your score: {score}")

    return render(request, "attempt_contest.html", {
        "contest": contest,
        "questions": questions if not submitted else [],
        "time_left": time_left,
        "expired": False,
        "submitted": submitted,
        "score": score if submitted else None,
    })

@login_required
def contest_leaderboard(request, contest_id):
    # Get all registrations for this contest, ordered by score descending
    leaderboard = (
        Registration.objects.filter(contest_id=contest_id)
        .select_related('user')
        .order_by('-score')
    )
    contest = get_object_or_404(Contest, id=contest_id)
    return render(request, "contest_leaderboard.html", {
        "leaderboard": leaderboard,
        "contest": contest,
    })

@login_required
def global_leaderboard(request):
    # Aggregate scores across all contests for each user
    leaderboard = (
        Registration.objects.values('user__username')
        .annotate(total_score=Sum('score'))
        .order_by('-total_score')[:20]
    )
    return render(request, "global_leaderboard.html", {"leaderboard": leaderboard})