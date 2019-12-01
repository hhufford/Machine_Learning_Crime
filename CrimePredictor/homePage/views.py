from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from source import ml_model

import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.backend import clear_session
import traceback


def load_crime_model():
    global crime_model
    model_file = 'models/keras-crime.h5'
    crime_model = load_model(model_file)
    crime_model._make_predict_function()


#Uses the Machine Learning model to predict the violent crime rate
#Returns "Low", "Average", or "High"
def machine_learning(in1):
    result = crime_model.predict(in1)
	
	if result < 0.3:
		return "Low"
	elif result > 0.7:
		return "High"
	else:
		return "Average"

def index(request): 
	#load_crime_model()
    try:
        in1 = float(request.POST["input1"])
        #in2 = float(request.POST["input2"])
        #in3 = float(request.POST["input3"])
        #in4 = float(request.POST["input4"])
        #in5 = float(request.POST["input5"])
        result = machine_learning(in1)
        template = loader.get_template('index.html')
        context = {'result' : result}
        return HttpResponse(template.render(context, request))
    except:
        template = loader.get_template('index.html')
        context = {}
        return HttpResponse(template.render(context, request))





