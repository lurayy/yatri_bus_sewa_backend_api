from django.urls import path
from . import views

urlpatterns = [
    path('add/layout',views.save_layout, name= "Some"),
]
