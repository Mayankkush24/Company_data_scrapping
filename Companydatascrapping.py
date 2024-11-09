#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless') 
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=service, options=options)


# In[3]:


target_url = 'https://www.yellowpages.com/search?search_terms=IT+Services&geo_location_terms=San+Francisco%2C+CA'
driver.get(target_url)


# In[4]:


csv_file = open('company_data.csv', mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Company Name', 'Website URL', 'Contact Number', 'Location/Address', 'Industry/Category', 'Company Description', 'Email Address'])


# In[5]:


company_limit = 50
num_pages = 3  
companies_scraped = 0

for page in range(1, num_pages + 1):
    time.sleep(2)  
    
    companies = driver.find_elements(By.CLASS_NAME, 'result')

    for company in companies:
        
        if companies_scraped >= company_limit:
            break

        try:
            company_name = company.find_element(By.CLASS_NAME, 'business-name').text
        except:
            company_name = None

        try:
            website_url = company.find_element(By.CLASS_NAME, 'track-visit-website').get_attribute('href')
        except:
            website_url = None

        try:
            contact_number = company.find_element(By.CLASS_NAME, 'phones').text
        except:
            contact_number = None

        try:
            address = company.find_element(By.CLASS_NAME, 'street-address').text
        except:
            address = None

        industry_category = "IT Services"  

        try:
            description = company.find_element(By.CLASS_NAME, 'snippet').text
        except:
            description = None

        try:
            email_address = company.find_element(By.XPATH, "//a[contains(@href, 'mailto:')]").get_attribute("href").replace('mailto:', '')
        except:
            email_address = None

        csv_writer.writerow([company_name, website_url, contact_number, address, industry_category, description, email_address])
        companies_scraped += 1

    if companies_scraped >= company_limit:
        break

    try:
        next_button = driver.find_element(By.LINK_TEXT, 'Next')
        next_button.click()
    except:
        print("No more pages to navigate.")
        break


# In[6]:


# Close CSV file and browser
csv_file.close()
driver.quit()

print(f'Successfully scraped data for {companies_scraped} companies.')


# In[ ]:




