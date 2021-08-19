# importing libraries
from bs4 import BeautifulSoup
import urllib.request
import re
# import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = "http://members.calbar.ca.gov/fal/LicenseeSearch/AdvancedSearch?LastNameOption=b&LastName=&FirstNameOption=b&FirstName=&MiddleNameOption=b&MiddleName=&FirmNameOption=b&FirmName=&CityOption=b&City=&State=&Zip=&District=&County=&LegalSpecialty=&LanguageSpoken=&PracticeArea=37"

try:
    page = urllib.request.urlopen(url)
except:
    print("An error occured.")

soup = BeautifulSoup(page, 'html.parser')

# Instantiate an Options object
opts = Options()
opts.add_argument(" --headless")
# Instantiate a webdriver
driver = webdriver.Chrome(options=opts)

#get all rows
rowName = re.compile('^rowASRLodd')
content_trs = soup.find_all('tr', attrs={'class': rowName})
print(str(len(content_trs)) + " items")

rows = []
#for each row
for i in range(1):
    tr = content_trs[i]
    #create array to store info for this row
    rowItems = []
    #get the name
    name = tr.find('td').find('a').getText().split(", ")
    for item in name:
      rowItems.insert(0, ((" ".join(item.split())).split(' ', 1)[0]))

    #get the url
    url = "http://members.calbar.ca.gov/" + tr.find('td').find('a').get('href')

    # Load the HTML page
    driver.get(url)
    # Put the page source into a variable and create a BS object from it
    soup_file=driver.page_source
    soupProfile = BeautifulSoup(soup_file, 'html.parser')

    # Find all the emails
    emails = soupProfile.find_all('a', attrs={'class': 'bluenormal'})
    # If the email is available
    if (emails):
        #Grap the obscuring style tag
        style = soupProfile.find('div', attrs={'class': "block block-body body-text"}).find_all('style')[2]
        styleList = str(style).split('{display:')
        index = 0
        for i in range(len(styleList)):
            s = styleList[i]
            if "inline" in s:
                index = i-1
        rowItems.append(emails[index].getText())  
    else:
        rowItems.append('')

    #Find website
    website = soupProfile.find(id='websiteLink')
    if (website):
        rowItems.append(website.getText())
    else:
        rowItems.append('')

    #add row to list
    rows.append(rowItems)

print(rows[0])
# Close the browser
driver.quit()  