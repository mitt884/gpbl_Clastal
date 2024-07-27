from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import ShippingForm
from .models import ShippingAddress
# Create your views here.
def payment_success(request):
    return render(request, "payment_success.html", {})

def checkout(request):
    cart = Cart(request)
    cart_courses = cart.get_courses
    total = cart.cart_total()
    
    if request.user.is_authenticated:
        #checkout as loggedin user
        shipping_user = ShippingAddress.objects.get(user_id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'checkout.html', {"cart_courses": cart_courses, "total": total, "shipping_form": shipping_form})

    else:
        #checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'checkout.html', {"cart_courses": cart_courses, "total": total})

def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_courses = cart.get_courses
        total = cart.cart_total()
        shipping_form = request.POST
        return render(request, 'billing_info.html', {"cart_courses": cart_courses, "total": total, "shipping_form": shipping_form})
    else:
        return redirect('home')