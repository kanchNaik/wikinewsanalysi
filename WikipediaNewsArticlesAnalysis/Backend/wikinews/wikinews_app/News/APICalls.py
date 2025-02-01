from wikinews_app.News.newsapi import NewsAPI
from wikinews_app.News.currentsapi import CurrentsapiAPI
from wikinews_app.News.marketaux import MarketauxAPI

NEWS_API_KEY = "f049190b6b744976b46acc21a25972f9"
MARKET_AUX_API_KEY = "TFCpiF4MR8mkme7nrql0RjS8PLsELCUtW6RsUAkD"

def make_newsapi_url(page):
        base_url = f"https://newsapi.org/v2/everything?q={page}&sortBy=publishedAt&apiKey={NEWS_API_KEY}&language=en"
        return base_url

def make_currentsapi_url(page):
        base_url = f"https://api.currentsapi.services/v1/search?keywords={page}&language=en"
        return base_url

def make_marketaux_url(page):
        base_url = f"https://api.marketaux.com/v1/news/all?symbols={page}&filter_entities=true&language=en&api_token={MARKET_AUX_API_KEY}"
        return base_url


def get_registered_api_urls():
    print("get_registered_api_urls")
    return [NewsAPI(), MarketauxAPI()]
    
    #return ['a', 'b', 'c']