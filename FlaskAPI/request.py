# -*- coding: utf-8 -*-
"""
Created on Thu May  9 11:18:07 2024

@author: Dhanush
"""

# connecting to the flask app using requests library 

import requests 

# import input data
from data_input import data_in

url = "http://127.0.0.1:5000/predict"
headers = {"Content-Type": "application/json"}
data = {"input": data_in}

# connect to the flask app 
r = requests.get(url, headers = headers, json = data)

# retrieve and delivery the response from r 
r.json()
