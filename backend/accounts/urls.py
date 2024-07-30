from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register_user, name='register'),
    path('login/',views.login_user, name='login'),
    path('logout/',views.logout_user, name='logout'),
    path('update_user/',views.update_user, name='update_user'),
    path('update_password/',views.update_password, name='update_password'),
    path('update_info/',views.update_info, name='update_info'),
    path('add_courses/',views.add_courses, name='add_courses'),
    path('delete_courses/<int:course_id>/',views.delete_courses, name='delete_courses'),
    path('user_courses/',views.user_courses, name='user_courses'),
    path('modify_courses/<int:course_id>/',views.modify_courses, name='modify_courses'),
]
