from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from .models import ShippingAddress
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def process_order(request):
    if request.POST:
        #Get billing info from last page
        payment_form = PaymentForm(request.POST or None)
        #Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')
        
        #Get shipping address from the session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"
        print(shipping_address)
        
        
        
        messages.success(request, "Order Placed")
        return redirect('home')
    else:
        messages.error(request, "Access Denied")
        return redirect('home')
    
    
def payment_success(request):
    return render(request, "payment_success.html", {})

@login_required
def checkout(request):
    cart = Cart(request)
    cart_courses = cart.get_courses
    total = cart.cart_total()
    
    if request.user.is_authenticated:
        #checkout as loggedin user
        shipping_user = ShippingAddress.objects.get(user_id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if shipping_form.is_valid():
            shipping_info = shipping_form.save(commit=False)
            shipping_info.user = shipping_user
            shipping_info.save()
        return render(request, 'checkout.html', {"cart_courses": cart_courses, "total": total, "shipping_form": shipping_form})

    else:
        #checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'checkout.html', {"cart_courses": cart_courses, "total": total})

    
@login_required(login_url='login')
def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_courses = cart.get_courses
        total = cart.cart_total()

        #create a session with Shipping Info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, 'billing_info.html', {
                "cart_courses": cart_courses, 
                "total": total, 
                "billing_form": billing_form, 
                "shipping_info": request.POST
            })
        else:
            billing_form = PaymentForm()
            return render(request, 'billing_info.html', {
                "cart_courses": cart_courses, 
                "total": total, 
                "billing_form": billing_form, 
                "shipping_info": request.POST
            })
    else:
        messages.error(request, "Access Denied")
        return redirect('home')
    
