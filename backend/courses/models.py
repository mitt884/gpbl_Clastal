from django.db import models
from accounts.models import User
from mimetypes import guess_type
from django.core.files.base import ContentFile
from urllib.parse import urlparse, parse_qs
from django.core.exceptions import ValidationError
from embed_video.fields import EmbedVideoField

# Create your models here.
class Tags(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'tags'
        

class Courses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name =  models.CharField(max_length=200)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    tags = models.ManyToManyField(Tags, blank=True)
    intro = models.CharField(max_length=20, default='', blank=True, null=True)
    description = models.CharField(max_length=300, default='', blank=True, null=True)
    context = models.FileField(upload_to="uploads/", blank=True)
    #sale
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def context_type(self):
        if self.context:
            return 'file'
        return None

    
class Genre(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
