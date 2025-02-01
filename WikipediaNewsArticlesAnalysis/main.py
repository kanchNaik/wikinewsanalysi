from content_extractor import ContentExtractor
from page_news import PageNews
from summarization import Summarizer

summarizer = Summarizer(True)
page_name = "Donald Trump"
page_news_obj = PageNews(summarizer, page_name)
json_pages = page_news_obj.fetch_news_article(5)

import json
json_pages_parsed = json.loads(json_pages)

print("page_news_obj.articles:", page_news_obj.articles)

for json_page in json_pages_parsed:
    # print(json_page)
    print(json_page["url"])
    # print(json_page["content"])
    summary = page_news_obj.fetch_article_summary(json_page["url"])
    print("summary: ",summary)

print("page_news_obj.articles:", page_news_obj.articles)

page_summary = page_news_obj.fetch_page_summary()

print("page_news_obj.summary:", page_summary)
