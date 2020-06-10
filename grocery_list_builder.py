## Load Required Packages


from bs4 import BeautifulSoup
import requests
import re
import string
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import pandas as pd


### Recommend Recipes based on User Input

### Parse HTML to Extract Ingredient List


def get_ingredients(url):
    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text
    # Parse the html content
    soup = BeautifulSoup(html_content, "lxml")
    if any(x in url for x in ('delish', 'countryliving', 'goodhousekeeping')):
        ingredients = [ li.text.replace("\t", "").replace("\n", "").strip() for li in soup.find_all("div", attrs={"class": "ingredient-item"})]
    elif any(x in url for x in ('cookinglight','myrecipes')):
        ingredients = str(soup.find("div", attrs={"class": "ingredients"})).replace("<li>", "").replace("</li>", "").split('\n')[2:-2]
    elif 'damn' in url:
        ingredients = [ li.text for li in soup.find_all("li", attrs={"itemprop": "ingredients"})]
    else:
        ingredients = []
    return ingredients


ingredients1 = get_ingredients('http://www.myrecipes.com/recipe/turkey-bean-chili')
ingredients2 = get_ingredients('https://www.countryliving.com/food-drinks/a23336101/seared-sausage-with-cabbage-and-pink-lady-apples-recipe/')


def process_ingredients(ingredients):
    ingredients = [x.lower() for x in ingredients]
    ingredients = [re.sub(r"([2-9])",r"\1 ", text) for text in ingredients]
    return ingredients



ingredients1 = process_ingredients(ingredients1)

ingredients2 = process_ingredients(ingredients2)



combined_ingredients = ingredients1+ingredients2


## tag each ingredient by type


tagged_ingredients = pd.read_csv(r"Documents/cooking project/tagged_ingredients.csv")



def grocery_tagger(ingredient_list, tags):
    # Define the sorter
    sorter = ['vegetable','fruit','meat','grain','condiment','canned good',
             'spice','baking','frozen','dairy']

    ingredient_list_df = pd.DataFrame(ingredient_list)
    ingredient_list_df['category'] = 0
    ingredient_list_df['name'] = 0
    for index, row in ingredient_list_df.iterrows():
        category = 'unknown'
        name = 'unknown'
        for index2, row2 in tags.iterrows():
            if row2['Name'] in row[0]:
                category = row2['Category']
                name = row2['Name']
                break
        ingredient_list_df.loc[index, 'category'] = category
        ingredient_list_df.loc[index, 'name'] = name
    ingredient_list_df = ingredient_list_df.sort_values('name')   
    true_sort = [s for s in sorter if s in ingredient_list_df.category.unique()]
    ingredient_list_df = ingredient_list_df.set_index('category').loc[true_sort].reset_index()
    return ingredient_list_df



grocery_tagger(combined_ingredients, tagged_ingredients)





