from django.urls import path, include

from . import views

app_name='Index'

urlpatterns = [
    path('',views.userauth)
    
]
