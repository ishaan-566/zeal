from django.urls import path
from .views import*

app_name = 'article'

urlpatterns = [
    path('newarticle', newarticle, name='newarticle'),
    path('editarticle', editarticle, name='editarticle'),
    path('editarticle@<id>', edit, name='edit'),
    path('addarticle-sub<id>', addarticle, name='addarticle'),
    path('display-sub<id>', display, name='display'),
    path('display-article<id>', displayart, name='displayart'),
    path('newcategory', newcategory, name='newcategory'),
    path('newsubcategory', newsubcategory, name='newsubcategory'),
]