from django.shortcuts import render, redirect, get_object_or_404
from .models import User_Profile
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .forms import UserRegisterForm, UserUpdateForm, ChangeUserPassword, UserInfoForm, User_Add_Course_Form
from django.contrib.auth import logout as auth_logout
import json
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from courses.models import Courses, Tags
from django.urls import reverse

def register_user(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Set password
            user.save()

            # Authenticate the user
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, "登録に成功。ログインしました。")
                return redirect('update_info')  # Redirect to the update_info page
            else:
                messages.error(request, "ユーザー認証に失敗しました。")
                return redirect('login')  # Redirect to login if authentication fails

        else:
            messages.error(request, "無効な資格情報")
            return render(request, 'register.html', {'form': form})
    else:
        form = UserRegisterForm()  # Initialize form for GET request
        return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            
            current_user = User_Profile.objects.filter(user=user).first()
            saved_cart = current_user.old_cart
            
            cart = Cart(request)
            #Loopthru cart, add item to cart
             
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                
                cart = Cart(request)
                #Loopthru cart, add item to cart
                for course_id, details in converted_cart.items():
                    cart.db_add(course_id, quantity=details['quantity'])

            
            messages.success(request, ("ログインに成功しました"))
            next_url = request.GET.get('next')
            return redirect(next_url) if next_url else redirect('home')
        else:
            messages.success(request, ("無効な資格情報"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})
    
def logout_user(request):
    if request.user.is_authenticated:
        # Convert the cart session data to a JSON string
        cart_data = json.dumps(request.session.get('cart', {}))
        User_Profile.objects.filter(user=request.user.id).update(old_cart=cart_data)
        
    auth_logout(request)
    return redirect('home')
 
@login_required   
def update_user(request):
    current_user = request.user
    user_form = UserUpdateForm(request.POST or None, instance=current_user)

    if user_form.is_valid():
        user_form.save()
        messages.success(request, ("Update infos successfully"))
        return redirect('home')
    
    
    return render(request, 'update_user.html', {'user_form': user_form})

@login_required 
def update_password(request):
    current_user = request.user
    if request.method == 'POST':
        form = ChangeUserPassword(current_user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Update Password Successfully")
            return redirect('login')
        else:
            return redirect('update_password')
    else:
        form = ChangeUserPassword(current_user)
        return render(request, 'update_password.html', {'form': form})
    
@login_required
def update_info(request):
    # Get current user profile
    current_user = User_Profile.objects.get(user=request.user)
    
    # Get current user's Shipping info
    try:
        shipping_user = ShippingAddress.objects.get(user=request.user)
    except ShippingAddress.DoesNotExist:
        shipping_user = ShippingAddress(user=request.user)

    # Handle POST request
    if request.method == 'POST':
        form = UserInfoForm(request.POST, instance=current_user)
        shipping_form = ShippingForm(request.POST, instance=shipping_user)

        # Check if the forms are valid (individually)
        if form.is_valid() or shipping_form.is_valid():
            # Save form data if valid
            if form.is_valid():
                form.save()
            if shipping_form.is_valid():
                shipping_form.save()
            messages.success(request, "Information updated successfully.")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserInfoForm(instance=current_user)
        shipping_form = ShippingForm(instance=shipping_user)

    return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})

@login_required
def add_courses(request):
    if not request.user.is_creator:
        return redirect('home')
    
    
    if request.method == "POST":
        add_course_form = User_Add_Course_Form(request.POST, request.FILES)
        if add_course_form.is_valid():
            course = add_course_form.save(commit=False)
            course.user = request.user
            course.save()
            #Handle new custom tag:
            new_tags = add_course_form.cleaned_data['new_tags']
            if new_tags:
                tag_names = [tag.strip() for tag in new_tags.split(',')]
                for tag_name in tag_names:
                    tag, created = Tags.objects.get_or_create(name=tag_name)
                    course.tags.add(tag)
            messages.success(request, ("You have added a course!!"))
            return redirect('home')
    else:
        add_course_form = User_Add_Course_Form()
        return render(request, 'add_courses.html', {'add_course_form': add_course_form})
    
@login_required
def delete_courses(request, course_id):
    if request.user.is_creator:
        course = get_object_or_404(Courses, id=course_id)
        
    if course.user != request.user:
        messages.error(request, "You are not allowed to delete this course!!")
        
    if course.context:
        course.context.delete(save=False) #delete file from medie/upload when deleted
    
    course.delete()
    messages.success(request, "Course deleted successfully!")
    return redirect('home')
        
@login_required
def user_courses(request):
    if not request.user.is_creator:
        return redirect('home')
    
    courses = Courses.objects.filter(user=request.user)
    add_course_url = reverse('add_courses')
    balance = request.user.balance
    return render(request, 'user_courses.html', {'courses': courses, 'add_course_url': add_course_url, 'balance': balance})