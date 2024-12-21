from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from app.forms import MessageForm, ProfileUpdateForm, MissingPetReportForm
from .models import Message, Profile, MissingPetReport

def news_page(request):
    # Fetch all missing pet reports
    missing_pets = MissingPetReport.objects.all().order_by('-date_last_seen')
    return render(request, 'news.html', {'missing_pets': missing_pets})

@login_required
def report_missing_pet(request):
    if request.method == "POST":
        form = MissingPetReportForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the report and associate it with the logged-in user
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            messages.success(request, "Your missing pet report has been submitted.")
            return redirect("home")  # Redirect to home or any other relevant page
        else:
            messages.error(request, "There was an error with your submission. Please correct it below.")
    else:
        form = MissingPetReportForm()

    context = {"form": form}
    return render(request, "report_missing_pet.html", context)

@login_required
def profile_view(request):
    # Get or create the user's profile
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')  # Redirect to the profile page after update
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'profile.html', {'form': form})

@login_required
def chatroom(request):
    messages = Message.objects.all().order_by('-created_at')  # Get all messages, ordered by latest
    form = MessageForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        content = form.cleaned_data['content']
        Message.objects.create(user=request.user, content=content)
        return redirect('chatroom')  # Redirect to refresh the chatroom with the new message
    
    return render(request, 'chatroom.html', {'messages': messages, 'form': form})


def home(request):
    if request.user.is_authenticated:
        context = {
            'user': request.user
        }
    else:
        context = {}

    return render(request, 'home.html', context)



def login_user(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home if already logged in

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Log the user in
            messages.success(request, "You have been logged in successfully!")
            return redirect('home')  # Redirect to home page after successful login
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')  # Redirect back to login page if authentication fails

    else:
        # If request is GET, render login page
        return render(request, 'log_in.html')

def logout_user(request):
    if request.method == "POST":
        confirm = request.POST.get('confirm')
        if confirm == "yes":
            logout(request)
            messages.success(request, "You have been logged out.")
            return redirect('home')
        elif confirm == "cancel":
            messages.info(request, "Logout canceled.")
            return redirect('home')  # Adjust to a relevant page, e.g., profile or dashboard
    return render(request, 'logout_confirm.html')


def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})

