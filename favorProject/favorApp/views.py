from django.shortcuts import render, redirect
from .forms import SignUpForm, AddFavorForm
from django.http import HttpResponseRedirect
from .models import Favor

# Signup/Login stuff
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from django.db.models import Q # new


def landing(request):
    return render(request, 'landing.html')


@login_required
def show_services(request):
    query = request.GET.get('q')
    cards = Favor.objects.all();
    if query:
        cards = Favor.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    return render(request, 'home.html', {
        "cards": cards,
        "search_term": query if query else ""
    })


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        else:
            print("form not valid")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


@login_required
def add_favor(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = AddFavorForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/user')
    # If this is a GET (or any other method) create the default form.
    else:
        form = AddFavorForm()

    context = {
        'form': form,
    }

    return render(request, 'add_favor.html', context)


def show_profile_page(request):
    current_user = request.user
    favors = Favor.objects.all().filter(owner=request.user)
    context = {
        'user' : current_user,
        'favors': favors,
    }
    return render(request, 'profile.html', context)