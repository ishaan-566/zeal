from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='categories/')
    feature = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='categories/subcategories/')

    def __str__(self):
        return self.name

    def newarticle(self):
        return reverse('article:addarticle', args=[self.id])
    
    def get_absolute_url(self):
        return reverse('article:display', args=[self.id])

class Article(models.Model):
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/subcategories/article/')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    youtube = models.CharField(max_length=30, blank=True)
    instructor = models.ForeignKey('login.Teacher', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

    def editarticle(self):
        return reverse('article:edit', args=[self.id])

class Comment(models.Model):
    author = models.CharField(max_length=60)
    email = models.EmailField(max_length=100, blank=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)