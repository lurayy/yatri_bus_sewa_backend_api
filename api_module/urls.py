from django.urls import path
from . import views

urlpatterns = [
    path('post/layout',views.save_layout, name= "Some"),
]
