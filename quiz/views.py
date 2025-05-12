from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseForbidden
from .models import Contest, Question, Prizes, Registration
from .forms import RegistrationForm

# Create your views here. 
    
def adminPanel(request):

    return render(request, "admin_panel.html")
# Create your views here. 
    
def categoryPage(request):

    return render(request, "category-page.html")


from django.shortcuts import rende
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

def my_registered_contests(request):
    # Example context data
    context = {
        'contests': [
            {'name': 'Algebra Contest', 'date': '2025-05-10'},
            {'name': 'Geometry Contest', 'date': '2025-05-15'},
        ]
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
        })

    time_left = max(0, int(duration - elapsed))

    if request.method == 'POST':
        # Handle answer submission logic here
        pass

    return render(request, "attempt_contest.html", {
        "contest": contest,
        "questions": questions,
        "time_left": time_left,
        "expired": False,
    })