''' Module containing the url patterns of yatri bus '''
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('', admin.site.urls),
    path('api/v1/', include('apiv1.urls')),
]
