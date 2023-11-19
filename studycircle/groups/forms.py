from django import forms
from django.forms import formset_factory
from .models import Group
from courses.models import Course

class GroupForm(forms.ModelForm):
    # Define form fields corresponding to the Group model fields
    # Additional fields like for Course can be added if they are part of the Group model

    course_department = forms.ModelChoiceField(
        queryset=Course.objects.values_list('department', flat=True).distinct(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Course Department"
    )

    course_level = forms.ModelChoiceField(
        queryset=Course.objects.values_list('level', flat=True).distinct(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Course Level"
    )

    session_type_choices = [
        ('exam_review', 'Exam Review'),
        ('collab_learning', 'Collaborative Learning'),
        ('quiet_study', 'Quiet Study'),
        ('discuss_debate', 'Discussion and Debate'),
    ]

    dynamics_choices = [
        ('social', 'Social'),
        ('intensive', 'Intensive Study'),
        ('mixed', 'Mixed (Study + Breaks)'),
        ('flexible', 'Flexible'),
    ]

    session_type = forms.MultipleChoiceField(
        choices=session_type_choices, 
        widget=forms.CheckboxSelectMultiple,
        label="Session Types"
    )
    
    dynamics = forms.MultipleChoiceField(
        choices=dynamics_choices, 
        widget=forms.CheckboxSelectMultiple,
        label="Group Dynamics Preference"
    )

    class Meta:
        model = Group
        fields = ['name', 'meeting_times', 'days', 'session_type', 'dynamics', 'location', 'course_department', 'course_level']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your group name'}),
            'meeting_times': forms.Textarea(attrs={'placeholder': 'Select first meeting date and time'}),
            'days': forms.TextInput(attrs={'placeholder': 'Add more meetings'}),
            'location': forms.TextInput(attrs={'placeholder': 'Select a location from drop-down menu'}),
        }

    def save(self, commit=True):
        # Here you would handle QR code generation before saving the group
        instance = super(GroupForm, self).save(commit=False)
        if commit:
            instance.save()  # Save the instance
            self.save_m2m()  # Save many-to-many data for the form
            # Handle QR code generation after saving the group
            # instance.qr_code = your_qr_code_generation_logic(instance)
            # instance.save()  # Re-save the instance with QR code
        return instance
    
    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['course_department'].queryset = Course.objects.values_list('department', flat=True).distinct()
        self.fields['course_level'].queryset = Course.objects.values_list('level', flat=True).distinct() 