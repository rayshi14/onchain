from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:contract_address>/", views.contract_abi, name="contract_abi"),
    path("<str:contract_address>/function/<str:function_name>/", views.function_abi, name="function_abi"),
    path("<str:contract_address>/event/<str:event_name>/", views.event_abi, name="event_abi")
]