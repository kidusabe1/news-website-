import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests_html import HTMLSession
import traceback
wine_list = []
image_links = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def step_one(my_url,scroll=0):
    url = my_url
    session = HTMLSession()
    r = session.get(url, headers=headers)

    r.html.render(sleep=1, scrolldown=scroll)
    # Wait for the page to load after scrolling
    soup = BeautifulSoup(r.html.html, features='lxml')
    return soup

soup=step_one('https://www.thereporterethiopia.com/latest-ethiopian-political-news/',3)

def parse(soup):
    articles = soup.find_all('div', class_='td-module-meta-info')
    for item in articles:
        try:
            title = item.find('h3')
            link = title.find('a')['href']  # Extract the URL from the 'href' attribute

            link_soup=step_one(link)
            data=link_soup.find('div',class_='td_block_wrap tdb_single_content tdi_155 td-pb-border-top td_block_template_1 td-post-content tagdiv-type')
            rendered_data=[]
            if data:
                paragraphs=data.find_all('div', attrs={'dir': 'auto'})
                for paragraph in paragraphs:
                    rendered_data.append(paragraph.text)

                paragraphs = data.find_all('p')
                for paragraph in paragraphs:
                    rendered_data.append(paragraph.text)
                
            head_lines=link_soup.find('h1')            
            article = {
                'teaser-title': title.find('a').text,
                'link': link,
                'head_line':head_lines.text,
                'real-data':rendered_data
            }
            wine_list.append(article)

        except Exception as e:
            print(f"Exception occurred: {e}")
            traceback.print_exc()

    images = soup.find_all('div',class_='td-module-thumb')
    for item in images:
        try:
            image_link=item.find('span')['data-bg']
            image_links.append(image_link)
        except Exception as e:
            print(f"Exception occurred: {e}")
            traceback.print_exc()

    

parse(soup)

def conc():
    df=pd.DataFrame(wine_list)
    df['image_links']=image_links
    df.to_csv('newsarticles.csv',index=False)
    print(df[1:4])
conc()








