import requests
import os
from time import sleep
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

save_path = 'books'
Path(save_path).mkdir(parents=True, exist_ok=True)

url_page = 'http://tululu.org/b1/'
url = 'http://tululu.org/txt.php?id={}'
filename = 'id{}.txt'

response = requests.get(url_page)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'lxml')
title_tag = soup.find('h1')
title_text = title_tag.text
text = title_text.split('::')
print('Заголовок:', text[0].strip())
print('Автор:', text[1].strip())

for n in range(1):
	url_book = url.format(n + 1)
	response = requests.get(url_book, allow_redirects=False)
	response.raise_for_status()

'''
	if response.status_code==200:
		complete_filename = os.path.join(save_path, filename.format(n + 1))
		with open(complete_filename, 'w') as file:
		    file.write(response.text)
'''
fname = "fi:l*e/p\"a?t>h|.t<xt"
print(f"{fname} -> {sanitize_filename(fname)}\n")
sleep(5)

def download_txt(url, filename, folder='books/'):
	return os.path.join(folder, sanitize_filename(filename + '.txt'))
	
	"""response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    text = title_tag.text.split('::')
	return sanitize_filename(text[0])
    Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    # TODO: Здесь ваша реализация

# Примеры использования
url = 'http://tululu.org/txt.php?id=1'

filepath = download_txt(url, 'Алиби')
print(filepath)  # Выведется books/Алиби.txt

filepath = download_txt(url, 'Али/би', folder='books/')
print(filepath)  # Выведется books/Алиби.txt

filepath = download_txt(url, 'Али\\би', folder='txt/')
print(filepath)  # Выведется txt/Алиби.txt