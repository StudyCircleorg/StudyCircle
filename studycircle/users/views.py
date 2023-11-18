from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User

# Create your views here.
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("core:index"))
        else:
            return render(request, "users/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "users/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("core:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure ualberta.ca domain validation        
        email = request.POST["email"]
        domain = email.split("@")[1]
        if domain != "ualberta.ca":
            return render(request, "users/register.html", {
                "message": "Invalid email (must use UofA email)."
            })

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "users/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "users/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("core:index"))
    else:
        return render(request, "users/register.html")
    
def profile_view(request):
    return render(request, "users/profile.html", {
        "user": request.user
    })