import json
import requests
import os
import string
from time import sleep
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
from pprint import pprint

url_page_template = 'http://tululu.org/l55/{}'
#url_book_template = 'http://tululu.org/b{}/'
url_download_txt_template = 'http://tululu.org/txt.php?id={}'

def download_txt(url, filename, folder='books'):
	response = requests.get(url, allow_redirects = False)
	response.raise_for_status()
	if response.status_code==200:
		filepath = os.path.join(folder, sanitize_filename(filename + '.txt'))
		with open(filepath, 'w') as file:
			file.write(response.text)
		return filepath
	
def download_image(url, filename, folder='images'):
	response = requests.get(url, allow_redirects = False)
	response.raise_for_status()
	if response.status_code==200:
		filepath = os.path.join(folder, filename)
		with open(filepath, 'wb') as file:
			file.write(response.content)
		return filepath	

Path('books').mkdir(parents=True, exist_ok=True)
Path('images').mkdir(parents=True, exist_ok=True)

start_page = 700
end_page = 701
books_data = []

for page in range(start_page, end_page):
	url = url_page_template.format(page)
	response = requests.get(url)
	response.raise_for_status()
	soup = BeautifulSoup(response.text, 'lxml')
	books_from_page = soup.select(".bookimage")
	
	for book in books_from_page:
		book_page_href = book.find('a')['href']
		book_page_url = urljoin('http://tululu.org/more', book_page_href)

		response = requests.get(book_page_url, allow_redirects = False)
		response.raise_for_status()
		soup = BeautifulSoup(response.text, 'lxml')

		book_title_text = soup.select_one("h1").text
		book_information = book_title_text.split('::')
		book_title = book_information[0].strip()
		book_author = book_information[1].strip()

		print(book_title)

		comments = [comment.text for comment in soup.select(".texts span")]
		genres = [genre.text for genre in soup.select("span.d_book a")]
		
		book_id = book_page_href.strip('/b')
		book_txt_url = url_download_txt_template.format(book_id)
		book_path = download_txt(book_txt_url, book_title)

		book_image_src = book.find('img')['src']
		book_image_title = book_image_src.split('/')[2]
		book_image_url = urljoin('http://tululu.org/more', book_image_src)
		img_src = download_image(book_image_url, book_image_title)

		book_data = {
				"title": book_title,
				"author": book_author,
				"img_src": img_src,
				"book_path": book_path,
				"comments": comments,
				"genres": genres
				}
		books_data.append(book_data)

with open("books_data.json", "w") as my_file:
  json.dump(books_data, my_file, ensure_ascii = False, indent=2)