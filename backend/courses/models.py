from django.db import models
from accounts.models import User
from mimetypes import guess_type
from django.core.files.base import ContentFile
from urllib.parse import urlparse, parse_qs
from django.core.validators import URLValidator

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
    description = models.CharField(max_length=300, default='', blank=True, null=True)
    context = models.FileField(upload_to="uploads/", blank=True)
    youtube_url = models.URLField(validators=[URLValidator()], blank=True, null=True)  
    #sale
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def context_type(self):
        """
        Determines the type of the context: file or YouTube URL.
        """
        if self.youtube_url:
            return 'youtube'
        elif self.context:
            return 'file'
        return None
        
    
    @property
    def youtube_embed_url(self):
        """
        Returns the YouTube embed URL if youtube_url is set.
        """
        if self.youtube_url:
            video_id = parse_qs(urlparse(self.youtube_url).query).get('v', [None])[0]
            if video_id:
                return f'https://www.youtube.com/embed/{video_id}'
        return None

    
class Genre(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
