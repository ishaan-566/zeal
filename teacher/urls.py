from django.urls import path
from .views import*

app_name = 'teacher'

urlpatterns = [
    path('', teacher, name='teacher'),
    path('@<id>', profile, name='profile'),
    path('article', newarticle, name='newarticle'),
    path('editarticle', editarticle, name='editarticle'),
    path('category', newcategory, name='newcategory'),
    path('subcategory', newsubcategory, name='newsubcategory'),
]