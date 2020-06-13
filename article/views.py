from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from login.models import*
from .forms import *
from django.core.paginator import Paginator
from django.db.models.functions import Lower


def display(request, id):
    context = {}
    categories  = Category.objects.all()
    temp = {}
    for c in categories:
        temp[c] = SubCategory.objects.filter(category=c)
    context['categories'] = temp
    if request.session.has_key('user'):
        user = UserCredentials.objects.get(email=request.session['user'])
        userd = UserDetails.objects.get(user=user)
        context['username'] = user
        context['userd'] = userd
    subcat = SubCategory.objects.get(id=id)
    articles = Article.objects.filter(subcategory=subcat).order_by(Lower('title'))
    paginator = Paginator(articles, 6)
    page = request.GET.get('page') if request.GET.get('page') else 1
    context['articles'] = paginator.get_page(page)
    pages = {i:'href=/article/display-sub1?page='+str(i)+' class=tran3s' for i in paginator.page_range}
    pages[int(page)] = 'href=# class=tran3s'
    context['pages'] = pages
    
    return render(request, 'blog.html', context)

def displayart(request, id):
    context = {}
    categories  = Category.objects.all()
    temp = {}
    for c in categories:
        temp[c] = SubCategory.objects.filter(category=c)
    context['categories'] = temp
    context['article'] = Article.objects.get(id=id)
    if request.session.has_key('user'):
        user = UserCredentials.objects.get(email=request.session['user'])
        userd = UserDetails.objects.get(user=user)
        context['username'] = user
        context['userd'] = userd    
    context['articles'] = Article.objects.filter(subcategory=context['article'].subcategory).order_by('created_on')
    context['comments'] = Comment.objects.filter(article=context['article'])
    if request.method == 'POST':
        author = request.POST['name']
        # phone = request.POST['phone']
        email = request.POST['email']
        body = request.POST['comment']
        comment = Comment(author=author, email=email, body=body, article=context['article'])
        comment.save()
    return render(request, 'blog-details.html', context)

def newarticle(request):
    categories = Category.objects.all()
    template = 'category.html'
    temp = {}
    context = {}
    user = UserCredentials.objects.get(email=request.session['user'])
    userd = UserDetails.objects.get(user=user)
    context['username'] = user
    context['userd'] = userd
    for c in categories:
        temp[c] = SubCategory.objects.filter(category=c)
        context['categories'] = temp
    return render(request, template, context)

def addarticle(request,id):
    context = {}
    categories  = Category.objects.all()
    temp = {}
    for c in categories:
        temp[c] = SubCategory.objects.filter(category=c)
    context['categories'] = temp
    if request.method == 'POST':
        subcat = SubCategory.objects.get(id=id)
        title = request.POST['title']
        body = request.POST['body']
        form = ArticleImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
        youtube = request.POST['youtube']
        instructor = Teacher.objects.get(
            userd = UserDetails.objects.get(
                user = UserCredentials.objects.get(email=request.session['user'])
            )
        )
        article = Article(subcategory=subcat, title=title, body=body, image=image, youtube=youtube, instructor=instructor)
        article.save()
        request.session['msg'] = 'Article Added Successfully'
        return redirect('teacher:teacher')

    if request.session.has_key('teacher'):   
        if request.session.has_key('user'):
            template = 'article.html'
            user = UserCredentials.objects.get(email=request.session['user'])
            userd = UserDetails.objects.get(user=user)
            context['username'] = user
            context['userd'] = userd
            context['form'] = ArticleImageForm()
            context['addarticle'] = True
            return render(request, template, context=context)
    else:
        template = 'error.html'
        context1 = {
            'gen_error': 'NOT Teacher',
            'head_error': 'AUTHORISATION FAILED',
            'desc': 'You are not authorised to view this page'
        }
        context.update(context1)
        if request.session.has_key('user'):
            user = UserCredentials.objects.get(email=request.session['user'])
            userd = UserDetails.objects.get(user=user)
            context['username'] = user
            context['userd'] = userd
            context['Teacher'] = True
        return render(request, template, context)


def editarticle(request):
    context = {}
    categories  = Category.objects.all()
    temp = {}
    for c in categories:
        temp[c] = SubCategory.objects.filter(category=c)
    context['categories'] = temp
    template = 'category.html'
    user = UserCredentials.objects.get(email=request.session['user'])
    userd = UserDetails.objects.get(user=user)
    context['username'] = user
    context['userd'] = userd
    context['form'] = ArticleImageForm()
    context['article'] = True
    temp = {}
    for c in categories:
        temp1 = {}
        sub = SubCategory.objects.filter(category=c)
        for s in sub:
            temp1[s] = Article.objects.filter(subcategory=s)
        temp[c] = temp1
    context['articles'] = temp
    return render(request, template, context=context)

def edit(request,id):
    context = {}
    categories  = Category.objects.all()
    temp = {}
    for c in categories:
        temp[c] = SubCategory.objects.filter(category=c)
    context['categories'] = temp
    if request.method == 'POST':
        article = Article.objects.get(id=id)
        article.title = request.POST['title']
        article.body = request.POST['body']
        form = ArticleImageForm(request.POST, request.FILES)
        if form.is_valid():
            article.image = form.cleaned_data['image']
        article.youtube = request.POST['youtube']
        article.save()
        request.session['msg'] = 'Article Edited Successfully'
        return redirect('teacher:teacher')

    if request.session.has_key('teacher'):   
        if request.session.has_key('user'):
            template = 'article.html'
            user = UserCredentials.objects.get(email=request.session['user'])
            userd = UserDetails.objects.get(user=user)
            context['username'] = user
            context['userd'] = userd
            context['form'] = ArticleImageForm()
            context['editarticle'] = True
            context['article'] = Article.objects.get(id=id)
            return render(request, template, context=context)
    else:
        template = 'error.html'
        context1 = {
            'gen_error': 'NOT Teacher',
            'head_error': 'AUTHORISATION FAILED',
            'desc': 'You are not authorised to view this page'
        }
        context.update(context1)
        if request.session.has_key('user'):
            user = UserCredentials.objects.get(email=request.session['user'])
            userd = UserDetails.objects.get(user=user)
            context['username'] = user
            context['userd'] = userd
            context['Teacher'] = True
        return render(request, template, context)


def newcategory(request):
    context = {}
    categories  = Category.objects.all()
    temp = {}
    for c in categories:
        temp[c] = SubCategory.objects.filter(category=c)
    context['categories'] = temp
    if request.method == 'POST':
        name = request.POST['catname']
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            pic = form.cleaned_data['image']
        else:
            pic = None
        cat = Category(name=name, image=pic)
        cat.save()
        request.session['msg'] = 'Category Added'
        return redirect('teacher:teacher')
    template = 'category.html'
    context['addcategory']=True
    user = UserCredentials.objects.get(email=request.session['user'])
    userd = UserDetails.objects.get(user=user)
    context['username'] = user
    context['userd'] = userd
    context['form'] = ImageForm()
    return render(request, template, context)


def newsubcategory(request):
    context = {}
    categories  = Category.objects.all()
    temp = {}
    for c in categories:
        temp[c] = SubCategory.objects.filter(category=c)
    context['categories'] = temp
    if request.method == 'POST':
        name = request.POST['subcatname']
        category = request.POST['category']
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            pic = form.cleaned_data['image']
        else:
            pic = None
        subcat = SubCategory(category=Category.objects.get(id=category), name=name, image=pic)
        subcat.save()
        request.session['msg'] = 'SubCategory Added'
        return redirect('teacher:teacher')

    template = 'category.html'
    context1 = {'addcategory':True,'addsubcategory':True}
    context.update(context1)
    user = UserCredentials.objects.get(email=request.session['user'])
    userd = UserDetails.objects.get(user=user)
    context['username'] = user
    context['userd'] = userd
    context['category'] = Category.objects.all()
    context['form'] = ImageForm()
    return render(request, template, context)