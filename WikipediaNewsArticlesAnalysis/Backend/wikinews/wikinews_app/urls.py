from django.urls import path
from . import views

urlpatterns = [
    path('api/trending-topics/', views.get_trending_topics, name='get_trending_topics'),
    path('api/newsarticles/', views.get_news_articles, name='get_news_articles'),
]
