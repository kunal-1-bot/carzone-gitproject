from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from contacts.models import Contact
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = auth.authenticate(username = username , password = password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, ' you are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, ' Invalid login credentials')
            return redirect('login')
    return render(request,'accounts/login.html')

def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'username already exists! !')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=firstname,last_name=lastname, email= email ,username=username,password=password)
                    auth.login(request,user)
                    messages.success(request, 'you are now loged in.')
                    return redirect('dashboard')
                    user.save()
                    messages.success(request, 'you are registered successfully!!')
                    return redirect('login')
        else:
            messages.error(request, 'password do not match')


    return render(request,'accounts/register.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'you are sucessfully logout')
        return redirect('home')
@login_required(login_url = 'login')
def dashboard(request):
    user_inquiry = Contact.objects.order_by('-create_date').filter(user_id = request.user.id)
    data = {
        'inquires': user_inquiry
    }
    return render(request,'accounts/dashboard.html', data)
