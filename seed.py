import requests
from bs4 import BeautifulSoup
import connect
import json
from models import Author, Quote

# функція для парсингу сторінок
def parsing_authors(url_page):
    url = url_page
    next_page = True
    html_doc = requests.get(url)
    if html_doc.status_code == 200:
        soup = BeautifulSoup(html_doc.content, 'html.parser')
        
        # перевіряємо, чи існує наступна сторінка
        is_next_page = soup.select('li.next')
        if is_next_page == []:
            next_page = False
      
        all_authors = soup.select('div.row')[1].find_all('small')
        for author in all_authors:
            # парсимо повне ім'я
            full_name = author.text
            
            # готуємо url для парсингу дати та місця народження, опису автора
            full_name_url = full_name.replace(".", " ").replace("  ", " ").replace(" ", "-").replace("é", "e")
            url_author = base_url + "author/" + full_name_url
            
            # парсимо дані авторів
            html_author = requests.get(url_author)
            soup_author = BeautifulSoup(html_author.content, 'html.parser')
            
            # парсимо дату народження
            born_date = soup_author.find('span', class_='author-born-date').text
            
            # парсимо місце народження
            born_location = soup_author.find('span', class_='author-born-location').text

            # парсимо опис
            description = soup_author.find('div', class_='author-description').text.strip()
            
            if full_name not in authors_names:
                authors_names.append(full_name)
                authors.append({
                    "fullname" : full_name, 
                    "born_date" : born_date, 
                    "born_location" : born_location,
                    "description" : description
                    })
    return next_page

def parsing_quotes(url_page):
    url = url_page
    html_doc = requests.get(url)
    if html_doc.status_code == 200:
        soup = BeautifulSoup(html_doc.content, 'html.parser')
        all_quotes = soup.select('div.row')[1].find_all('div', class_='quote')
        for quote_info in all_quotes:
            # парсимо автора
            author = quote_info.find('small', class_='author').text
            
            # парсимо цитату
            quote = quote_info.find('span', class_='text').text

            # парсимо теги
            all_tags = quote_info.find_all('a', class_='tag')
            tags = []
            for tag in all_tags:
                tags.append(tag.text)

            
            quotes.append({
                "tags" : tags,
                "author" : author,
                "quote" : quote
                })






authors_names = []
authors = []
quotes = []
page = 1
next_page = True
base_url = 'https://quotes.toscrape.com/'

# в циклі парсимо всі сторінки для пошуку авторів
while next_page:
    current_url_page = base_url + "/page/" + str(page) + "/"
    next_page = parsing_authors(current_url_page)
    parsing_quotes(current_url_page)
    page += 1

# створюємо файл authors.json та наповнюємо його даними за результатами парсингу
with open('authors.json', 'w', encoding='utf-8') as f:
    json.dump(authors, f, ensure_ascii=False, indent=4)

# створюємо файл quotes.json та наповнюємо його даними за результатами парсингу
with open('quotes.json', 'w', encoding='utf-8') as f:
    json.dump(quotes, f, ensure_ascii=False, indent=4)


with open("authors.json", "r", encoding="utf-8") as f:
    data_from_authors = json.load(f)
    for record in data_from_authors:
        author = Author(
            fullname = record['fullname'], 
            born_date = record['born_date'], 
            born_location = record['born_location'], 
            description = record['description'])
        author.save()

with open("quotes.json", "r", encoding="utf-8") as f:
    data_from_quotes = json.load(f)
    for record in data_from_quotes:
        author = Author.objects(fullname=record['author']).first()
        if author:
            quote = Quote(
                tags=record['tags'],
                author=author,
                quote=record['quote']
            )
            quote.save()


