from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from .models import ShippingAddress
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import Order, OrderItems
from accounts.models import User_Profile
from django.utils import timezone
# Create your views here.
@login_required
def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_courses = cart.get_courses
        total = cart.cart_total()
   
        #Get billing info from last page(This is for real billing)
        payment_form = PaymentForm(request.POST or None)
        #Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')
        
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        
        #Get shipping address from the session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"
        print(shipping_address)
        amount_paid = total
        
        #Create an Order
        user = request.user
        create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
        create_order.save()
        
        #Add Order Items
        order_id = create_order.pk
        for course in cart_courses():
            course_id = course.id
            if course.is_sale:
                price = course.sale_price
            else:
                price = course.price
                
            for key, value in cart.cart.items():
                quantity = value.get('quantity', 1)
                if int(key) == course_id:
                    #create order item
                    create_order_item = OrderItems(user=user,order_id=order_id, course_id=course_id, quantity=quantity, price=price)
                    create_order_item.save()
        
         # Set the purchased_at field
        OrderItems.objects.filter(order_id=order_id).update(purchased_at=timezone.now())
        
        # Credit the creator
        creator = course.user
        if creator and creator.is_creator:
            creator.balance += (price * quantity)
            creator.save()
            
        #Delete the cart
        for key in list(request.session.keys()):
            if key == "session_key":
                #Delete the key
                del request.session[key]
                
        #Delete cart from db
        cart.clear()
        # Update user profile
        if request.user.is_authenticated:
            current_user_profile = User_Profile.objects.get(user=request.user)
            current_user_profile.old_cart = ""
            current_user_profile.save()
                    
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
    
