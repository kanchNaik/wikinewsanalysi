import requests
from bs4 import BeautifulSoup


class ContentExtractor:

    def scrape_nyt_article(self, url):
        # Set custom headers including a User-Agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        }

        # Send a GET request to the URL
        try:
            response = requests.get(url, headers=headers)

            # Check if the response indicates a login requirement
            if response.status_code == 401:  # Unauthorized
                print("Login is required to access this page.")
                return None
            elif response.status_code == 403:  # Forbidden
                print("Access to this page is forbidden. You may need to check for login requirements or scraping restrictions.")
                return None
            elif response.status_code == 200:  # Successful response
                print("Page accessed successfully.")
                return response.text
            else:
                print(f"Failed to access the page. Status code: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def parse_article(self, content):
        # Parse the article content using BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')

        # Safely extract title
        title_tag = soup.find('h1')
        title = title_tag.get_text() if title_tag else "No Title Found"

        # Safely extract paragraphs
        paragraphs = soup.find_all('p')
        article_text = "\n".join([para.get_text() for para in paragraphs if para])  # Added check if para exists

        return title, article_text


    def fetch_content(self,url):
        page_content = self.scrape_nyt_article(url)
        if page_content:
            title, article_text = self.parse_article(page_content)
            return title, article_text
