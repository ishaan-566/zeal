from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from article.models import*
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.db.models.functions import Lower

# def error_404_view(request, exception):
#     context = {}
#     print(exception, '************************')
#     if request.session.has_key('user'):
#         user = UserCredentials.objects.get(email=request.session['user'])
#         userd = UserDetails.objects.get(user=user)
#         context['username'] = user
#         context['userd'] = userd
#     categories  = Category.objects.all()
#     temp = {}
#     for c in categories:
#         temp[c] = SubCategory.objects.filter(category=c)
#     context['categories'] = temp
#     return render(request,'404.html',context)


def contact(request):
    template = 'contact-us.html'
    context = {}
    if request.session.has_key('user'):
        user = UserCredentials.objects.get(email=request.session['user'])
        userd = UserDetails.objects.get(user=user)
        context['username'] = user
        context['userd'] = userd
    categories  = Category.objects.all()
    temp = {}
    for c in categories:
        temp[c] = SubCategory.objects.filter(category=c)
    context['categories'] = temp
    if request.method=='POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        message = request.POST['message']
        body = "Hi {}<br>{}<br> your message<br>\"<i>{}</i>\"<br> has been recorded successfully.".format(name, phone, message)
        try:
            email = EmailMessage(
                'Zeal Message Delivered',
                body,
                '',
                [email],
            )
            email.send()
            email.content_subtype = "html"
        except:
            pass
    return render(request, template, context)

def email(request):
    email = EmailMessage(
        'Test',
        'this is a test mail',
        '',
        ['ishaanaggarwal4748@gmail.com'],
    )
    email.send()
    return HttpResponse("Success")

def subscribe(request):
    if request.method == 'POST':
        name = request.POST['name'] if 'name' in request.POST else "Learner"
        email = request.POST['email']
        phone = request.POST['phone'] if 'phone' in request.POST else "0"
        obj = MailLetter(name=name, email=email, phone=phone)
        obj.save()
        body = "Hello "+name+",<br>Your Subscription to our mail letter has been added successfully"
        try:
            email = EmailMessage(
                'Zeal Mail Letter Subscription',
                body,
                '',
                [email],
            )
            email.content_subtype = "html"
            email.send()
        except:
            pass
        
    return redirect('login:home')

def about(request):
    template = 'about-us.html'
    context = {}
    if request.session.has_key('user'):
        user = UserCredentials.objects.get(email=request.session['user'])
        userd = UserDetails.objects.get(user=user)
        context['username'] = user
        context['userd'] = userd
        if request.session.has_key('teacher'):
            context['teacher'] = Teacher.objects.get(userd=userd)
    categories  = Category.objects.all()
    temp = {}
    for c in categories:
        temp[c] = SubCategory.objects.filter(category=c)
    context['categories'] = temp
    context['teachers'] = Teacher.objects.all()
    return render(request, template, context)

def home(request):
    template = 'index.html'
    context = {}
    if request.session.has_key('user'):
        user = UserCredentials.objects.get(email=request.session['user'])
        userd = UserDetails.objects.get(user=user)
        context['username'] = user
        context['userd'] = userd
        if request.session.has_key('teacher'):
            context['teacher'] = Teacher.objects.get(userd=userd)
    categories  = Category.objects.all()
    temp = {}
    for c in categories:
        temp[c] = SubCategory.objects.filter(category=c)
    context['categories'] = temp
    context['features'] = Category.objects.filter(feature=True)
    context['teachers'] = Teacher.objects.all()
    return render(request, template, context)

def logout(request):
    request.session.flush()
    return redirect('login:home')

def login(request):
    if request.method == 'POST':
        context = {}
        categories  = Category.objects.all()
        temp = {}
        for c in categories:
            temp[c] = SubCategory.objects.filter(category=c)
        context['categories'] = temp
        error = None
        email = request.POST['email']
        password = request.POST['password']
        try:
            temp = UserCredentials.objects.get(email=email)    
            cpassword = temp.password
        except:
            error = 'Email Doesnt exist'
            context['error'] = error
            return render(request, 'index.html', context=context)

        if password == cpassword:
            user = UserDetails.objects.get(user=temp)
            request.session['user'] = user.user.email
            if temp.admin:
                request.session['admin'] = True
            if temp.teacher:
                request.session['teacher'] = True
            return redirect('login:home')
        else:
            error = 'Password didnt match'
            context['error'] = error
            return render(request, 'index.html', context)


def signup(request):
    context = {}
    categories  = Category.objects.all()
    temp = {}
    for c in categories:
        temp[c] = SubCategory.objects.filter(category=c)
    context['categories'] = temp
    if request.session.has_key('user'):
        return redirect('login:home')
    if request.method == 'POST':
        error = None
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        fname = request.POST['fname']
        mname = request.POST['mname']
        lname = request.POST['lname']
        try:
            temp = UserCredentials.objects.get(email=email)
            error = 'Email already exist'
            context['error'] = error
            return render(request, 'sign-up.html', context)
        except:
            pass
        if password == cpassword:
            user = UserCredentials(email=email, password=password)
            user.save()
        else:
            error = 'Password didnt match'
            context['error'] = error
            return render(request, 'sign-up.html', context)
        
        user_d = UserDetails(user=user, fname=fname, mname=mname, lname=lname)
        user_d.save()
        context['msg'] = 'User Created Successfully Proceed To Login'
        return render(request, 'index.html', context)

    return render(request,'sign-up.html',context)

def admin(request):
    template = 'admin.html'
    context = {}
    categories  = Category.objects.all()
    temp = {}
    for c in categories:
        temp[c] = SubCategory.objects.filter(category=c)
    context['categories'] = temp
    if request.session.has_key('admin'):   
        if request.session.has_key('user'):
            user = UserCredentials.objects.get(email=request.session['user'])
            userd = UserDetails.objects.get(user=user)
            context['username'] = user
            context['userd'] = userd
            context['admin'] = True
            context['error'] = request.session['error'] if request.session.has_key('error') else None
            request.session['error'] = None
            context['msg'] = request.session['msg'] if request.session.has_key('msg') else None
            request.session['msg'] = None
        return render(request, template, context)
    else:
        template = 'error.html'
        context1 = {
            'gen_error': 'NOT ADMIN',
            'head_error': 'AUTHORISATION FAILED',
            'desc': 'You are not authorised to view this page'
        }
        context.update(context1)
        if request.session.has_key('user'):
            user = UserCredentials.objects.get(email=request.session['user'])
            userd = UserDetails.objects.get(user=user)
            context['username'] = user
            context['userd'] = userd
            context['admin'] = True
        return render(request, template, context)

def category(request):
    template='category-list.html'
    context = {}
    if request.session.has_key('user'):
        user = UserCredentials.objects.get(email=request.session['user'])
        userd = UserDetails.objects.get(user=user)
        context['username'] = user
        context['userd'] = userd
    categories  = Category.objects.all().order_by(Lower('name'))
    paginator = Paginator(categories, 12)
    page = request.GET.get('page') if request.GET.get('page') else 1
    context['categories2'] = paginator.get_page(page)
    pages = {i:'href=/category?page='+str(i)+' class=tran3s' for i in paginator.page_range}
    pages[int(page)] = 'href=# class=tran3s'
    context['pages'] = pages
    temp = {}
    for c in categories:
        temp[c] = SubCategory.objects.filter(category=c)
    context['categories'] = temp
    return render(request, template, context)

def subcategory(request, id):
    context = {}
    categories  = Category.objects.all()
    temp = {}
    for c in categories:
        temp[c] = SubCategory.objects.filter(category=c)
    context['categories'] = temp
    try:
        subcategory = SubCategory.objects.filter(category=Category.objects.get(id=id)).order_by(Lower('name'))
        paginator = Paginator(subcategory, 9)
        page = request.GET.get('page') if request.GET.get('page') else 1
        context['subcategory'] = paginator.get_page(page)
        pages = {i:'href=/category-'+id+'?page='+str(i)+' class=tran3s' for i in paginator.page_range}
        pages[int(page)] = 'href=# class=tran3s'
        context['pages'] = pages
        # context['courses'] = Article.objects.filter(instructor=teacher).order_by('-created_on')
    except:
        context1 = {
            'gen_error': 'NOT FOUND',
            'head_error': 'CATEGORY NOT FOUND',
            'desc': 'The given Category ID is not Valid'
        }
        context.update(context1)
        if request.session.has_key('user'):
            user = UserCredentials.objects.get(email=request.session['user'])
            userd = UserDetails.objects.get(user=user)
            context['username'] = user
            context['userd'] = userd
        return render(request, 'error.html', context)
    
    template = 'subcategory-list.html'
    if request.session.has_key('user'):
        user = UserCredentials.objects.get(email=request.session['user'])
        userd = UserDetails.objects.get(user=user)
        context['username'] = user
        context['userd'] = userd
    context['subcategory'] = subcategory
    return render(request, template, context)