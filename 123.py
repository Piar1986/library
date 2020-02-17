import json
import requests
import os
from time import sleep
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin

save_path = 'books'
Path(save_path).mkdir(parents=True, exist_ok=True)
save_path = 'images'
Path(save_path).mkdir(parents=True, exist_ok=True)


#url_page = 'http://tululu.org/b{}/'
#url_text = 'http://tululu.org/txt.php?id={}'
#filename = 'id{}.txt'

def download_txt(id, folder='books/'):
	url_page = 'http://tululu.org/b{}/'.format(id)
	url_text = 'http://tululu.org/txt.php?id={}'.format(id)
	response = requests.get(url_page, allow_redirects = False)
	response.raise_for_status()
	if response.status_code==200:
		soup = BeautifulSoup(response.text, 'lxml')
		title_tag = soup.find('h1')
		image = soup.find('div', class_="bookimage").find('img')['src']
		print(urljoin('http://tululu.org/more', image))
		title_text = title_tag.text
		text = title_text.split('::')
		book_title = text[0].strip()
		book_author = text[1].strip()
		complete_filename = os.path.join(folder, sanitize_filename(book_title + '.txt'))
		response = requests.get(url_text)
		response.raise_for_status()
		#with open(complete_filename, 'w') as file:
		#	file.write(response.text)
	return
 
def download_image(id, folder='images/'):
	url_page = 'http://tululu.org/b{}/'.format(id)
	response = requests.get(url_page, allow_redirects = False)
	response.raise_for_status()
	if response.status_code==200:
		soup = BeautifulSoup(response.text, 'lxml')

		comments = soup.find_all('div', class_="texts")
		for comment in comments:
			print(comment.find('span').text)

		genres = soup.find('span', class_="d_book").find_all('a')
		for genre in genres:
			print(genre.text)	

		image = soup.find('div', class_="bookimage").find('img')['src']
		image_url = urljoin('http://tululu.org/more', image)
		print(image.split('/'))
		complete_filename = os.path.join(folder, image.split('/')[2])
		response = requests.get(image_url)
		response.raise_for_status()
		with open(complete_filename, 'wb') as file:
			file.write(response.content)	

for n in range(10):
	download_image(n)
	