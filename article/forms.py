from .models import Category, Article
from django import forms
 
class ImageForm(forms.ModelForm): 
  
    class Meta: 
        model = Category 
        fields = ['image']

class ArticleImageForm(forms.ModelForm): 
  
    class Meta: 
        model = Article 
        fields = ['image']