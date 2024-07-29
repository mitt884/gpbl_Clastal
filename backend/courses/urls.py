from django.urls import path
from . import views

urlpatterns = [
    path('course/<int:pk>/', views.course, name='course'),
    path('tag/<str:foo>/', views.tag, name='tag'),
]
