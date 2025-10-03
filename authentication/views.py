from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    return render(request,'home.html')

def login_page(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        if not User.objects.filter(username=username).exists:
            messages.error(request, 'invalid username')
            return redirect('/login/')
        
        user = authenticate(username=username,password=password)
        if user is None:
            messages.error(request,'invalid password')
            return redirect('/login/')
        elif user.is_staff:
            login(request,user)
            return redirect('/post_new/')
        else :
            login(request,user)
        return redirect('/main/')
        
        
    return render(request,'login.html')
        

def register_page(request):
    if request.method == 'POST':
        # first_name =request.POST.get(first_name)  
        first_name=request.POST['first_name']
        last_name =request.POST['last_name']
        username=request.POST['username']
        password=request.POST['password']

        user =User.objects.filter(username=username)

        if user.exists():
            messages.info(request,"User already taken!")
            return redirect('/register/')
        
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        
        user.set_password(password)
        user.save()

        messages.info(request,"Account sucessfully created!")
        return redirect("/login/")
    return render(request, 'register.html')






    





