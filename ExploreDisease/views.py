from django.shortcuts import render

# Create your views here.
def renderDisease(request):
    return render(request,'disease.html')