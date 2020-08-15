from django.urls import path
from . import views

app_name="Predict"

urlpatterns = [
    path('',views.renderPredict,name="predict")
]
