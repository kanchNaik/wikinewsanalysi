import React, { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import axios from "axios";
import NewsArticleCard from "./NewsArticleCard";

const NewsArticles = () => {
    const [searchParams] = useSearchParams();
    const keyword = searchParams.get("keyword"); // Extract the 'keyword' query parameter

    const [data, setArticlesData] = useState(null); // Articles data
    const [loading, setLoading] = useState(true); // Loading state
    const [error, setError] = useState(null); // Error state
    const [page, setSummary] = useState('');

    const fetchTopicsData = async () => {
        try {
            setLoading(true); // Start loading
            console.log(`http://localhost:8000/wikinews/api/newsarticles?keyword=${keyword}`);
            const response = await axios.get(`http://localhost:8000/wikinews/api/newsarticles?keyword=${keyword}`);
            setArticlesData(response.data.articles);
            setSummary(response.data.page_summary);
        } catch (err) {
            console.error(err);
            setError("Failed to fetch articles");
        } finally {
            setLoading(false); // Stop loading
        }
    };

    useEffect(() => {
        fetchTopicsData();
    }, [keyword]); // Refetch data if the keyword changes

    if (loading) {
        return <div>Loading...</div>; // Show loading message while fetching
    }

    if (error) {
        return <div>Error: {error}</div>; // Show error message if something goes wrong
    }

    return (
        <div style={{ display: "flex", gap: "16px" }}>
        <div  style={{ flex: "3", padding: "16px" }}>
            <h1>News Articles</h1>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "16px" }}>
                {data && data.length > 0 ? (
                    data.map((article, index) => (
                        <NewsArticleCard key={index} article={article} />
                    ))
                ) : (
                    <div>No articles found for the given keyword.</div>
                )}
            </div>
            
        </div>
        <div style={{ flex: "1", padding: "16px" }}>
            <h2>Summary</h2>
            <p>{page}</p>
        </div>
        </div>
    );
};

export default NewsArticles;
