from django.shortcuts import render
from courses.models import Courses
from django.contrib import messages
from django.db.models import Q
def home(request):
    courses = Courses.objects.all()
    return render(request, 'home.html', {'courses': courses})

def about(request):
    return render(request, 'about.html', {})

def search(request):
    #if they fillout the form:
    if request.method == 'POST':
        searched = request.POST['searched']
        #Query the courses
        searched = Courses.objects.filter(Q(name__icontains=searched)| Q(intro__icontains=searched))
        
        if not searched:
            messages.success(request, ("No courses found"))
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched': searched})
    else:
        return render(request, 'search.html', {})
