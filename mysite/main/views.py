from django.shortcuts import render, redirect
from .models import Product, Article
from django.core.paginator import Paginator
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 

# Create your views here.

# Homepage view
def homepage(request):
    product = Product.objects.all()[:4]
    return render(request = request, template_name='main/home.html', context={'product': product})


# Products page view
def products(request):
    products = Product.objects.all()
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request = request, template_name = 'main/products.html', context = {'page_object' : page_object} )


# Registration form view
def register(request):
    if request.method == "POST":  # checks the request method
        form = NewUserForm(request.POST)        # Instance of a form
        if form.is_valid():                     # Checks if the form is valid
            user = form.save()                  # Saves user's info from the form
            login(request, user)                # Initiates login using saved user credentials
            messages.success(request, "Registration Successful.")  # Message to display successful registration
            return redirect("main:homepage")    # Redirects to homepage
        else:
            messages.error(request, "Registration unsuccessful. Invalid Credentials")
    else: 
        form = NewUserForm
    return render(request = request, template_name = "main/register.html", context = {"form" : form} )


# Login request view
def login_request(request):
    if request.method == "POST":
        form =  AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            # Get cleaned data from form and authenticate
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)

            # Login if user exists
            if user is not None:
                login(request, user)
                messages.success(request, f'You are logged in as {username}.')
                return redirect('main:homepage')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    
    # If request method is not POST, return form as context to be rendered in login page
    form = AuthenticationForm()
    return render(request = request, template_name = 'main/login.html', context = {'form': form})

# Logout request view
def logout_request(request):
    logout(request)
    messages.success(request , 'You are successfully logged out.')
    return redirect('main:homepage')

# Blog function
def blog(request):
    blog = Article.objects.all().order_by('-article_published')
    paginator = Paginator(blog, 6)
    page_number = request.GET.get('page')    
    blog_object = paginator.get_page(page_number)
    return render(request = request, template_name= 'main/blog.html', context= {'blog_object': blog_object})

# Article view
def article(request, article_page):
    article = Article.objects.get(article_slug=article_page)
    return render(request = request, template_name= 'main/article.html', context= {'article': article})


