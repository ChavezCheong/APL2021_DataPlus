# Handling imports
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re
import sys

# Extract from website
source = requests.get('https://www.mass.gov/consent-order/yauvan-kumar').text
soup = BeautifulSoup(source, 'lxml')

# Parse through text of site
paragraph =  soup.find_all('div', class_ ="main-content main-content--two")[1]
# print(paragraph.prettify())
lines = paragraph.find_all(class_ = "ma__rich-text")[1]
text = lines.get_text()

text= re.sub(r"(\n( ?))+", "\n", text)
text = re.sub(r"   +", "  ", text)
text = text.replace("\n"," ")
print(len(text))

df = pd.read_csv(r"C:\Users\chave\Desktop\Duke\APL2021_DataPlus\Data_Analysis\Unstandardized Data\MA_completed.csv")
np.set_printoptions(threshold=sys.maxsize)
df.at[282,'Text'] = text
print(df.at[282,'Text'])
print(len(df.at[6,'Text']))
df.to_csv(r"C:\Users\chave\Desktop\Duke\APL2021_DataPlus\Data_Analysis\Unstandardized Data\MA_completed.csv")