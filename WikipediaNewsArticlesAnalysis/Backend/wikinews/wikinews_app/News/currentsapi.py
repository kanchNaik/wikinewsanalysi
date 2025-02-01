import requests

class CurrentsapiAPI:
    def get_news(self, page):
        base_url = f"https://api.currentsapi.services/v1/search?keywords={page}&language=en"
        response = requests.get(base_url)
        response.raise_for_status() 
        return base_url