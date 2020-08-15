from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def renderSymptoms(request):
    return render(request,'symptoms.html')


