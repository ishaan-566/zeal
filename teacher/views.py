from django.shortcuts import render, redirect
from login.models import *
from article.models import*

def teacher(request):
    template = 'teacher.html'
    context = {}
    categories  = Category.objects.all()
    temp = {}
    for c in categories:
        temp[c] = SubCategory.objects.filter(category=c)
    context['categories'] = temp
    if request.session.has_key('teacher'):   
        if request.session.has_key('user'):
            user = UserCredentials.objects.get(email=request.session['user'])
            userd = UserDetails.objects.get(user=user)
            context['username'] = user
            context['userd'] = userd
            context['error'] = request.session['error'] if request.session.has_key('error') else None
            request.session['error'] = None
            context['msg'] = request.session['msg'] if request.session.has_key('msg') else None
            request.session['msg'] = None
        return render(request, template, context)
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


def profile(request, id):
    context = {}
    categories  = Category.objects.all()
    temp = {}
    for c in categories:
        temp[c] = SubCategory.objects.filter(category=c)
    context['categories'] = temp
    try:
        teacher = Teacher.objects.get(id=id)
        context['displaycourses'] = True
        context['courses'] = Article.objects.filter(instructor=teacher).order_by('-created_on')
    except:
        context1 = {
            'gen_error': 'NOT FOUND',
            'head_error': 'TEACHER NOT FOUND',
            'desc': 'The given Teacher ID is not Valid'
        }
        context.update(context1)
        if request.session.has_key('user'):
            user = UserCredentials.objects.get(email=request.session['user'])
            userd = UserDetails.objects.get(user=user)
            context['username'] = user
            context['userd'] = userd
        return render(request, 'error.html', context)
    
    template = 'teachers-profile.html'
    if request.session.has_key('user'):
        user = UserCredentials.objects.get(email=request.session['user'])
        userd = UserDetails.objects.get(user=user)
        context['username'] = user
        context['userd'] = userd
    context['teacher'] = teacher
    return render(request, template, context)

def newarticle(request):
    context = {}
    categories  = Category.objects.all()
    temp = {}
    for c in categories:
        temp[c] = SubCategory.objects.filter(category=c)
    context['categories'] = temp
    if request.session.has_key('teacher'):   
        if request.session.has_key('user'):
            user = UserCredentials.objects.get(email=request.session['user'])
            userd = UserDetails.objects.get(user=user)
            context = {}
            context['username'] = user
            context['userd'] = userd
            return redirect('article:newarticle')
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
    if request.session.has_key('teacher'):   
        if request.session.has_key('user'):
            user = UserCredentials.objects.get(email=request.session['user'])
            userd = UserDetails.objects.get(user=user)
            context['username'] = user
            context['userd'] = userd
            return redirect('article:editarticle')
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
    if request.session.has_key('teacher'):   
        if request.session.has_key('user'):
            user = UserCredentials.objects.get(email=request.session['user'])
            userd = UserDetails.objects.get(user=user)
            context['username'] = user
            context['userd'] = userd
            return redirect('article:newcategory')
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


def newsubcategory(request):
    context = {}
    categories  = Category.objects.all()
    temp = {}
    for c in categories:
        temp[c] = SubCategory.objects.filter(category=c)
    context['categories'] = temp
    if request.session.has_key('teacher'):   
        if request.session.has_key('user'):
            user = UserCredentials.objects.get(email=request.session['user'])
            userd = UserDetails.objects.get(user=user)
            context['username'] = user
            context['userd'] = userd
            return redirect('article:newsubcategory')
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
