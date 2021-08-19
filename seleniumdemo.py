from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Instantiate an Options object
opts = Options()
opts.add_argument(" --headless")

# Instantiate a webdriver
driver = webdriver.Chrome(options=opts)
# Load the HTML page
driver.get(os.getcwd() +"\\test.html")
# # To scrape a url rather than a local file just do something like this: driver.get("https://your.url")

# Put the page source into a variable and create a BS object from it
soup_file=driver.page_source
soup = BeautifulSoup(soup_file, 'html.parser')
# Load and print the title and the text of the <div>
print(soup.title.get_text())
print(soup.find(id='text').get_text())
# Close the browser
driver.quit()