import pandas as pd
import os

csv_files = []

directory = "/home/ec2-user/environment/APL2021_DataPlus/Data_Extraction/Ohio_Textract/textract_to_text/test"
ohio_csv = "/home/ec2-user/environment/APL2021_DataPlus/Data_Collection/Ohio_MEA_Database.csv"

for filename in os.listdir(directory):
    if filename.endswith(".csv") or filename.endswith(".png"):
        csv_files.append(os.path.join(directory, filename))
    else:
        continue

df_list= []

itr = 0
for csv in csv_files:
    df_list.append(pd.read_csv(csv))

df = pd.concat(df_list)

df = df.drop(columns=['Unnamed: 0'])

df = df.drop_duplicates()

print(df)

ohio_df = pd.read_csv(ohio_csv)

print(ohio_df)

final_df = ohio_df.join(df.set_index('Filename'), on='Filename')

print(final_df)

final_df.to_csv("/home/ec2-user/environment/APL2021_DataPlus/Data_Extraction/Ohio_Textract/Ohio_completed.csv")