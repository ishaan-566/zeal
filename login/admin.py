from django.contrib import admin
from .models import *

admin.site.register(UserCredentials)
admin.site.register(UserDetails)
admin.site.register(Teacher)
admin.site.register(MailLetter)