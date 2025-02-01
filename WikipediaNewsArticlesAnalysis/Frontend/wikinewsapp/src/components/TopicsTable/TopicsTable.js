import React from "react";
import "./TopicsTable.css"; // optional CSS for styling
import { useState, useEffect } from "react";
import axios from "axios";
// import messageService from "../../services/messageService";
// import { BASE_API_URL } from "../../constants/constants";

const TopicsTable = () => {
    const [data, setTopicsData] = useState(null);
    const fetchTopicsData = async () => {
        try {
            const response = await axios.get(`http://localhost:8000/wikinews/api/trending-topics/`);
            setTopicsData(response.data.trending_topics);
            
        } catch (err) {
            console.log(err);
        }
    };

    useEffect(() => {
        fetchTopicsData();
    }, []);

  return (
    <table>
      <thead>
        <tr>
          <th>Rank</th>
          <th>Page</th>
          <th>Pageviews</th>
          <th>Weight</th>
        </tr>
      </thead>
      <tbody>
        {data && data.map((row, index) => (
          <tr key={index}>
            <td>{1}</td>
            <td>{row.page_title}</td>
            <td>{row.view_count}</td>
            <td>{row.decayed_avg}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default TopicsTable;
