import requests
class MarketauxAPI:
    MARKET_AUX_API_KEY = "TFCpiF4MR8mkme7nrql0RjS8PLsELCUtW6RsUAkD"
    def __init__(self):
        self.MARKET_AUX_API_KEY = "TFCpiF4MR8mkme7nrql0RjS8PLsELCUtW6RsUAkD"

    def get_news(self, page):
        base_url = f"https://api.marketaux.com/v1/news/all?symbols={page}&filter_entities=true&language=en&api_token={self.MARKET_AUX_API_KEY}"
        response = requests.get(base_url)
        response.raise_for_status() 
        data = response.json()
        articles = data.get('data', [])
        extracted_data_list = []

        if articles:
            for article in articles:

                extracted_data = {
            "title": article.get("title"),
            "description": article.get("description"),
            "url": article.get("url"),
            "url_to_image": article.get("image_url"),
            "source_name": article.get("source"),
            "content": article.get("snippet")}
                
                extracted_data_list.append(extracted_data)

        return extracted_data_list