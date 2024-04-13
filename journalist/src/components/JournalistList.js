// src/components/JournalistList.js
import React, { useState } from 'react';
import axios from 'axios';

const JournalistList = () => {
  const [journalists, setJournalists] = useState([]);
  const [query, setQuery] = useState('');

  const fetchJournalists = async () => {
    try {
      const response = await axios.get(`http://filthy-reeba-saelent.koyeb.app/fetch_journalists?query=${query}&language=en`);
      setJournalists(response.data);
    } catch (error) {
      console.error('Error fetching journalists:', error);
    }
  };

  const handleChange = (event) => {
    setQuery(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    fetchJournalists();
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="text" value={query} onChange={handleChange} placeholder="Enter query" />
        <button type="submit">Search</button>
      </form>
      <ul>
      {journalists.map((journalist, index) => (
  <li key={index}>
    <h3>{journalist.title}</h3>
    <p>{journalist.description}</p>
    <p>Author: {journalist.author}</p>
    <p>Publication: {journalist.publication}</p>
    <p>Published At: {new Date(journalist.publishedAt).toLocaleDateString()}</p>
    <a href={journalist.url} target="_blank" rel="noopener noreferrer">Read more</a>
    {journalist.urlToImage && <img src={journalist.urlToImage} alt="Article" />}
  </li>
))}

      </ul>
    </div>
  );
};

export default JournalistList;
