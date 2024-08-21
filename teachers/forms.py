from django import forms
from students.models import Davomat
class CreateLessonForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput({"class":"form-control"}))

class DavomatForm(forms.ModelForm):
    class Meta:
        model = Davomat
        fields = [ 'student', 'status']  # Include the fields you want in the form
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }