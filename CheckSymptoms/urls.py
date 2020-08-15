from django.urls import path
from . import views

app_name="CheckSymptoms"

urlpatterns = [
    path('',views.renderSymptoms,name="checksymptoms"),
]
