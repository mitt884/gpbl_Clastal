from django.db import models
from accounts.models import User
from courses.models import Courses
# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def sub_total(self):
        return self.courses.price * self.quantity