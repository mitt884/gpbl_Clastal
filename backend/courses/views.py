from django.shortcuts import render, redirect
from .models import Courses,Tags
from django.contrib import messages
from orders.models import Order, OrderItems
# Create your views here.
def course(request, pk):
    course = Courses.objects.get(id=pk)
    purchased_courses = []
    
    if request.user.is_authenticated:
        order_items = OrderItems.objects.filter(user=request.user)
        purchased_courses = [order_item.course.id for order_item in order_items]
        
    return render(request, 'course.html', {'course': course, 'purchased_courses': purchased_courses})

def tag(request,foo):
    #replace space with hyphen
    foo = foo.replace('-', ' ')
    
    try:
        tag = Tags.objects.get(name=foo)
        courses = Courses.objects.filter(tags=tag)
        return render(request, 'tag.html', {'courses': courses, 'tag': tag})
    except:
        messages.success(request, ("タグが存在しません"))
        return redirect('home')


def classroom(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    order_items = OrderItems.objects.filter(user=request.user)
    courses = [(item.course, item.purchased_at) for item in order_items]
    
    return render(request, 'classroom.html', {'courses': courses})