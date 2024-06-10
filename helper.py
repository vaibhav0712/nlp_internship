import requests
from bs4 import BeautifulSoup
BASE_URL = 'https://www.premiumbeautynews.com/'
username, password = open('auth.txt', 'r').read().split('\n')


def proxy_request(url):
    """
    This function makes a request to the Oxylabs API
    :param url:
    :return: beautiful soup object
    """
    try:
        payload = {
            'source': 'universal',
            'url': url
        }

        response = requests.request(
            'POST',
            'https://realtime.oxylabs.io/v1/queries',
            auth=(username, password),
            json=payload
        )
        html_response = response.json()['results'][0]['content']
        return BeautifulSoup(html_response, 'html.parser')
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None


def direct_request(url):
    """
    This function makes a direct request to the website
    :param url:
    :return: beautiful soup object
    """
    html_content = requests.get(url).content
    return BeautifulSoup(html_content, 'html.parser')


def scrap_blog_content(url):
    """
    This function scrapes the content of the blog post
    :param url:
    :return: dictionary of the {title, text}
    """
    try:
        soup = proxy_request(url)
        if soup:
            title = soup.find(class_='article-title').text
            text_selection = soup.find(class_='article-text')
            text = ' '.join([p.text for p in text_selection.find_all('p')])
            return {'title': title, 'text': text}
        else:
            return None
    except Exception as e:
        print('Error:', e)
        return None


def scrap_blog_urls(url, pages):
    """
    This function scrapes the urls of the blog posts of specific category
    :param url:
    :param pages:
    :return: list of urls
    """
    blog_urls = []
    try:
        for page in range(1, pages):
            print('scraping page:', page)
            page_url = url + f'?debut_rub_lastart={page*10}#pagination_rub_lastart'
            soup = proxy_request(page_url)
            if soup:
                blog_section = soup.find(id='post-list')
                selection = blog_section.find_all(class_='post-thumb')
                urls = [BASE_URL + url.find('a').get('href') for url in selection]
                blog_urls.extend(urls)

        return blog_urls
    except Exception as e:
        print('Error:', e)
        return blog_urls




