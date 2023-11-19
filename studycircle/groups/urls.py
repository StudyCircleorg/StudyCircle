from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('groups/create/', views.create_group_view, name='create_group'),
     path('groups/<int:pk>/', views.group_detail_view, name='group_detail'),
]