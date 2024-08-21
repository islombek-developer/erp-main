from django import forms
from .models import Homework,Davomat

class HomeworkForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea())
    homework_file = forms.FileField(widget=forms.FileInput())


class DavomatForm(forms.ModelForm):
    class Meta:
        model = Davomat
        fields = ['team', 'student', 'status']  # Include the fields you want in the form
        widgets = {
            'team': forms.Select(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }