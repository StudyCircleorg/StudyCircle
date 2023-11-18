from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # URL patterns for the core app
    path('users/', include('users.urls')),  # URL patterns for the users app
]