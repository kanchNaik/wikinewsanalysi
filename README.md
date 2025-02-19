# WikiNews Insights

## Overview
WikiNews Insights is a real-time analytical tool that establishes a correlation between Wikipedia pageviews and trending news headlines. This project leverages big data technologies to process Wikipedia data on an hourly basis, identify trending topics, and link them to the latest news articles from major news APIs. The insights are presented through interactive dashboards to facilitate decision-making for journalists, researchers, and policymakers.

## Features
- Real-time Wikipedia pageviews analysis
- Integration with trending news headlines
- Summarization of related news articles
- Interactive dashboard for visualization
- Scalable big data pipeline
- Implementation of Decaying Window Algorithm and Locality Sensitive Hashing (LSH)

## Technologies Used
- **Programming Languages**: Python, JavaScript
- **Frameworks**: Django, React.js
- **Big Data Tools**: Apache Kafka, Apache Spark, PySpark
- **Databases**: MongoDB
- **APIs**: Wikimedia EventStreams, NewsAPI, Currents API
- **Web Scraping**: BeautifulSoup
- **Machine Learning**: Text Summarization (LED Model)

## System Architecture
1. **Data Collection**: Fetches Wikipedia pageviews and trending news articles using APIs.
2. **Data Processing**: Filters and aggregates data using Apache Spark and Kafka.
3. **Summarization**: Generates concise summaries of correlated news using transformer-based models.
4. **Visualization**: Displays results on a React.js-based dashboard.

## Installation
1. Clone the repository:
   ```sh
   https://github.com/kanchNaik/wikinewsanalysi.git
   ```
2. Navigate to the project directory:
   ```sh
   cd WikipediaNewsArticlesAnalysis
   ```
3. Set up a virtual environment (optional but recommended):
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
5. Set up the front-end:
   ```sh
   cd frontend
   npm install
   npm start
   ```
6. Run the backend server:
   ```sh
   cd backend
   python manage.py runserver
   ```

## Usage
- Access the dashboard via `http://localhost:3000`.
- Explore trending Wikipedia topics and their correlated news articles.
- View summarized news content for deeper insights.

## Contribution
We welcome contributions! Follow these steps to contribute:
1. Fork the repository.
2. Create a new branch for your feature/fix.
3. Commit your changes with clear messages.
4. Push to your fork and submit a Pull Request.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
