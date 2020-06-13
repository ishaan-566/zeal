from django.db import models
from django.urls import reverse

# Create your models here.
class UserCredentials(models.Model):
    email = models.EmailField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    admin = models.BooleanField(default=False)
    teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class UserDetails(models.Model):
    user = models.ForeignKey('UserCredentials', on_delete=models.CASCADE)
    fname = models.CharField(max_length=20)
    mname = models.CharField(max_length=20, blank=True)
    lname = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.email + "--" +self.fname

class Teacher(models.Model):
    userd = models.ForeignKey('UserDetails', on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    facebook = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    website = models.CharField(max_length=100, blank=True)
    about = models.TextField()
    pic = models.ImageField(upload_to='teachers/')

    def __str__(self):
        return self.userd.user.email + "--" +self.userd.fname

    def get_profile_url(self):
        return reverse('teacher:profile', args=[self.id])


class MailLetter(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)