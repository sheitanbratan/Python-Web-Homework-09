import json
import requests
from bs4 import BeautifulSoup


URL = 'https://quotes.toscrape.com/page/'
page_num = 1

authors_set = set()


def save_to_json(filename, new_data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(new_data, file, ensure_ascii=False, indent=1)


def authors_scrapping_func(links):
    url_base = 'http://quotes.toscrape.com'
    data = []
    for link in links:
        full_url = url_base + link
        print(f'    {full_url}')
        response = requests.get(full_url)
        soup = BeautifulSoup(response.text, 'lxml')

        full_name = soup.find('h3', class_='author-title')
        born_date = soup.find('span', class_='author-born-date')
        born_location = soup.find('span', class_='author-born-location')
        description = soup.find('div', class_='author-description')

        author_data = {
            'fullname': full_name.text,
            'born_date': born_date.text,
            'born_location': born_location.text,
            'description': description.text.strip()
        }
        data.append(author_data)
    return data


def quotes_scrapping_func():
    global page_num
    global authors_set
    data = []

    full_url = URL + str(page_num)
    print(f'    {full_url}')

    response = requests.get(full_url)
    soup = BeautifulSoup(response.text, 'lxml')

    quotes = soup.find_all('span', class_='text')
    authors = soup.find_all('small', class_='author')
    tags = soup.find_all('div', class_='tags')

    authors_urls = soup.find_all('a', string='(about)', href=True)
    [authors_set.add(a_url['href']) for a_url in authors_urls]

    for i in range(0, len(quotes)):
        quote = quotes[i].text
        author = authors[i].text
        tagsforquote = tags[i].find_all('a', class_='tag')
        tags_list = []
        for tagforquote in tagsforquote:
            tags_list.append(tagforquote.text)
        quote_data = {
            'tags': tags_list,
            'author': author,
            'quote': quote
        }
        data.append(quote_data)

    next_page = soup.find('li', class_='next')
    if next_page:
        page_num += 1
        data += quotes_scrapping_func()

    return data


if __name__ == "__main__":
    print('Quotes pages scrapping:')
    quotes_data = quotes_scrapping_func()
    save_to_json('quotes.json', quotes_data)
    print('Authors pages scrapping:')
    authors_data = authors_scrapping_func(authors_set)
    save_to_json('authors.json', authors_data)
