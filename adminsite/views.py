from django.shortcuts import render, redirect
from django.http import HttpResponse
from login.models import *
from .forms import ImageForm
from article.models import*
from django.core.mail import EmailMessage

def mailletter(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        body = request.POST['body']
        emailobj = MailLetter.objects.all()
        if 'name' in request.POST:
            for e in emailobj:
                try:
                    email = EmailMessage(
                        subject,
                        body.format(name=e.name),
                        '',
                        [e.email],
                    )
                    email.content_subtype = "html"
                    email.send()
                except:
                    pass
        else:
            try:
                email = EmailMessage(
                    subject,
                    body,
                    '',
                    [e.email for e in emailobj]
                )
            except:
                pass
            email.content_subtype = "html"
            email.send()

        return redirect('login:admin')
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
        return render(request, 'mailletter.html', context)

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

def feat(request, opr, id):
    context = {}
    categories  = Category.objects.all()
    temp = {}
    for c in categories:
        temp[c] = SubCategory.objects.filter(category=c)
    context['categories'] = temp
    if request.session.has_key('admin'):
        feature = Category.objects.get(id=id)
        if opr == 'delete':
            feature.feature = False
        else:
            feature.feature = True
        feature.save()
        return redirect('adminsite:features')


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

def feature(request):
    features = Category.objects.filter(feature=True)
    template = 'features.html'
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
            context['form'] = ImageForm()
            context['features'] = features
            context['contfeat'] = Category.objects.filter(feature=False)
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

def teacher(request):
    if request.method == 'POST':
        error = None
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        fname = request.POST['fname']
        mname = request.POST['mname']
        lname = request.POST['lname']
        if 'admin' in request.POST:
            admin = True
        else:
            admin = False
        designaition = request.POST['designation']
        facebook = request.POST['facebook']
        twitter = request.POST['twitter']
        linkedin = request.POST['linkedin']
        instagram = request.POST['instagram']
        website = request.POST['website']
        about = request.POST['about']
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            pic = form.cleaned_data['pic']
        else:
            pic = None
        
        try:
            temp = UserCredentials.objects.get(email=email)
            error = 'Teacher Exist'
            request.session['error'] = error
            return redirect('adminsite:teacher')
        except:
            user = UserCredentials(email=email, password=password, admin=admin, teacher=True)
            user.save()
        user_d = UserDetails(user=user, fname=fname, mname=mname, lname=lname)
        user_d.save()
        teacher = Teacher(
            userd = user_d,
            designation = designaition,
            facebook = facebook,
            twitter = twitter,
            linkedin = linkedin,
            instagram = instagram,
            website = website,
            about = about,
            pic = pic
        )
        teacher.save()
        request.session['msg'] = 'Instructor added successfully'
        return redirect('login:admin')


    template = 'teachers-profile.html'
    if request.session.has_key('admin'):   
        if request.session.has_key('user'):
            user = UserCredentials.objects.get(email=request.session['user'])
            userd = UserDetails.objects.get(user=user)
            context = {'addteacher': True}
            categories  = Category.objects.all()
            temp = {}
            for c in categories:
                temp[c] = SubCategory.objects.filter(category=c)
            context['categories'] = temp
            context['username'] = user
            context['userd'] = userd
            context['admin'] = True
            context['form'] = ImageForm()
            context['error'] = request.session['error'] if request.session['error'] else None
            request.session['error'] = None
            context['msg'] = request.session['msg'] if request.session['msg'] else None
            request.session['msg'] = None
        return render(request, template, context)
    else:
        template = 'error.html'
        context = {
            'gen_error': 'NOT ADMIN',
            'head_error': 'AUTHORISATION FAILED',
            'desc': 'You are not authorised to view this page'
        }
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
            context['admin'] = True
        return render(request, template, context)

def editteachers(request):
    teachers = Teacher.objects.all()
    template = 'teachers.html'
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
            context['form'] = ImageForm()
            context['teachers'] = teachers
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


def editteacher(request, id):
    if request.method == 'POST':
        error = None
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        fname = request.POST['fname']
        mname = request.POST['mname']
        lname = request.POST['lname']
        if 'admin' in request.POST:
            admin = True
        else:
            admin = False
        designaition = request.POST['designation']
        facebook = request.POST['facebook']
        twitter = request.POST['twitter']
        linkedin = request.POST['linkedin']
        instagram = request.POST['instagram']
        website = request.POST['website']
        about = request.POST['about']
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            pic = form.cleaned_data['pic']
        
        temp = UserCredentials.objects.get(email=email)
        if not temp.password == password:
            temp.password == password
            temp.save()
        user_d = UserDetails.objects.get(user=temp)
        user_d.fname = fname
        user_d.mname = mname
        user_d.lname = lname
        user_d.save()
        teacher = Teacher.objects.get(userd=user_d)
        teacher.designation = designaition
        teacher.facebook = facebook
        teacher.twitter = twitter
        teacher.linkedin = linkedin
        teacher.instagram = instagram
        teacher.website = website
        teacher.about = about
        teacher.pic = pic
        teacher.save()
        request.session['msg'] = 'Instructor edited successfully'
        return redirect('login:admin')


    template = 'teachers-profile.html'
    if request.session.has_key('admin'):   
        if request.session.has_key('user'):
            user = UserCredentials.objects.get(email=request.session['user'])
            userd = UserDetails.objects.get(user=user)
            context = {'editteacher': True}
            categories  = Category.objects.all()
            temp = {}
            for c in categories:
                temp[c] = SubCategory.objects.filter(category=c)
            context['categories'] = temp
            context['username'] = user
            context['userd'] = userd
            context['admin'] = True
            context['form'] = ImageForm()
            context['error'] = request.session['error'] if request.session['error'] else None
            request.session['error'] = None
            context['msg'] = request.session['msg'] if request.session['msg'] else None
            request.session['msg'] = None
            context['teacher'] = Teacher.objects.get(id=id)
        return render(request, template, context)
    else:
        template = 'error.html'
        context = {
            'gen_error': 'NOT ADMIN',
            'head_error': 'AUTHORISATION FAILED',
            'desc': 'You are not authorised to view this page'
        }
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
            context['admin'] = True
        return render(request, template, context)