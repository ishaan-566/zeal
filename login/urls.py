from django.urls import path
from .views import*

app_name = 'login'

urlpatterns = [
    path('', home, name='home'),
    # path('email', email, name='email'),
    path('login', login, name='login'),
    path('signup', signup, name='signup'),
    path('logout', logout, name='logout'),
    path('site-admin', admin, name='admin'),
    path('subscribe', subscribe, name='subscribe'),
    path('category', category, name='category'),
    path('category-<id>', subcategory, name='subcategory'),
    path('contact-us', contact, name='contact'),
    path('about-us', about, name='about'),
]