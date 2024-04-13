import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [query, setQuery] = useState('');
  const [journalists, setJournalists] = useState([]);

  const fetchJournalists = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/fetch_journalists?query=${query}`);
      setJournalists(response.data);
    } catch (error) {
      console.error('Error fetching journalists:', error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Journalist Search</h1>
      <div className="mb-4">
        <input
          type="text"
          placeholder="Enter your query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="border p-2 w-full"
        />
        <button onClick={fetchJournalists} className="bg-blue-500 text-white px-4 py-2 ml-2">Search</button>
      </div>
      <div>
        {journalists.map((journalist, index) => (
          <div key={index} className="border p-4 mb-4">
            <h2 className="text-xl font-bold mb-2">{journalist.author}</h2>
            <p>{journalist.description}</p>
            <a href={journalist.url} target="_blank" rel="noopener noreferrer" className="text-blue-500">Read more</a>
            <img src={journalist.urlToImage} alt={journalist.title} className="mt-2" style={{ maxWidth: '100%' }} />
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;
