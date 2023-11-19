from django import forms
from .models import Group
from courses.models import Course

class GroupForm(forms.ModelForm):
    # Adding a field to select a course
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Course"
    )

    class Meta:
        model = Group
        fields = ['name', 'meeting_date', 'meeting_time', 'session_type', 'dynamics', 'location', 'course', 'bio']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your group name'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write about your group'}),
            'meeting_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'meeting_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'session_type': forms.Select(attrs={'class': 'form-control'}),
            'dynamics': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        # Set the queryset for the course field
        self.fields['course'].queryset = Course.objects.all()