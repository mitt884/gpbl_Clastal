from django.contrib import admin
from courses.models import Courses, Tags, Genre

admin.site.register(Courses)
admin.site.register(Tags)
admin.site.register(Genre)