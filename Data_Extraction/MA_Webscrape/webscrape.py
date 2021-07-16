# Handling imports
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re
import sys

# Set up the dataframe
df = pd.read_csv(r"C:\Users\chave\Desktop\Duke\APL2021_DataPlus\Data_Extraction\MA_Webscrape\Massachusetts_MEA_Database_Text_FileName.csv")
# print(df.columns)
# Edit the dataframe
df.drop(['Unnamed: 0', 'Text'], axis=1, inplace=True)
df.rename(columns={'URL - to be filled in':'URL','File Name':'Filename'}, inplace=True)

def get_text(row):
    # Get URL
    url = row['URL']
    questionable_stuff = ['doc', 'pdf']
    
    if not pd.isnull(url) and not any(x in url for x in questionable_stuff):
        try:
            # Extract from website
            source = requests.get(url).text
            soup = BeautifulSoup(source, 'lxml')

            # Parse through text of site
            paragraph =  soup.find_all('div', class_ ="main-content main-content--two")[1]
            #print(paragraph.prettify())

            lines = paragraph.find_all(class_ = "ma__rich-text")[1]
            text = lines.get_text(separator=' ')
            text= re.sub(r"(\n( ?))+", "\n", text)
            text = re.sub(r"   +", "  ", text)
            text = text.replace("\n"," ")
            return text

        except Exception as exception:
            print(url)
            return exception.__class__.__name__
    return np.nan

df['Text'] = df.apply(lambda row : get_text(row), axis=1)
np.set_printoptions(threshold=sys.maxsize)
df.to_csv(r"C:\Users\chave\Desktop\Duke\APL2021_DataPlus\Data_Extraction\MA_Webscrape\Massachusetts_MEA_Database_Text.csv")