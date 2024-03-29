from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

#from source import ml_model

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.backend import clear_session
import traceback
import os
from django.conf import settings


def load_crime_model():
    global crime_model
    model_file = os.path.join(settings.BASE_DIR, 'source\keras-crime.h5')
    crime_model = load_model(model_file)
    #crime_model._make_predict_function()


#Uses the Machine Learning model to predict the violent crime rate
#Returns "Low", "Average", or "High"
def machine_learning(in1):
    print("in the function")
    result = crime_model.predict([in1])[0][0]
    print("after predict call")
    print(result)
    result = result - 0.3
    result = result * 10
    print(result)
    if result < 0.5:
        return "Low"
    elif result > 0.7:
        return "High"
    else:
        return "Average"

def index(request): 
    load_crime_model()
    try:
        in1 = float(request.POST["input1"])
        print(in1)
        
	#estimated statistics calculated based on https://www2.census.gov/library/publications/decennial/1990/cph-l/cph-l-110.pdf
        average = 0.1382
        std_dev = 0.067
        norm = (in1 - average)/(std_dev)
        if norm < -2:
            norm = -2
        elif norm > 2:
            norm = 2
        norm = norm/5
        norm = norm + 0.5
		
        result = machine_learning(norm)
        print("The result is")
        print(result)
        template = loader.get_template('index.html')
        context = {'result' : result}
        return HttpResponse(template.render(context, request))
    except:
        template = loader.get_template('index.html')
        context = {}
        return HttpResponse(template.render(context, request))





