
from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.ApiOverview, name='home'),
    path('items', views.ListISOs, name = "list-isos"),
    path('update/<str:pk>', views.UpdateISO, name = "update-iso"),
    path('create', views.ISOCreate, name = "task-create"),
    path('item/<str:pk>/delete', views.ISODelete, name = "task-update")
]