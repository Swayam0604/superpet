from django.shortcuts import render , HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate,logout
from product.models import Product

def home(request):
    return render(request,"index.html")

def contact(request):
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")

# def login(request):
#     return render(request,"login.html")

def register(request):
    if request.method == "GET":
        # form = UserCreationForm()
        form = CustomUserCreationForm()
        return render(request,"register.html",{"form":form})
    elif request.method == "POST":
        # form = UserCreationForm(request.POST)
        message = None
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            message = "User Registration Successful"
        else:
            message = "UserRegistration Failed"
        return render (request,"register.html",{"form":form,"message":message})
    
def user_login(request):
    if request.method == "GET":
        return render (request,'login.html')
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        message = None
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/products')
        message = "Invalid Credentials !!"

        return render (request,'login.html',{"message":message})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')
    
def search(request):
    keyword=request.GET.get("search")
    products=Product.objects.filter(product_name__icontains=keyword)
    
    return render(request,"search.html",{"products":products})
    
def template_filters_example(request):
    return render (request,"demo.html",{"data":"Django"})

def profile(request):
    return render(request,"profile.html")