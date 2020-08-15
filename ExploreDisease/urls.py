from django.urls import path
from . import views

app_name='ExploreDisease'

urlpatterns = [
    path('',views.renderDisease, name="home")
]
