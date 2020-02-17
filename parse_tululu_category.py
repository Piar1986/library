import json
import requests
import os
import string
from time import sleep
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin

url_page_template = 'http://tululu.org/l55/{}'
url_book_template = 'http://tululu.org/b{}/'
url_download_txt_template = 'http://tululu.org/txt.php?id={}'

def download_txt(url, filename, folder='books/'):
	response = requests.get(url, allow_redirects = False)
	response.raise_for_status()
	if response.status_code==200:
		filepath = os.path.join(folder, sanitize_filename(filename + '.txt'))
		#with open(filepath, 'w') as file:
		#	file.write(response.text)
		#return filepath
	

def download_image(url, filename, folder='images/'):
	response = requests.get(url, allow_redirects = False)
	response.raise_for_status()
	if response.status_code==200:
		#soup = BeautifulSoup(response.text, 'lxml')
		#image = soup.find('div', class_="bookimage").find('img')['src']
		#image_url = urljoin('http://tululu.org/more', image)
		#print(image.split('/'))
		filepath = os.path.join(folder, filename)
		#response = requests.get(image_url)
		#response.raise_for_status()
		with open(filepath, 'wb') as file:
			file.write(response.content)

for n in range(1):
	url = url_page_template.format(n + 1)
	response = requests.get(url)
	response.raise_for_status()
	soup = BeautifulSoup(response.text, 'lxml')
	book_href = soup.find_all('div', class_="bookimage")

	for book in book_href:
		href = book.find('a')['href']
		book_id = href.strip('/b')
		href = book.find('img')['src']

		response = requests.get(url_book_template.format(book_id), allow_redirects = False)
		response.raise_for_status()
		soup = BeautifulSoup(response.text, 'lxml')
		title_tag = soup.find('h1')
		print(title_tag)
		title_text = title_tag.text
		text = title_text.split('::')
		book_title = text[0].strip()
		book_author = text[1].strip()
		'''
		comments = soup.find_all('div', class_="texts")
		for comment in comments:
			print(comment.find('span').text)

		genres = soup.find('span', class_="d_book").find_all('a')
		for genre in genres:
			print(genre.text)
		'''
		book_url = urljoin('http://tululu.org/more', href)
		book_url_txt = url_download_txt_template.format(book_id)
		#download_txt(book_url_txt, book_title)
		href = book.find('img')['src'].strip('/shots')
		download_image(book_url, href)
		
'''
{
	"title":
	"author":
	"img_src":
	"book_path":
	"comments":
	"genres":
}
'''