from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.apps import apps

# Create your views here.

def renderDoctorRecommendation(request):
    databasedata = apps.get_model('Predict','DiagnosisModel')
    symptomdata = [databasedata.objects.latest('id')]
    symptomlist = symptomdata[0].symtoms_entered
    return render(request,'doctor_report.html',context={'databasedata':symptomdata,'symptomname':symptomlist})