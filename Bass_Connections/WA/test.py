import requests

URL = "https://dfi.wa.gov/sites/default/files/consumer-services/enforcement-actions/2001-126-O01.pdf"
response = requests.get(URL)
pdf = open(r"WashingtonDocs\pdftest.pdf", 'wb')
pdf.write(response.content)
pdf.close()
print("File ", "test", " downloaded")