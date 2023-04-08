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





@app.get("/arms")
async def root():
    return {"Name": "Bicep Curls",
            "YouTube" : "https://www.youtube.com/watch?v=Nkl8WnH6tDU",
            "Steps" : "Stand up straight with your feet shoulder-width apart and your arms at your sides. Hold a dumbbell in each hand with your palms facing forward. Slowly lift one dumbbell towards your shoulder, while keeping your elbow close to your body and your wrist straight. Exhale as you lift the weight. Pause at the top of the movement, then slowly lower the weight back down to the starting position. Inhale as you lower the weight. Repeat the movement with the other arm. Alternate arms for a total of 7-10 repetitions per arm, or as many as you can comfortably perform with good form."
        }


@app.get("/quads")
async def root():
    return {"Name": "Leg Extensions",
            "YouTube" : "https://www.youtube.com/watch?v=tTbJBUKnWU8",
            "Steps" : "Adjust the machine to fit your body size. Sit on the machine with your back against the backrest and your feet placed under the padded lever. Adjust the lever so that it sits just above your feet. Grab the handles on either side of the seat for support and stability. Begin the movement by extending your legs in front of you, and pushing against the lever with your feet. Straighten your legs as much as possible, then hold the position for a second or two. Slowly lower the lever back down to the starting position, keeping your movements smooth and controlled. Repeat the movement for a total of 8-12 repetitions or as many as you can comfortably perform with good form."
        }


@app.get("/glutes")
async def root():
    return {"Name": "Hip Thrusts",
            "YouTube" : "https://www.youtube.com/watch?v=Zp26q4BY5HE",
            "Steps" : "Start by sitting on the floor with your back against a bench or box, with your knees bent and your feet flat on the ground. Place a barbell across your hips, with your hands holding the bar just outside your hips. Roll the barbell towards you to position it on top of your hips. Make sure the barbell is centered and secure. Engage your core and glutes, and press your feet into the ground to lift your hips off the ground. Lift your hips up as high as possible, while keeping your shoulders and feet flat on the ground. Hold the position for a second or two, then slowly lower your hips back down to the starting position. Repeat the movement for a total of 8-12 repetitions or as many as you can comfortably perform with good form."
        }

@app.get("/chest")
async def root():
    return {"Name": "Dumbell Chest Press",
            "YouTube" : "https://www.youtube.com/watch?v=VmB1G1K7v94",
            "Steps" : "Lie flat on your back on a bench, with your feet flat on the ground and your knees bent. Hold a pair of dumbbells at chest level with your palms facing forward and your elbows bent. Engage your core muscles and press the dumbbells up towards the ceiling, extending your arms fully. Pause briefly at the top of the movement, then slowly lower the dumbbells back down to chest level, keeping your elbows at a 90-degree angle. Repeat the movement for a total of 8-12 repetitions or as many as you can comfortably perform with good form."
        }



@app.get("/back")
async def root():
    return {"Name": "Lat Pulldown",
            "YouTube" : "https://www.youtube.com/watch?v=CAwf7n6Luuc",
            "Steps" : "Start by sitting at a lat pulldown machine and adjusting the knee pad so that it fits snugly against your thighs. Grasp the bar with an overhand grip that is slightly wider than shoulder-width apart. Engage your core muscles and pull the bar down towards your chest, keeping your elbows close to your sides. Pause briefly at the bottom of the movement, then slowly release the bar back up to the starting position, with your arms fully extended. Repeat the movement for a total of 8-12 repetitions or as many as you can comfortably perform with good form."
        }





# uvicorn main:app --reload

