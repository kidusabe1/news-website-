from requests_html import HTMLSession
import traceback
import requests

session=HTMLSession()
url='https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNRE55YXpBU0JXVnVMVWRDS0FBUAE?hl=en-IN&gl=IN&ceid=IN%3Aen'
r=session.get(url)

r.html.render(sleep=1, scrolldown=0)

articles= r.html.find('article')
newslist=[]
for item in articles:
    try: 
        newsitem=item.find('h4',first=True)
        # title = newsitem.text
        pseudo_link= item.find('a')
        # link=pseudo_link[0].absolute_links.pop()
        link=pseudo_link[0].absolute_links.pop()

        news_article={
            'title':newsitem.text,
            'link':link.replace('/topics', '')
        }
        # print(title)
        # print(link)
        newslist.append(news_article)
    except Exception as e:
        print(f"Exception occurred: {e}")
        traceback.print_exc()
# modified_links = [link.replace('/topics', '') for link in links]
print(len(newslist))
print(newslist[0])
# import requests
# from requests_html import HTMLSession
# import traceback

# session = HTMLSession()
# url = 'https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNRE55YXpBU0JXVnVMVWRDS0FBUAE?hl=en-IN&gl=IN&ceid=IN%3Aen'
# r = session.get(url)
# r.html.render(sleep=1, scrolldown=0)

# articles = r.html.find('article')

# for item in articles:
#     try:
#         newsitem = item.find('h4', first=True)
#         title = newsitem.text
#         # pseudo_link = item.find('a')
#         # print(type(pseudo_link))
#         link = newsitem.absolute_links.pop()
        
#         # Send a GET request to the link and get the redirected URL
#         response = requests.get(link)
#         redirected_url = response.url
        
#         print(title)
#         print(redirected_url)
#     except Exception as e:
#         print(f"Exception occurred: {e}")
#         traceback.print_exc()