import pandas as pd
import os
import numpy as np
import sys

csv_files = []

directory = "/home/ec2-user/environment/APL2021_DataPlus/Data_Extraction/Ohio_Textract/test"
ohio_csv = "/home/ec2-user/environment/APL2021_DataPlus/Data_Extraction/Ohio_Textract/Ohio_completed.csv"

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

final_df =  ohio_df.merge(df, on='Filename', how='left')

final_df['Text_x'] = final_df['Text_x'].fillna('')
final_df['Text_y'] = final_df['Text_y'].fillna('')

def merge_two_rows(s):
    return str(s['Text_x']) + str(s['Text_y'])

final_df['Text'] = final_df.apply(merge_two_rows, axis = 1)
final_df = final_df.drop(columns=['Text_x','Text_y'])

print(final_df)
np.set_printoptions(threshold=sys.maxsize)
final_df.to_csv("/home/ec2-user/environment/APL2021_DataPlus/Data_Extraction/Ohio_Textract/Ohio_completed2.csv")
print(len(final_df.at[5,'Text']))