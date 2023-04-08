#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


import io, time, json
import requests
from bs4 import BeautifulSoup


# In[3]:


import requests

query = 'chicken rice'
api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
response = requests.get(api_url, headers={'X-Api-Key': 'IiBcsYDnkt70LsAirjY+6w==g1XgUj4Ld8KLhkA3'})
if response.status_code == requests.codes.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)


# In[5]:


import requests

query = input()
print("")
#thequery = query.split(", ")
api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
response = requests.get(api_url, headers={'X-Api-Key': 'IiBcsYDnkt70LsAirjY+6w==g1XgUj4Ld8KLhkA3'})
if response.status_code == requests.codes.ok:
    data = json.loads(response.text) # load all of the data to parse
    size = len(data)
    for i in range(size): 
        nutrition_data = data[i] 
        calories = nutrition_data['calories'] # get calories for the item
        protein = nutrition_data['protein_g'] # get protein for the item
        fat = nutrition_data['fat_total_g']
        carbs = nutrition_data['carbohydrates_total_g'] # get carbs for the item
        serving_size = nutrition_data['serving_size_g'] # check serving size
        name = nutrition_data['name']
        
        print(name.capitalize())
        print(f"Calories: {calories}")
        print(f"Protein: {protein}")
        print(f"Carbohydrates: {carbs}")
        print(f"Fat: {fat}")
        print(f"Serving Size: {serving_size}")
        print("            ")
        
        labels = ["protein", "carbohydrates","fat"]
        listofdata = [protein,carbs,fat]
        plt.pie(listofdata, labels = labels)
        plt.title(name.upper())
        plt.show() 
else:
    print("Error:", response.status_code, response.text)


# In[ ]:




