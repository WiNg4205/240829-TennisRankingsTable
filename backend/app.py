from bs4 import BeautifulSoup
from selenium import webdriver
    
driver = webdriver.Chrome()
driver.get("https://www.atptour.com/en/rankings/singles?rankRange=0-5000&region=all")
driver.implicitly_wait(0.5)
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')
with open('content.html', 'w') as f:
    f.write(soup.prettify())