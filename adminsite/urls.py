from django.urls import path
from .views import*

app_name = 'adminsite'

urlpatterns = [
    path('teacher', teacher, name='teacher'),
    path('edit-teachers', editteachers, name='editteachers'),
    path('feature', feature, name='features'),
    path('mailletter', mailletter, name='mailletter'),
    path('feat<opr><id>', feat, name='feat'),
    path('edit-teacher/<id>', editteacher, name='edit-teacher'),
]