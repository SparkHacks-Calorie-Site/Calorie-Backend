from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io, time, json
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from typing import Optional

from starlette.responses import StreamingResponse

class Item(BaseModel):
    food1: str
    food2: Optional[str] = None
    food3: Optional[str] = None



app = FastAPI()


# checks for successful connection 

@app.get("/root")
async def root():
    return {"message": "Success"}

# returns total amount of calories for all foods entered 

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


# returns total amount of macros for all food entered 

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



# returns encoded image of data visualization of total macros 

import base64

@app.post("/picture/")
async def create_item(item: Item):
    listoffood = [item.food1,item.food2,item.food3]
    images = []
    totalProtein  = 0
    totalCarbs = 0
    totalFat = 0

    for i in range(len(listoffood)): 
        query = listoffood[i]
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
        response = requests.get(api_url, headers={'X-Api-Key': 'IiBcsYDnkt70LsAirjY+6w==g1XgUj4Ld8KLhkA3'})
        if response.status_code == requests.codes.ok:
            data = json.loads(response.text)
            size = len(data)
            for i in range(size):
                nutrition_data = data[i] 
                protein = nutrition_data['protein_g']
                fat = nutrition_data['fat_total_g']
                carbs = nutrition_data['carbohydrates_total_g']
                totalProtein = totalProtein + protein
                totalFat = totalFat + fat
                totalCarbs = totalCarbs + carbs
                name = nutrition_data['name']

            labels = ["protein", "carbohydrates", "fat"]
            listofdata = [totalProtein, totalCarbs, totalFat]
            plt.pie(listofdata, labels=labels)
            plt.title(name.upper())
            
            # create a buffer to store image data
            buf = BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            
            # encode the image data as base64
            image_data = base64.b64encode(buf.getvalue()).decode("utf-8")
            images.append(image_data)
            
            plt.clf()

        else:
            print("Error:", response.status_code, response.text)

    return {"images": images}



# sends all information for arm workouts 

@app.get("/arms")
async def root():
    return {"Exercise 1 Name": "Bicep Curls",
            "YouTube 1" : "https://www.youtube.com/watch?v=Nkl8WnH6tDU",
            "Steps 1" : "Stand up straight with your feet shoulder-width apart and your arms at your sides. Hold a dumbbell in each hand with your palms facing forward. Slowly lift one dumbbell towards your shoulder, while keeping your elbow close to your body and your wrist straight. Exhale as you lift the weight. Pause at the top of the movement, then slowly lower the weight back down to the starting position. Inhale as you lower the weight. Repeat the movement with the other arm. Alternate arms for a total of 7-10 repetitions per arm, or as many as you can comfortably perform with good form.",
            
            "Exercise 2 Name": "Tricep Extensions",
            "YouTube 2" : "https://www.youtube.com/watch?v=_gsUck-7M74",
            "Steps 2" : "Sit on the edge of a bench with your hands placed next to your hips, fingers facing forward. Walk your feet out a few steps, keeping your heels on the ground. Straighten your arms, lifting your body off the bench. Slowly bend your elbows to lower your body towards the ground, keeping your back close to the bench. Once your elbows are at a 90-degree angle, push yourself back up to the starting position. Repeat for a total of 10-15 reps, or as many as you can comfortably perform with good form.", 

            "Exercise 3 Name": "Concentration Curls",
            "YouTube 3" : "https://www.youtube.com/watch?v=0AUGkch3tzc",
            "Steps 3" : "Sit on a bench or chair with your feet flat on the floor and your back straight. Hold a dumbbell in one hand with your palm facing up and your elbow resting against the inside of your thigh. Slowly curl the dumbbell up towards your shoulder, keeping your elbow stationary against your thigh and your wrist straight. Exhale as you lift the weight. Pause at the top of the movement and squeeze your bicep muscles. Lower the weight back down to the starting position, inhaling as you do so. Repeat for 8-10 repetitions, then switch to the other arm and repeat the same number of repetitions." 
        }

# sends all information for quad workouts 

@app.get("/quads")
async def root():
    return {"Exercise 1 Name": "Leg Extensions",
            "YouTube 1" : "https://www.youtube.com/watch?v=tTbJBUKnWU8",
            "Steps 1" : "Adjust the machine to fit your body size. Sit on the machine with your back against the backrest and your feet placed under the padded lever. Adjust the lever so that it sits just above your feet. Grab the handles on either side of the seat for support and stability. Begin the movement by extending your legs in front of you, and pushing against the lever with your feet. Straighten your legs as much as possible, then hold the position for a second or two. Slowly lower the lever back down to the starting position, keeping your movements smooth and controlled. Repeat the movement for a total of 8-12 repetitions or as many as you can comfortably perform with good form.", 
            
            "Exercise 2 Name": "Squat",
            "YouTube 2" : "https://www.youtube.com/watch?v=aclHkVaku9U",
            "Steps 2" : "Stand with your feet shoulder-width apart, toes pointing slightly outward. Keep your back straight and engage your core muscles. Extend your arms straight out in front of you or place your hands on your hips. Lower your body down by bending your knees, as if you're sitting back in a chair. Keep your heels on the ground and your knees over your ankles as you lower yourself down. Lower yourself as far as you can while maintaining good form and without letting your knees collapse inward. Pause briefly at the bottom of the squat, then push back up to a standing position, extending your legs fully. Repeat for 8-10 reps or as many as you can comfortably perform with good form.", 

            "Exercise 3 Name": "Leg Press",
            "YouTube 3" : "https://www.youtube.com/watch?v=IZxyjW7MPJQ",
            "Steps 3" : "Sit on a bench or chair with your feet flat on the floor and your back straight. Hold a dumbbell in one hand with your palm facing up and your elbow resting against the inside of your thigh. Slowly curl the dumbbell up towards your shoulder, keeping your elbow stationary against your thigh and your wrist straight. Exhale as you lift the weight. Pause at the top of the movement and squeeze your bicep muscles. Lower the weight back down to the starting position, inhaling as you do so. Repeat for 8-12 repetitions, then switch to the other arm and repeat the same number of repetitions." 
    }

# sends all information for glute workouts 

@app.get("/glutes")
async def root():
    return {"Exercise 1 Name": "Hip Thrusts with Barbell",
            "YouTube 1" : "https://www.youtube.com/watch?v=Zp26q4BY5HE",
            "Steps 1" : "Start by sitting on the floor with your back against a bench or box, with your knees bent and your feet flat on the ground. Place a barbell across your hips, with your hands holding the bar just outside your hips. Roll the barbell towards you to position it on top of your hips. Make sure the barbell is centered and secure. Engage your core and glutes, and press your feet into the ground to lift your hips off the ground. Lift your hips up as high as possible, while keeping your shoulders and feet flat on the ground. Hold the position for a second or two, then slowly lower your hips back down to the starting position. Repeat the movement for a total of 8-12 repetitions or as many as you can comfortably perform with good form.",

            "Exercise 2 Name": "Walking Lunges with Barbell",
            "YouTube 2" : "https://www.youtube.com/watch?v=83pKWaXl8VE",
            "Steps 2" : "Start by placing a barbell on a squat rack at chest height. Load the barbell with a weight that you can handle with good form. Stand facing the barbell and step forward to grip it with both hands, keeping your elbows pointing forward. Lift the barbell off the rack and rest it on the top of your back, just below your neck and above your shoulder blades. Step forward with your right foot, lowering your back knee towards the ground as you bend both knees to 90-degree angles. Keep your front knee over your ankle and your back knee hovering just above the ground. Push through your front heel and lift your back leg up, stepping forward with your left foot to repeat the lunge on the other side. Continue walking forward, alternating legs with each step, until you have completed the desired number of lunges.", 

            "Exercise 3 Name": "Deadlifts",
            "YouTube 3" : "https://www.youtube.com/watch?v=XxWcirHIwVo",
            "Steps 3" : "Adjust the seat of the machine so that your knees are bent at a 90-degree angle when your feet are flat on the platform. Place your feet hip-width apart on the platform, with your toes pointed slightly outward. Grip the handles of the machine and take a deep breath. Push the platform away from you, straightening your legs without locking your knees. Exhale as you push the platform away. Slowly lower the platform back down towards you, bending your knees to a 90-degree angle. Inhale as you lower the platform. Repeat for 8-12 repetitions or as many as you can comfortably perform with good form." 

        }


# sends all information for chest workouts 

@app.get("/chest")
async def root():
    return {"Exercise 1 Name": "Dumbell Chest Press",
            "YouTube 1" : "https://www.youtube.com/watch?v=VmB1G1K7v94",
            "Steps 1"  : "Lie flat on your back on a bench, with your feet flat on the ground and your knees bent. Hold a pair of dumbbells at chest level with your palms facing forward and your elbows bent. Engage your core muscles and press the dumbbells up towards the ceiling, extending your arms fully. Pause briefly at the top of the movement, then slowly lower the dumbbells back down to chest level, keeping your elbows at a 90-degree angle. Repeat the movement for a total of 8-12 repetitions or as many as you can comfortably perform with good form.", 

            "Exercise 2 Name": "Chest Fly",
            "YouTube 2" : "https://www.youtube.com/watch?v=eozdVDA78K0",
            "Steps 2" : "Lie on a flat bench with your feet flat on the floor, your head at one end of the bench, and your knees bent. Hold a dumbbell in each hand with your arms extended straight up over your chest, palms facing each other. Your elbows should be slightly bent and your wrists should be in a neutral position. Slowly lower your arms out to the sides in a wide arc, keeping your elbows slightly bent and your palms facing each other. Lower the dumbbells until they are level with your chest. Pause at the bottom of the movement for a moment, then slowly raise the dumbbells back up to the starting position, bringing them together over your chest. Repeat the movement for the desired number of repetitions.", 


            "Exercise 3 Name": "Incline Dumbell Press",
            "YouTube 3" : "https://www.youtube.com/watch?v=8iPEnn-ltC8",
            "Steps 3" : "Adjust the bench to a 30-45 degree incline and sit on the bench with a dumbbell in each hand, resting on your thighs. Lie back on the bench, bringing the dumbbells up to your chest. Keep your palms facing forward and your elbows bent at a 90-degree angle. Take a deep breath and press the dumbbells up above your chest, straightening your arms but not locking your elbows. Exhale as you press the weight. Slowly lower the dumbbells back down to your chest, keeping your elbows at a 90-degree angle. Inhale as you lower the weight. Repeat for 8-12 repetitions or as many as you can comfortably perform with good form." 
        }


# sends all information for back workouts 

@app.get("/back")
async def root():
    return {"Exercise 1 Name": "Lat Pulldown",
            "YouTube 1" : "https://www.youtube.com/watch?v=CAwf7n6Luuc",
            "Steps 1" : "Start by sitting at a lat pulldown machine and adjusting the knee pad so that it fits snugly against your thighs. Grasp the bar with an overhand grip that is slightly wider than shoulder-width apart. Engage your core muscles and pull the bar down towards your chest, keeping your elbows close to your sides. Pause briefly at the bottom of the movement, then slowly release the bar back up to the starting position, with your arms fully extended. Repeat the movement for a total of 8-12 repetitions or as many as you can comfortably perform with good form.", 


            "Exercise 2 Name": "Bent Over Rows",
            "YouTube 2" : "https://www.youtube.com/watch?v=FWJR5Ve8bnQ",
            "Steps 2" : "Stand with your feet shoulder-width apart and hold a dumbbell in each hand. Bend forward at the waist while keeping your back straight, and let your arms hang straight down towards the floor. Your palms should be facing each other, and your elbows should be close to your sides. Keeping your back straight and your core engaged, pull the dumbbells up towards your chest by bending your elbows and squeezing your shoulder blades together. Keep your elbows close to your sides throughout the movement. Pause at the top of the movement for a moment, then slowly lower the dumbbells back down to the starting position. Repeat the movement for the desired number of repetitions.", 


            "Exercise 3 Name": "Bent Over Reverese Fly",
            "YouTube 3" : "https://www.youtube.com/watch?v=ttvfGg9d76c",
            "Steps 3" : "Stand with your feet shoulder-width apart and hold a dumbbell in each hand with your palms facing each other. Hinge forward at your hips, keeping your back flat and your core engaged. Lift your arms out to the sides, squeezing your shoulder blades together as you do so. Keep your elbows slightly bent and your palms facing the ground throughout the exercise. Hold the top position for a second, then slowly lower the dumbbells back down to the starting position. Repeat for 8-12 repetitions or as many as you can comfortably perform with good form." 
        }

# send all information for hamstring workouts 

@app.get("/hamstrings")
async def root():
    return {
        "Exercise 1 Name": "Romanian Deadlift",
        "YouTube 1": "https://www.youtube.com/watch?v=_oyxCn2iSjU&t=25s",
        "Steps 1": "Start with your feet shoulder-width apart and your knees slightly bent. Hold a barbell with an overhand grip and let it rest on the front of your thighs. Keep your back straight and your core engaged as you hinge forward at the hips, lowering the bar down the front of your legs. Go as low as you can while maintaining a flat back and keeping the bar close to your legs. Pause at the bottom of the movement, then use your hamstrings and glutes to lift the bar back up to the starting position. Repeat for 8-12 repetitions or as many as you can comfortably perform with good form.",

        "Exercise 2 Name": "Lying Leg Curl",
        "YouTube 2": "https://www.youtube.com/watch?v=6y_GEg3YFC0",
        "Steps 2": "Lie face down on a leg curl machine with your knees just off the edge of the bench and your ankles hooked under the padded bar. Grasp the handles of the machine for stability. Keep your hips and legs in contact with the bench throughout the exercise. Use your hamstrings to pull the padded bar towards your buttocks, keeping your toes pointed towards the ground. Pause briefly at the top of the movement, then slowly lower the padded bar back down to the starting position. Repeat for 8-12 repetitions or as many as you can comfortably perform with good form.",

        "Exercise 3 Name": "Seated Leg Curl",
        "YouTube 3" : "https://www.youtube.com/watch?v=oFxEDkppbSQ",
        "Steps 3" : "Start by sitting at a leg curl machine and adjusting the weight. Hook your ankles under the padded lever, and grasp the handles of the machine. Engage your core muscles and curl your legs towards your buttocks, squeezing your hamstrings at the top of the movement. Pause briefly, then slowly lower the weight back down to the starting position. Repeat for 8-12 repetitions or as many as you can comfortably perform with good form." 
    }