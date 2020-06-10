## Load Required Packages

from bs4 import BeautifulSoup
import requests
import re
import string
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import pandas as pd


### Extract Keywords and Cook Time from Recipe Webpages

### define functions for text cleaning

def remove_stop_words(s):
    stop_words = {'tag','cat','type', 'recipe', 'meal', 'post',
                  'breakfast','lunch','dinner','dessert', 
                  'for','idea','best'}
    for w in stop_words:
        pattern = r'\b'+w+r'\b'
        s = re.sub(pattern, '', s)
    return s

def lemmatize(s):
    s = s.split(' ')
    lemmatizer = WordNetLemmatizer()
    s = [lemmatizer.lemmatize(w) for w in s]
    s = ' '.join(s)
    return s


### define function to extract and clean keywords and time


def get_recipe_keywords_time(url):
    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text
    # Parse the html content
    soup = BeautifulSoup(html_content, "lxml")
    time = 'none'
    if any(x in url for x in ('delish', 'countryliving', 'goodhousekeeping')):
        try:
            keywords = str(soup.find("meta", attrs={"name": "keywords"})).split('"')[1]
        except IndexError:
            keywords = "none"
        time = str(soup.find("span", attrs={"class": "total-time-amount"}))
    elif any(x in url for x in ('cookinglight','myrecipes')):
        try:
            keywords = str(soup.find("meta", attrs={"name": "keywords"})).split('"')[1]
        except IndexError:
            keywords = "none"
        time = str(soup.find_all('div', {'class' :'recipe-meta-item'}))
    elif 'damn' in url:
        keywords = str(soup.find("meta", attrs={"name":"shareaholic:keywords"})).split('"')[1]
        time = str(soup.find_all('div',{'class':"post-meta time"}))
    
    keywords = re.split(',|/', keywords) 
    keywords = [re.sub(r'[^A-Za-z0-9]+',r" ", text) for text in keywords]
    keywords = [text.lower() for text in keywords]
    keywords = [lemmatize(w) for w in keywords]
    keywords = [remove_stop_words(w) for w in keywords]
    keywords = [text.strip() for text in keywords]
    keywords = [re.sub(' +', ' ',text) for text in keywords]
    keywords = list(dict.fromkeys(keywords))
    keywords = [i for i in keywords if i]
    keywords = ', '.join(keywords)
    
    time = time.replace("\n", "")
    time = re.sub('<[^>]+>', ' ', time)
    time = re.sub(' +', ' ',time)
    time = time.strip('[]')
    time = time.strip()
    
    return [keywords, time]


### use function on a sample dataset

recipes = pd.read_csv(r"Documents/cooking project/recipes.csv")


recipes_sample = recipes[['link','meal']]

fn = lambda x: get_recipe_keywords_time(x['link'])
cols = recipes_sample.apply(fn, axis=1)
cols_df = pd.DataFrame(cols.tolist())
recipes_sample = recipes_sample.assign(keywords= cols_df[0].values,
                                      time=cols_df[1].values)


recipes_sample.to_csv("Documents/cooking project/recipes_updated2.csv")





