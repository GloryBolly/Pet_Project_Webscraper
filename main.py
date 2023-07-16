import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = "https://lenta.ru/parts/news/1/"

with requests.Session() as session:  # Используйте сессию для повторного использования соединений
    response = session.get(base_url)
    response.raise_for_status()  # Бросьте исключение, если запрос не удался

    soup = BeautifulSoup(response.text, 'lxml')

    news = soup.findAll('li', class_='parts-page__item')

    data_url = []
    data_title =[]
    for ele in news:
        try:
            relative_url = ele.find('a', class_='card-full-news _parts-news').get("href")
            url_news = urljoin(base_url, relative_url)  # Используйте urljoin для создания полного URL
            title_news = ele.find('a', class_='card-full-news _parts-news').find('h3', class_="card-full-news__title").text
            data_url.append(url_news)
            data_title.append(title_news)
        except AttributeError:
            pass

    data_txt = []
    for data in data_url:
        try:
            response = session.get(data)
            response.raise_for_status()  # Бросьте исключение, если запрос не удался
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                new_title = soup.find('div', class_="topic-body _news").find('div',class_="topic-body__content").text
                data_txt.append(new_title)
        except AttributeError:
            pass

print(data_txt)

with open('myfile.txt', 'w') as f:
    # Проходим по каждому элементу списка и записываем его в файл
    for item in data_txt:
        f.write("%s\n" % item)
