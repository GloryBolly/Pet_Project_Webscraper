import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_url(session, url):
    try:
        response = session.get(url)
        response.raise_for_status()
        return response
    except (requests.HTTPError, requests.ConnectionError) as e:
        print(f"Failed to fetch {url}: {e}")
        return None

def parse_news_list(session, url):
    response = fetch_url(session, url)
    if response is None:
        return [], []

    soup = BeautifulSoup(response.text, 'lxml')
    news = soup.findAll('li', class_='parts-page__item')

    data_url = []
    data_title = []
    for ele in news:
        link = ele.find('a', class_='card-full-news _parts-news')
        if link is None:
            continue
        relative_url = link.get("href")
        url_news = urljoin(url, relative_url)
        title_news = link.find('h3', class_="card-full-news__title")
        if title_news is None:
            continue
        data_url.append(url_news)
        data_title.append(title_news.text)
    return data_url, data_title

def fetch_news_content(session, url):
    response = fetch_url(session, url)
    if response is None:
        return None

    soup = BeautifulSoup(response.text, 'lxml')
    content = soup.find('div', class_="topic-body _news")
    if content is None:
        return None

    return content.find('div',class_="topic-body__content").text

def main():
    base_url = "https://lenta.ru/parts/news/1/"
    with requests.Session() as session:
        data_url, data_title = parse_news_list(session, base_url)

        data_txt = []
        for url in data_url:
            news_content = fetch_news_content(session, url)
            if news_content is not None:
                data_txt.append(news_content)

        with open('myfile.txt', 'w') as f:
            for item in data_txt:
                f.write("%s\n" % item)

if __name__ == "__main__":
    main()
