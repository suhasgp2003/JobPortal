from django import forms
from .models import Job, Application


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'location', 'job_type', 'salary', 'description']


class ApplicationForm(forms.ModelForm):  # <-- Only one form
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']

        widgets = {
            'resume': forms.ClearableFileInput(attrs={'class': 'portal-field'}),
            'cover_letter': forms.Textarea(attrs={'class': 'portal-field', 'rows': 6}),
        }
