import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import NewsArticles from './components/NewsArticles/NewsArticles';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/news" element={<NewsArticles/>} />
      </Routes>
    </div>
  );
}

export default App;
