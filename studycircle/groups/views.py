from django.shortcuts import get_object_or_404, redirect, render
from .forms import GroupForm
from .models import Group, GroupCourse, UserGroup
from courses.models import Course
from django.db.models import Q

# Create your views here.
def create_group_view(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            new_group = form.save(commit=False)
            new_group.save()  # Save the group to get an id

            # Get the selected course from the form
            selected_course = form.cleaned_data.get('course')

            # Create a GroupCourse instance to link the group with the course
            GroupCourse.objects.create(group=new_group, course=selected_course)

            # Add the user who created the group to the group's members
            UserGroup.objects.create(user=request.user, group=new_group)

            # Redirect to group detail or another appropriate page
            return redirect('groups:group_detail', pk=new_group.pk)
    else:
        form = GroupForm()

    return render(request, 'groups/create_group.html', {
        'form': form
    })

def group_detail_view(request, pk):
    # Get the group by pk (primary key) or return 404 if not found
    group = get_object_or_404(Group, pk=pk)
    
    # Fetching related courses through the GroupCourse model
    group_courses = group.groupcourse_set.all()
    courses = [gc.course for gc in group_courses]

    # Fetching related users through the UserGroup model
    user_groups = group.usergroup_set.all()
    members = [ug.user for ug in user_groups]

    already_member = UserGroup.objects.filter(user=request.user, group=group).exists()

    # Pass the group and any other related information to the template
    return render(request, 'groups/group_detail.html', {
        'group': group,
        'courses': courses,  # Pass courses, not GroupCourse objects
        'members': members,  # Pass User instances
        'already_member': already_member 
    })

def join_group_view(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        # Add the user to the group's members
        UserGroup.objects.get_or_create(user=request.user, group=group)
        return redirect('group_detail', pk=group_id)

    # You might want to check if the user is already a member and show a message or redirect.
    already_member = UserGroup.objects.filter(user=request.user, group=group).exists()

    return redirect('group_detail', pk=group_id)

def leave_group_view(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        UserGroup.objects.filter(user=request.user, group=group).delete()
        # Redirect to a confirmation page or back to the group list
        return redirect('core:index')

    # You can include a confirmation dialog or page before finalizing the leave action
    return render(request, 'groups/confirm_leave.html', {
        'group': group
    })

def group_search_view(request):
    # Initialize an empty queryset for groups
    groups = Group.objects.none()

    # Get search query and filter options from request
    search_query = request.GET.get('search', '')
    filter_dynamics = request.GET.get('dynamics', '')
    filter_location = request.GET.get('location', '')

    # Apply filters only if they are provided
    if filter_dynamics:
        groups = groups.filter(dynamics=filter_dynamics)

    if filter_location:
        groups = groups.filter(location=filter_location)

    # Apply the search query filter if it's provided
    if search_query:
        groups = Group.objects.filter(name__icontains=search_query)

    # Get dynamics and locations for the filter options
    dynamics_choices = Group._meta.get_field('dynamics').choices
    location_choices = Group._meta.get_field('location').choices

    return render(request, 'groups/group_search.html', {
        'groups': groups,
        'dynamics_choices': dynamics_choices,
        'location_choices': location_choices,
        'search_query': search_query,
        'filter_dynamics': filter_dynamics,
        'filter_location': filter_location,
    })
