from django import forms
from students.models import Davomat ,Lesson

class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = [ 'title', 'homework_status', 'lesson_file']
    
    title = forms.CharField(widget=forms.TextInput({'class': 'form-control'}))

class DavomatForm(forms.ModelForm):
    class Meta:
        model = Davomat
        fields = [ 'student', 'status'] 
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }