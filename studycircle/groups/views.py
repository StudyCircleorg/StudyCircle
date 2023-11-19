from django.shortcuts import get_object_or_404, redirect, render
from .forms import GroupForm
from .models import Group, GroupCourse
from courses.models import Course

# Create your views here.
def create_group_view(request):

    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            new_group = form.save(commit=False)
            new_group.save()

            department = form.cleaned_data.get('course_department')
            level = form.cleaned_data.get('course_level')

            course = Course.objects.filter(department=department, level=level).first()
            if course:
                # Create a GroupCourse instance
                GroupCourse.objects.create(group=new_group, course=course)
            # Additional logic after creating the group, such as redirecting to the group's detail page
            return redirect('group_detail', pk=new_group.pk)
    else:
        form = GroupForm()

    return render(request, 'groups/create_group.html', {
        'form': form
        })

def group_detail_view(request, pk):
    # Get the group by pk (primary key) or return 404 if not found
    group = get_object_or_404(Group, pk=pk)

    # You could also include logic to get the related courses and users
    # For example:
    courses = group.groupcourse_set.all()
    members = group.usergroup_set.all()

    # If you have a many-to-many relationship directly with Course and User models,
    # it would be something like:
    courses = group.courses.all()
    members = group.users.all()

    # If the UserGroup model is used to manage memberships, you might need to query it like this:
    # members = UserGroup.objects.filter(group=group).select_related('user')

    # Pass the group and any other related information to the template
    return render(request, 'groups/group_detail.html', {
        'group': group,
        'courses': courses,  
        'members': members,  
    })
