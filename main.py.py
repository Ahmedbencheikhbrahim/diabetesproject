# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 10:41:47 2024

@author: Ahmed
"""

#!pip install fastapi
#!pip install uvicorn
#!pip install pickle5
#!pip install pydantic
#!pip install scikit-learn
#!pip install requests
#!pip install pypi-json
#!pip install pyngrok
#!pip install nest-asyncio

#from pyngrok import ngrok
#ngrok config add-authtoken 2bDPQ4eBKISgu3k4G6T6PesclBQ_3wewkxmW131FMnJjAfXgu

from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import json
from fastapi.middleware.cors import CORSMiddleware  # an api to allow the domain to use our api

app = FastAPI()

# an api to allow the domain to use our api
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class model_input(BaseModel):

    Pregnancies : int
    Glucose : int
    BloodPressure : int
    SkinThickness : int
    Insulin : int
    BMI : float
    DiabetesPedigreeFunction : float
    Age : int

# loading the saved model
diabetes_model = pickle.load(open('trained_model.sav', 'rb'))

@app.post('/diabetes_prediction')
def diabetes_predd(input_parameters : model_input):

    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)

    preg = input_dictionary['Pregnancies']
    glu = input_dictionary['Glucose']
    bp = input_dictionary['BloodPressure']
    skin = input_dictionary['SkinThickness']
    insulin = input_dictionary['Insulin']
    bmi = input_dictionary['BMI']
    dpf = input_dictionary['DiabetesPedigreeFunction']
    age = input_dictionary['Age']


    input_list = [preg, glu, bp, skin, insulin, bmi, dpf, age]

    prediction = diabetes_model.predict([input_list])

    if (prediction[0] == 0):
        return 'The person is not diabetic'
    else:
        return 'The person is diabetic'
