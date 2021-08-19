# importing libraries
from bs4 import BeautifulSoup
import urllib.request
import re

url = "http://members.calbar.ca.gov/fal/LicenseeSearch/AdvancedSearch?LastNameOption=b&LastName=&FirstNameOption=b&FirstName=&MiddleNameOption=b&MiddleName=&FirmNameOption=b&FirmName=&CityOption=b&City=&State=&Zip=&District=&County=&LegalSpecialty=&LanguageSpoken=&PracticeArea=37"

try:
    page = urllib.request.urlopen(url)
except:
    print("An error occured.")

soup = BeautifulSoup(page, 'html.parser')

rowName = re.compile('^rowASRLodd')
content_trs = soup.find_all('tr', attrs={'class': rowName})
print(str(len(content_trs)) + " items")
# print(content_trs[0])
# .getText().replace("\r","").replace("\t","").strip()
rows = []
for tr in content_trs:
    #for each row, extract each cell
    cells = tr.find_all('td')
    rowItems = []
    #for each cell, extract the text and add to array
    for i in range(len(cells)):
        cell = cells[i]
        if i == 0:
            temp = cell.getText().split(", ")
            for item in temp:
                rowItems.append(" ".join(item.split()))
        else:
            rowItems.append(cell.getText().strip())
    #take care of the middle name
    rowItems[1] = rowItems[1].split(' ', 1)[0]
    rows.append(rowItems)

print(rows[0])