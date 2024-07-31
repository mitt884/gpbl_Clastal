from django.urls import path
from . import views

urlpatterns = [
    path('course/<int:pk>/', views.course, name='course'),
    path('tag/<str:foo>/', views.tag, name='tag'),
    path('classroom/', views.classroom, name='classroom'),
    path('course/<int:pk>/content/', views.course_content, name='course_content')
]
