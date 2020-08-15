from django.urls import path
from . import views

app_name="DoctorRecommendation"

urlpatterns = [
    path('',views.renderDoctorRecommendation,name="doctorrecommend")
]
