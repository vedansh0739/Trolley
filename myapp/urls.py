from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello_world, name='hello_world'),
    path('a/', views.a, name='a'),
    path('receptor',views.receptor,name='receptor')
]
