import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from pprint import pp


DATA_URL = 'https://habr.com/ru/all'
KEYWORDS = ['дизайн', 'фото', 'web', 'python', '2025', '2024',
            'библиотека', 'chatGPT', 'победили']
response = requests.get(DATA_URL,
                        headers=Headers(browser='chrome',
                                        os='windows').generate())
soup = BeautifulSoup(response.text, features='lxml')
articles = soup.find_all('article')
data_from_title = ['Совпадения только по заголовку']
data_from_text = ['Совпадения по тексту']
for article in articles:
    article_link = ('https://habr.com' +
                    article.find('a',
                                 class_='tm-article-datetime-published_link')
                    ['href'])
    article_time = article.find('time')['title']
    article_title = article.find('a', class_='tm-title__link')
    article_title = article_title.find('span').text
    contains_keyword_from_title = any(keyword_ in article_title
                                      for keyword_ in KEYWORDS)
    if contains_keyword_from_title:
        data_from_title.append({
            'Заголовок': article_title,
            'Дата': article_time,
            'Ссылка': article_link,
        })
    response = requests.get(article_link,
                            headers=Headers(browser='chrome',
                                            os='windows').generate())
    soup = BeautifulSoup(response.text, features='lxml')
    article_text = soup.find('div',
                             class_='article-formatted-body').text.strip()
    contains_keyword_from_text = any(keyword_ in article_text
                                     for keyword_ in KEYWORDS)
    if contains_keyword_from_text:
        data_from_text.append({
            'Заголовок': article_title,
            'Дата': article_time,
            'Текст': article_text,
            'Ссылка': article_link,
        })


pp(data_from_title)
print('--------------------')
pp(data_from_text)
