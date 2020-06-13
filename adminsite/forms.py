from login.models import Teacher
from django import forms
 
class ImageForm(forms.ModelForm): 
  
    class Meta: 
        model = Teacher 
        fields = ['pic']