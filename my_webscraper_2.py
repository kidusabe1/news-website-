# import requests
# from bs4 import BeautifulSoup

# wine_list = []

# url = 'https://www.thereporterethiopia.com/latest-ethiopian-political-news/'

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }

# r = requests.get(url, headers=headers)
# soup = BeautifulSoup(r.content, features='lxml')

# articles = soup.find_all('div', class_='tdb-module-title-wrap')
# for item in articles:
#     try:
#         title = item.find('h3')
#         link = title.find('a')['href']  # Extract the URL from the 'href' attribute
#         article = {
#             'title': title.text,
#             'link': link
#         }
#         wine_list.append(article)

#     except:
#         print("Failed")
#         pass

# print(wine_list)


import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests_html import HTMLSession
wine_list = []

url = 'https://www.thereporterethiopia.com/latest-ethiopian-political-news/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

session = HTMLSession()
r = session.get(url, headers=headers)

r.html.render(sleep=1, scrolldown=1)

# Wait for the page to load after scrolling

soup = BeautifulSoup(r.html.html, features='lxml')

articles = soup.find_all('div', class_='td-module-meta-info')
for item in articles:
    try:
        title = item.find('h3')
        link = title.find('a')['href']  # Extract the URL from the 'href' attribute
        article = {
            'title': title.find('a').text,
            'link': link
        }
        wine_list.append(article)

    except:
        print("Failed")
        pass

df=pd.DataFrame(wine_list)
df.to_csv('newsarticles.csv',index=False)









# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup
# import time
# wine_list = []

# url = 'https://www.thereporterethiopia.com/latest-ethiopian-political-news/'

# # Set up Chrome WebDriver with Selenium
# chrome_options = Options()
# chrome_options.add_argument('--headless')  # Run Chrome in headless mode
# driver = webdriver.Chrome(options=chrome_options)

# driver.get(url)

# # Wait for the page to fully render (adjust the sleep time as needed)
# time.sleep(5)

# # Extract the page source after rendering
# page_source = driver.page_source

# driver.quit()

# soup = BeautifulSoup(page_source, 'html.parser')

# articles = soup.find_all('div', class_='tdb-module-title-wrap')
# for item in articles:
#     try:
#         title = item.find('h3')
#         link = title.find('a')['href']  # Extract the URL from the 'href' attribute
#         article = {
#             'title': title.text,
#             'link': link
#         }
#         wine_list.append(article)

#     except:
#         print("Failed")
#         pass

# print(wine_list[0])