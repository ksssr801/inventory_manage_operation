from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('purchase/', include('inven_app.urls')),
]
