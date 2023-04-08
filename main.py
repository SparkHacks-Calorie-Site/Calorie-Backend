from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io, time, json
import requests
from bs4 import BeautifulSoup


class Item(BaseModel):
    food1: str
    food2: str
    food3: str


app = FastAPI()


@app.post("/calories/")
async def create_item(item: Item):
    totalCals = 0
    listoffood = [item.food1,item.food2,item.food3]

    for i in range(len(listoffood)): 
        query = listoffood[i]
        #thequery = query.split(", ")
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
        response = requests.get(api_url, headers={'X-Api-Key': 'IiBcsYDnkt70LsAirjY+6w==g1XgUj4Ld8KLhkA3'})
        if response.status_code == requests.codes.ok:
            data = json.loads(response.text) # load all of the data to parse
            size = len(data)
            for i in range(size):
                nutrition_data = data[i] 
                calories = nutrition_data['calories'] # get calories for the item
                totalCals = totalCals + calories
                name = nutrition_data['name']

                print(name.capitalize())
                print(f"Calories: {calories}") 
            
            print("TOTAL CALORIES: " ,round(totalCals,2))

        else:
            print("Error:", response.status_code, response.text)

    return totalCals



@app.post("/macros/")
async def create_item(item: Item):
    listoffood = [item.food1,item.food2,item.food3]
    totalProtein  = 0
    totalCarbs = 0
    totalFat = 0

    for i in range(len(listoffood)): 
        query = listoffood[i]
        #thequery = query.split(", ")
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
        response = requests.get(api_url, headers={'X-Api-Key': 'IiBcsYDnkt70LsAirjY+6w==g1XgUj4Ld8KLhkA3'})
        if response.status_code == requests.codes.ok:
            data = json.loads(response.text) # load all of the data to parse
            size = len(data)
            for i in range(size):
                nutrition_data = data[i] 
                protein = nutrition_data['protein_g'] # get protein for the item
                fat = nutrition_data['fat_total_g']
                carbs = nutrition_data['carbohydrates_total_g'] # get carbs for the item
                totalProtein = totalProtein + protein
                totalFat = totalFat + fat
                totalCarbs = totalCarbs + carbs
                totalMacros = {'Protein': totalProtein, 'Fat': totalFat, 'Carbs': totalCarbs}

                print(f"Protein: {totalProtein}")
                print(f"Carbs: {totalFat}") 
                print(f"Fat: {totalCarbs}")  

        else:
            print("Error:", response.status_code, response.text)

    return totalMacros