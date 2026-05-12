from django.shortcuts import render, redirect
from .models import Product, Article, Tag
from django.core.paginator import Paginator
from .forms import NewUserForm, UserForm, ProfileForm, VoteForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 

# Create your views here.

# Homepage view
def homepage(request):
    if request.method == "POST":
        product_id = request.POST.get("product_pk")
        product = Product.objects.get(id = product_id)
        request.user.profile.product.add(product)
        messages.success(request, f'{product} added to wishlist!')
        return redirect("main:homepage")
    product = Product.objects.all()[:4]
    new_posts = Article.objects.all().order_by('-article_published')[:4]
    featured = Article.objects.filter(article_tags__tag_name = 'Featured')[:3]
    most_recent = new_posts.first()
    return render(request = request, template_name='main/home.html', context={'product': product, 'featured': featured, 'most_recent': most_recent, 'new_posts': new_posts})


# Products page view
def products(request):
    if request.method == "POST":
        product_id = request.POST.get("product_pk")
        product = Product.objects.get(id = product_id)
        request.user.profile.product.add(product)  
        messages.success(request,(f'{product} added to wishlist.'))
        return redirect("main:products")
    products = Product.objects.all()
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    vote_form = VoteForm()
    return render(request = request, template_name = 'main/products.html', context = {'page_object' : page_object, 'vote_form': vote_form} )


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
def blog(request, tag_page):
    if tag_page == 'articles':
        tag = ''
        blog = Article.objects.all().order_by('-article_published')
    else:
        tag = Tag.objects.get(tag_slug = tag_page)
        blog = Article.objects.filter(article_tags = tag).order_by('-article_published')
    paginator = Paginator(blog, 6)
    page_number = request.GET.get('page')    
    blog_object = paginator.get_page(page_number)
    return render(request = request, template_name= 'main/blog.html', context= {'blog_object': blog_object, 'tag': tag})

# Article view
def article(request, article_page):
    article = Article.objects.get(article_slug=article_page)
    return render(request = request, template_name= 'main/article.html', context= {'article': article})

# Userpage function
def userpage(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance = request.user)
        profile_form = ProfileForm(request.POST, instance = request.user.profile)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, ('Your profile was updated successfully!'))
        elif profile_form.is_valid():
            profile_form.save()
            messages.success(request, ('Your wishlist was saved successfully!'))
        else:
            messages.error('Unable to complete request')
        return redirect('main:userpage')
    user_form = UserForm(instance = request.user)
    profile_form = ProfileForm(instance = request.user.profile)
    return render(request = request, template_name='main/user.html', context={'user': request.user, 'user_form': user_form, 'profile_form': profile_form})


