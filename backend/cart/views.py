from django.shortcuts import render, get_object_or_404
from .cart import Cart
from courses.models import Courses
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.
def cart_summary(request):
    #get cart
    cart = Cart(request)
    cart_courses = cart.get_courses
    total = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_courses": cart_courses , "total": total})

def cart_add(request):
    # Get the cart
    cart = Cart(request)
    #POST test
    if request.POST.get('action') == 'post':
        #get courses
        course_id = int(request.POST.get('course_id'))
        #look up course in DB
        course = get_object_or_404(Courses, id=course_id)
        #Save to session
        cart.add(course=course)
        
        #Get cart_q
        
        cart_quantity = cart.__len__()
        #Return response
        # response = JsonResponse({'Course Name:': course.name})
        response = JsonResponse({'Quantity': cart_quantity})
        messages.success(request, ("Added to cart"))
        return response
    
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #get courses
        course_id = int(request.POST.get('course_id'))
        #Call delete function
        cart.delete(course=course_id)
        
        response = JsonResponse({'course': course_id})
        messages.success(request, ("Delete from cart successfully"))
        return response
    
def cart_update(request):
    pass
    