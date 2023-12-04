from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("data/<str:contract_address>", views.data_contract_abi, name="data_contract_abi"),
    path("data/<str:contract_address>/function/<str:function_name>", views.data_function_abi, name="data_function_abi"),
    path("data/<str:contract_address>/event/<str:event_name>", views.data_event_abi, name="data_event_abi"),
    path('api/add_abi', views.add_abi, name='add_abi'),
    path('api/call_abi', views.call_abi, name='call_abi'),
    path('api/search_abi', views.search_abi, name='search_abi'),
    path('view/view_add_abi', views.view_add_abi, name='view_add_abi'),
    path('view/view_abi/<str:id>', views.view_abi, name='view_abi'),
    path('view/view_abi/<str:id>/edit', views.view_edit_abi, name='view_edit_abi'),
    path('view/view_results/<str:keywords>', views.view_search_results, name='view_search_results')
]