import React from "react";
import "./NewsArticleCard.css"; // Add your CSS styles here

const NewsArticleCard = ({ article }) => {
    return (
        <div className="news-card">
            {article.urlToImage && (
                <img
                    src={article.urlToImage}
                    alt={article.title}
                    className="news-card-image"
                />
            )}
            <div className="news-card-content">
                <h2 className="news-card-title">{article.title}</h2>
                <p className="news-card-description">{article.description}</p>
                <p className="news-card-source">
                    Source: <strong>{article.source?.name || "Unknown"}</strong>
                </p>
                <a
                    href={article.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="news-card-link"
                >
                    Read More
                </a>
            </div>
        </div>
    );
};

export default NewsArticleCard;
