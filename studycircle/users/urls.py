from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile_view, name="profile"),
    path("edit_profile", views.edit_profile_view, name="edit_profile"),
    path('add_course/', views.add_course_view, name='add_course'),
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
    path('delete_group/<int:group_id>/', views.delete_group, name='delete_group'),
]