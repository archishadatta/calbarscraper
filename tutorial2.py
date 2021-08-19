import collections
import multiprocessing
import os
import time
from pprint import pprint
from bs4 import BeautifulSoup
import urllib.request
import csv
import re

file = open('calbarlawyers.csv', 'w')
writer = csv.writer(file)

# write title row
writer.writerow(['First Name', 'Last Name', 'Email', 'Website'])
# process person function (get row, write info)


def processPerson(x):
    tr = BeautifulSoup(x, 'html.parser')
    # create array to store info for this row
    rowItems = []
    # get the name
    name = tr.find('td').find('a').getText().split(", ")
    for item in name:
        rowItems.insert(0, ((" ".join(item.split())).split(' ', 1)[0]))

    print("Processing " + rowItems[0])

    # get the url
    url = "http://members.calbar.ca.gov/" + tr.find('td').find('a').get('href')

    # Put the page source into a variable and create a BS object from it
    try:
        page = urllib.request.urlopen(url)
    except:
        print("An error occured.")
    soupProfile = BeautifulSoup(page, 'html.parser')

    # Find all the emails
    emails = soupProfile.find(
        'p', attrs={'style': 'padding: 0; margin: 0'}).find_all('span', recursive=False)
    # If the email is available
    if (emails):
        # Grab the obscuring style tag
        style = soupProfile.find(
            'div', attrs={'class': "block block-body body-text"}).find_all('style')[2]
        styleList = str(style).split('{display:')
        # Find the real email index
        index = 0
        for k in range(len(styleList)):
            s = styleList[k]
            if "inline" in s:
                index = k-1
        # Add email to list
        rowItems.append(emails[index].getText())
    else:
        return

    # Find website
    website = soupProfile.find(id='websiteLink')
    if (website):
        rowItems.append(website.getText())
    else:
        rowItems.append('')

    writer.writerow(rowItems)
    return(rowItems)


start = time.time()
if __name__ == '__main__':
    for i in range(4):
        print("Iteration" + str(i))
        url = "http://members.calbar.ca.gov/fal/LicenseeSearch/AdvancedSearch?LastNameOption=b&LastName=&FirstNameOption=b&FirstName=&MiddleNameOption=b&MiddleName=&FirmNameOption=b&FirmName=&CityOption=b&City=&State=&Zip=&District=&County=&LegalSpecialty=&LanguageSpoken=&PracticeArea=37"

        try:
            page = urllib.request.urlopen(url)
        except:
            print("An error occured.")

        soup = BeautifulSoup(page, 'html.parser')

        # get all rows
        rowName = re.compile('^rowASRLodd')
        content_trs = soup.find_all('tr', attrs={'class': rowName})
        print(str(len(content_trs)) + " items")

        # for each row
        pool = multiprocessing.Pool()
        content = [str(item) for item in content_trs]
        pool.map(processPerson, content)

    end = time.time()
    print(f'\n Time to complete: {end - start:.2f}s\n')
    file.close()
