from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('groups/create/', views.create_group_view, name='create_group'),
    path('<int:pk>/', views.group_detail_view, name='group_detail'),
    path('groups/join/<int:group_id>/', views.join_group_view, name='join_group'),
    path('groups/leave/<int:group_id>/', views.leave_group_view, name='leave_group'),
     path('groups/search/', views.group_search_view, name='group_search'),
]