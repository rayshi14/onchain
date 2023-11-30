from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('call_function/', views.call_function, name='call_function')
]