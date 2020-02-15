import requests
from bs4 import BeautifulSoup

url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
url = 'http://tululu.org/b1/'
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')
title_tag = soup.find('main').find('header').find('h1')
title_text = title_tag.text
print(title_tag)
print(title_text)

image = soup.find('img', class_='attachment-post-image')['src']
# https://www.franksonnenbergonline.com/wp-content/uploads/2019/10/image_are-you-grateful.jpg
print(image)