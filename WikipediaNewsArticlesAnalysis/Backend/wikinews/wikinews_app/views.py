from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
import requests
from django.views.decorators.http import require_GET
from .utils.TrendingTopics import read_parquet_files_from_last_hour, get_top_trending_topics
from .News.PageNews import PageNews
from .News.Summarizer import Summarizer
import json

# Create your views here.
output_dir = "C:/Kafka/output/test_output"

def get_trending_topics(request):
    # Step 1: Read the parquet files from the last hour
    data = read_parquet_files_from_last_hour(output_dir)

    # Step 2: Get top 10 trending topics based on precomputed decayed average weight
    top_topics = get_top_trending_topics(data)

    # Convert the top topics to a list of dictionaries
    topics_list = top_topics.select("page_title", "decayed_avg", "total_pageviews").collect()

    # Prepare the response as a list of dictionaries
    trending_topics = [{"page_title": row['page_title'], "decayed_avg": row['decayed_avg'], "view_count": row['total_pageviews']} for row in topics_list]

    # Return the top 10 topics as a JSON response
    return JsonResponse({"trending_topics": trending_topics}, safe=False)


def get_news_articles(request):
    keyword = request.GET.get('keyword', '')  
    summarizer = Summarizer()
    print(keyword)
     
    try:
        if not keyword:
            return JsonResponse({'error': 'Keyword parameter is required.'}, status=400)
        
        page_news_obj = PageNews(summarizer, keyword)
        (urls, json_pages) = page_news_obj.fetch_news_article(5)
        json_pages_parsed = json.loads(json_pages)

        for json_page in json_pages_parsed:
            # print(json_page)
            print(json_page["url"])
            # print(json_page["content"])
            summary = page_news_obj.fetch_article_summary(json_page["url"])

        page_summary = page_news_obj.fetch_page_summary()
        
        return JsonResponse({'keyword': keyword, 'articles': json_pages_parsed, 'urls': urls, 'page_summary': page_summary}, status=200)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred.', 'details': str(e)}, status=500)
    

# def get_news_summary(request):
#     summarizer = Summarizer()
     
#     try:
#         page_news_obj = PageNews(summarizer, '')
#         (urls, json_pages) = page_news_obj.fetch_api_responses(5)
#         json_pages_parsed = json.loads(json_pages)
        
#         return JsonResponse({'keyword': keyword, 'articles': json_pages_parsed, 'urls': urls}, status=200)
#     except Exception as e:
#         return JsonResponse({'error': 'An error occurred.', 'details': str(e)}, status=500)
