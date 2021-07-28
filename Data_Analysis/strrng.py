boof = ""
with open(r'C:\Users\chave\Desktop\Duke\APL2021_DataPlus\Data_Analysis\stop_words.txt','r', encoding = "ISO-8859-1") as file:
    contents = file.readlines()
    for word in contents:
        boof += f"|{word[:-1]}"

print(boof)