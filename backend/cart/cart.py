import json
from courses.models import Courses
from decimal import Decimal
from accounts.models import User_Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        self.cart = self.session.get('cart', {})
        
        if 'cart' not in request.session:
            self.session['cart'] = {}
            self.cart = self.session['cart']

    def add(self, course, quantity=1):
        course_id = str(course.id)
        
        if course_id in self.cart:
            self.cart[course_id]['quantity'] = quantity
        else:
            self.cart[course_id] = {'price': str(course.price), 'quantity': quantity}
        
        self.session.modified = True
        self._save_to_user_profile()

    def db_add(self, course_id, quantity=1):
        # Assuming `course_id` is a string and `quantity` is always 1
        if course_id in self.cart:
            self.cart[course_id]['quantity'] = quantity
        else:
            course = Courses.objects.get(id=course_id)
            self.cart[course_id] = {'price': str(course.price), 'quantity': quantity}
        
        self.session.modified = True
        self._save_to_user_profile()
    
    def _save_to_user_profile(self):
        if self.request.user.is_authenticated:
            current_user = User_Profile.objects.get(user=self.request.user)
            cart_data = json.dumps(self.cart)
            current_user.old_cart = cart_data
            current_user.save()

    def __len__(self):
        return sum(item.get('quantity', 1) for item in self.cart.values())
    
    def get_courses(self):
        course_ids = self.cart.keys()
        courses = Courses.objects.filter(id__in=course_ids)
        for course in courses:
            course_id = str(course.id)
            quantity = self.cart[course_id].get('quantity', 1)
            if course.is_sale:
                course.individual_total = course.sale_price * quantity
            else:
                course.individual_total = course.price * quantity
        return courses

    def delete(self, course):
        course_id = str(course)
        if course_id in self.cart:
            del self.cart[course_id]
        self.session.modified = True
        self._save_to_user_profile()

    def cart_total(self):
        course_ids = self.cart.keys()
        courses = Courses.objects.filter(id__in=course_ids)
        total = Decimal('0.00')
        for key, value in self.cart.items():
            key = int(key)
            quantity = value.get('quantity', 1)
            for course in courses:
                if course.id == key:
                    if course.is_sale:
                        total += course.sale_price * quantity
                    else:
                        total += course.price * quantity
        return total
