import pandas as pd 

df = pd.read_excel(r"C:\Users\chave\Desktop\Duke\APL2021_DataPlus\Data_Collection\OhioSelenium\test.xlsx", sheet_name="Ohio")
df.to_csv('Ohio_MEA_Database.csv')

df2 = pd.read_excel(r"C:\Users\chave\Desktop\Duke\APL2021_DataPlus\Data_Collection\OhioSelenium\test.xlsx", sheet_name="Massachusetts")
df2.to_csv('Massachusetts_MEA_Database.csv')