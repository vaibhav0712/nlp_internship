import requests
from bs4 import BeautifulSoup
import helper
import pandas as pd
import tqdm
import time

BASE_URL = 'https://www.premiumbeautynews.com   /'
base_df = pd.read_csv('blog_urls.csv')

categories = {
    'markets-trends': 116,
    'laws-and-regulations': 28,
    'science-rd': 15,
    'packaging-design': 84,
    'ingredients-and-formulation': 42,
    'environment': 16,
    'innovation-new-products': 30,
    'companies-industry': 98,
    'industry-buzz': 100
}


def scrap_blog_url_by_category(cat):
    result_dict = {}
    for c in cat:
        c_url = BASE_URL + 'en/' + c
        print(c_url)
        urls = helper.scrap_blog_urls(c_url, cat[c])
        result_dict[c] = urls
    return result_dict


def create_caturl_dataframe(cat_result_dict):
    data = []
    for key, value in cat_result_dict.items():
        for v in value:
            data.append({'category': key, 'url': v})
    df = pd.DataFrame(data)
    df.to_csv('temp_blog_urls.csv', index=False)
    print("DataFrame saved to blog_urls.csv")


def scrap_blog_content(category):
    df1 = base_df[base_df['category'] == category]
    data = []
    for index, row in tqdm.tqdm(df1.iterrows(), total=df1.shape[0]):
        result = helper.scrap_blog_content(row['url'])
        if result:
            data.append(result)
    temp_df = pd.DataFrame(data)
    temp_df.to_csv(f'{category}_content.csv', index=False)


# action
# ret_result_dict = scrap_blog_url_by_category(categories)
# create_caturl_dataframe(ret_result_dict)
scrap_blog_content('industry-buzz')

