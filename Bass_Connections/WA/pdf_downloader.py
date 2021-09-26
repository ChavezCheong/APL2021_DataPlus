from openpyxl import load_workbook
import urllib.request
wb = load_workbook(filename = 'C:/Users/Ridge/Documents/Third year/American Lending Project/Data Team/Washington.xlsx')
sheet_ranges = wb['Washington']
links = []
names = []
for i in range(2, 535):
    try:   
        links.append(sheet_ranges['F' + str(i)].hyperlink.display)
        names.append(sheet_ranges['F' + str(i)].value)
    except:
        continue

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)    
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()
 
for i, link in enumerate(links):
    try:
        download_file(link, 'C:/Users/Ridge/Documents/Third year/American Lending Project/Data Team/pdfs/' + names[i])
    except:
        print(link)