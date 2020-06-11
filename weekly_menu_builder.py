
### Load Necessary Packages

import random
import pandas as pd
import numpy as np

### Define Functions to create menu based on input of meal types, dietary restrictions, and preferences


def find_meal(meal,diet_res, preferences, menu_urls):
    random_tag = random.choice(preferences)
    diet_res.append(random_tag)
    meal = list(db.recipes.aggregate([{"$match": {"meal":'dinner',"tags":{"$all": diet_res}}}, {"$sample":{"size": 1}}]))
    del diet_res[-1]
    if len(meal) > 0:
        url = meal[0]['url']
        if url in menu_urls:
            meal = None
    elif len(meal) == 0:
        meal = None
    return meal

def create_meal_type_list(breakfast_days,lunch_days, dinner_days, dessert_days):
    meal_types = []
    for i in breakfast_days:
        meal_types.append('breakfast')
    for i in lunch_days:
        meal_types.append('lunch')
    for i in dinner_days:
        meal_types.append('dinner')
    for i in dessert_days:
        meal_types.append('dessert')
    return meal_types

def url_getter(breakfast_days,lunch_days, dinner_days, dessert_days, diet_res, preferences):
    menu_urls = []
    meal_types = create_meal_type_list(breakfast_days,lunch_days, dinner_days, dessert_days)
    print(meal_types)
    for meal in meal_types:
        selection = None
        while selection is None:
            selection = find_meal(meal, diet_res, preferences, menu_urls)
            if selection is not None:
                url = selection[0]['url']
        menu_urls.append(url)     
    return menu_urls

#example of how to use code

breakfast_days = []
lunch_days = ['wednesday']
dinner_days = ['tuesday','wednesday']
dessert_days = []
diet_res = ['easy']
preferences = ['chinese','salad','chicken','italian','stew','italian','quick','egg','oreo','chocolate','quiche']
menu_urls = url_getter(breakfast_days,lunch_days, dinner_days, dessert_days, diet_res, preferences)
menu_urls

