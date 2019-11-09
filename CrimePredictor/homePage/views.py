from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request): 
    try:
        in1 = float(request.POST["input1"])
        in2 = float(request.POST["input2"])
        in3 = float(request.POST["input3"])
        in4 = float(request.POST["input4"])
        in5 = float(request.POST["input5"])
        result = machine_learning(in1,in2,in3,in4,in5)
        template = loader.get_template('index.html')
        context = {'result' : result}
        return HttpResponse(template.render(context, request))
    except:
        template = loader.get_template('index.html')
        context = {}
        return HttpResponse(template.render(context, request))

def machine_learning(in1,in2,in3,in4,in5):
    return "Low"


