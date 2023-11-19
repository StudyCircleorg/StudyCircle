from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from groups.models import UserGroup, Group
from courses.models import Course

from .models import User, UserCourse

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
    user = request.user
    enrolled_courses = UserCourse.objects.filter(user=user)
    enrolled_groups = UserGroup.objects.filter(user=user)
    courses = Course.objects.all()
    available_groups = Group.objects.exclude(usergroup__user=user)  # Get groups that the user is not already in

    if request.method == "POST" and 'group_id' in request.POST:
        group_id = request.POST.get("group_id")
        group = Group.objects.get(id=group_id)
        UserGroup.objects.create(user=user, group=group)
        return redirect('users:profile')

    return render(request, "users/profile.html", {
        "user": user,
        "enrolled_courses": enrolled_courses,
        "enrolled_groups": enrolled_groups,
        "courses": courses,
        "available_groups": available_groups,
    })

def edit_profile_view(request):
    if request.method == "POST":
        new_username = request.POST["new_username"]
        new_email = request.POST["new_email"]
        major = request.POST["major"]
        degree = request.POST["degree"]
        user = request.user

        # Add Major and Degree
        user.major = major
        user.degree = degree

        # Check if the new username or email is different from the current one
        if new_username != user.username or new_email != user.email:
            # Check if the new username or email is available
            if User.objects.filter(username=new_username).exists() or User.objects.filter(email=new_email).exists():
                return render(request, "users/profile.html", {
                    "user": user,
                    "message": "Username or email is already taken."
                })

            # Update Username and Email
            user.username = new_username
            user.email = new_email
            user.save()

            return render(request, "users/profile.html", {
                "user": user,
                "message": "Profile updated successfully."
            })

        else:
            return render(request, "users/profile.html", {
                "user": user,
                "message": "No changes detected in Username or Email."
            })
    else:
        return render(request, "users/profile.html", {
            "user": request.user
        })
    
def add_course_view(request):
    if request.method == "POST":
        try:
            course_id = request.POST.get("course_id")

            # Check if the course_id is provided and is not empty
            if not course_id:
                messages.error(request, "Please select a course to add.")
                return redirect('users:profile')

            # Get the course by id
            course = Course.objects.get(id=course_id)

            # Check if the user is already enrolled in the course
            if UserCourse.objects.filter(user=request.user, course=course).exists():
                messages.error(request, "You are already enrolled in this course.")
            else:
                # Create the UserCourse relationship
                user_course = UserCourse(user=request.user, course=course)
                user_course.save()
                messages.success(request, "Course added successfully.")
            
        except Course.DoesNotExist:
            # Handle the case where the course does not exist
            messages.error(request, "The selected course does not exist.")

        except Exception as e:
            # Handle any other exception that may occur
            messages.error(request, "An error occurred while adding the course.")

    # Whether successful or not, redirect back to the profile page
    return redirect('users:profile')

@login_required
def delete_course(request, course_id):
    if request.method == "POST":
        user_course = UserCourse.objects.filter(user=request.user, course_id=course_id)
        if user_course.exists():
            user_course.delete()
            messages.success(request, "Course removed successfully.")
        return redirect('users:profile')
    
@login_required
def delete_group(request, group_id):
    if request.method == "POST":
        user_group = UserGroup.objects.filter(user=request.user, group_id=group_id)
        if user_group.exists():
            user_group.delete()
            messages.success(request, "Study group removed successfully.")
        return redirect('users:profile')