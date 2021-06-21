# Handling imports
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re

# Extract from website
source = requests.get('https://www.mass.gov/letter-ruling/tremont-credit-union').text
soup = BeautifulSoup(source, 'lxml')

# Parse through text of site
paragraph =  soup.find_all('div', class_ ="main-content main-content--two")[2]
# print(paragraph.prettify())
lines = paragraph.find_all(class_ = "ma__rich-text")[0]
text = lines.get_text()

text= re.sub(r"(\n( ?))+", "\n", text)
text = re.sub(r"   +", "  ", text)
text = text.replace("\n"," ")
print(text)

# df = pd.read_csv(r"C:\Users\chave\Desktop\Duke\APL2021_DataPlus\Data_Extraction\MA_Webscrape\Massachusetts_MEA_Database_Text.csv")
# print(df.columns)