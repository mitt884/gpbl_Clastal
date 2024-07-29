from django.contrib import admin
from accounts.models import User, User_Profile

admin.site.register(User)
admin.site.register(User_Profile)

#mix proflie info and user info
class ProfileInline(admin.StackedInline):
    model = User_Profile
    
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username', 'age', 'email', 'university', 'is_creator']
    inlines = [ProfileInline]

#UNregister the old way
admin.site.unregister(User)

#Re-register
admin.site.register(User, UserAdmin)