import requests
from bs4 import BeautifulSoup
import helper
import pandas as pd
import tqdm
import time

BASE_URL = "https://www.premiumbeautynews.com/"

# categories = {
#     "markets-trends": 116,
#     "laws-and-regulations": 28,
#     "science-rd": 15,
#     "packaging-design": 84,
#     "ingredients-and-formulation": 42,
#     "environment": 16,
#     "innovation-new-products": 30,
#     "companies-industry": 98,
#     "industry-buzz": 100,
# }

# use small numbers for demo it will require less time
categories = {
    "markets-trends": 2,
    "laws-and-regulations": 2,
    "science-rd": 2,
}


# ----------------------SCRAP ULRS----------------------------
def scrap_blog_url_by_category(cat):
    result_dict = {}
    for c in cat:
        c_url = BASE_URL + "en/" + c
        print(c_url)
        urls = helper.scrap_blog_urls(c_url, cat[c])
        result_dict[c] = urls
    return result_dict


def create_caturl_dataframe(cat_result_dict):
    data = []
    for key, value in cat_result_dict.items():
        for v in value:
            data.append({"category": key, "url": v})
    df = pd.DataFrame(data)
    df.to_csv("blog_urls.csv", index=False)
    print("DataFrame saved to blog_urls.csv")


# ----------------------SCRAP BLOG DATA BASED ON URLS SCAPRED EARLY------------------------------
def scrap_blog_content(category):
    df1 = base_df[base_df["category"] == category]
    data = []
    for index, row in tqdm.tqdm(df1.iterrows(), total=df1.shape[0]):
        result = helper.scrap_blog_content(row["url"])
        if result:
            data.append(result)
    temp_df = pd.DataFrame(data)
    temp_df.to_csv(f"{category}_content.csv", index=False)


# --------------------- ACTION ------------------------

# scrap_blog_content("industry-buzz")


# 1. First step to scrap urls of blog and save into csv file
# ret_result_dict = scrap_blog_url_by_category(categories)
# create_caturl_dataframe(ret_result_dict)

# 2. Ones the all urls are scrap now scrap blog context
# it will scrap all the blog related to given category and store into csv file
base_df = pd.read_csv("blog_urls.csv")  # url csv file
# scrap_blog_content("markets-trends")  # category name to be scraped


# 3. ones all the blog content is scraped based on category i combined them into one file to filtering
# NOTE: ones the all the data is scraped i move them into data folder for use by app
