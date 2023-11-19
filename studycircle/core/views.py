from django.utils import timezone
from django.shortcuts import render
from .models import Session
from django.contrib.auth.decorators import login_required
from groups.models import UserGroup

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        # The user is authenticated
        user_groups = UserGroup.objects.filter(user=request.user).select_related('group')

        # Prepare group details for the template
        group_details = [{
            'name': ug.group.name,
            'meeting_date': ug.group.meeting_date,
            'meeting_time': ug.group.meeting_time,
            'location': ug.group.get_location_display(),
            'session_type': ug.group.get_session_type_display(),
            'dynamics': ug.group.get_dynamics_display()
        } for ug in user_groups]
    else:
        # The user is not authenticated
        user_groups = []
        group_details = []

    return render(request, 'core/index.html', {
        'user_groups': user_groups,
        'group_details': group_details,
        'is_authenticated': request.user.is_authenticated  # Pass authentication status to the template
    })
