import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
url = 'http://tululu.org/b9/'
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')
'''
title_tag = soup.find('main').find('header').find('h1')
title_text = title_tag.text
print(title_tag)
print(title_text)
'''
image = soup.find('div', class_="bookimage").find('img')['src']
#image = soup.find('img', class_='attachment-post-image')['src']
# https://www.franksonnenbergonline.com/wp-content/uploads/2019/10/image_are-you-grateful.jpg

print(urljoin('http://tululu.org/more', image))

comments = soup.find_all('div', class_="texts")
for comment in comments:
	print(comment.find('span').text)

genres = soup.find('span', class_="d_book").find_all('a')

for genre in genres:
	print(genre.text)
