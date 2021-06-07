import docx
import glob
import os
import re
import comtypes.client

FILE_PATH = r"C:\Users\chave\Desktop\Duke\APL2021_DataPlus\OhioSelenium\WordDocs\*.doc"
OUTPUT_PATH = r"C:\Users\chave\Desktop\Duke\APL2021_DataPlus\OhioSelenium\WordDocs\\"

fileslist=glob.glob(FILE_PATH)
regex_filename=r".*\\"
regex_withoutext=r".doc"
for i in range(0, len(fileslist)):
    filename=re.sub(regex_filename, "", fileslist[i])
    filename=re.sub(regex_withoutext, "", filename)
    in_file = os.path.abspath(fileslist[i])
    
    out_file = os.path.abspath(OUTPUT_PATH+str(filename))

    word = comtypes.client.CreateObject('Word.Application')
    doc = word.Documents.Open(in_file)
    doc.SaveAs(out_file, FileFormat=17)
    doc.Close()


