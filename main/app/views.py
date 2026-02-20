from django.shortcuts import redirect, render
from urllib3 import request
from .models import Product, Category, Profile 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from django.db.models import Q
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress





def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})

def category(request, foo):
    # Replace the hyphen with a space
    foo = foo.replace('_', '')
    # Grab the category
    try:
        # Look up the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category}) 
    except:
        messages.success(request, ("Category does not exist"))
        return redirect('home')
def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            

            # Do some shooping cart stuff
            current_user = Profile.objects.get(user__id=user.id)
            # Check if there is an old cart 
            saved_cart = current_user.old_cart
            if saved_cart:
                # Convert string to dictionary
                import json
                converted_cart = json.loads(saved_cart)
                # Set the session cart to old cart
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            return redirect('home')
            
        else:
            messages.success(request, ("Invalid username or password."))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have successfully logged out."))
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration successful. Information needed to complete profile, but not required."))
            return redirect('update_info')
        else:
            messages.success(request, ("Unsuccessful registration. Invalid information."))
    else:
        form = SignUpForm()
    
    return render(request, 'register.html', {'form': form})


def update_user(request):
    if request.user.is_authenticated:
        current_users = User.objects.get(id=request.user.id)
       
        form = UserInfoForm(request.POST or None, instance=current_users)
        
        if form.is_valid():
            form.save()
            login(request, current_users)
            messages.success(request, ("User information updated."))
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': form})
      
    else:
        messages.success(request, ("You must be logged in to update your information."))
        return redirect('home')
    
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, ("Password updated successfully. Please Login again"))
                # login(request, current_user)
                return redirect('update_password')
            else:
                for error in list(form.errors.values()):
                   messages.error(request, error)
                   return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})   
    else:
        messages.success(request, ("You must be logged in to update your password."))
        return redirect('home')

def update_info(request):
    if request.user.is_authenticated:
        # Get current User
        current_users = Profile.objects.get(user__id=request.user.id)
        # Get currrent Shipping Address
        shipping_user = ShippingAddress.objects.filter(shipping_user=request.user).first()
        # Current User Info
        form = UserInfoForm(request.POST or None, instance=current_users)
        # Shipping Info
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, ("User information updated."))
            return redirect('home')
        return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})
      
    else:
        messages.success(request, ("You must be logged in to update your information."))
        return redirect('home')
    

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        products = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not products:
            messages.success(request, ("Sorry ...No Products found. Please try again."))
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched': searched, 'products': products})
    else:
        return render(request, 'search.html', {})










