import React, { useState } from 'react';
import SearchBar from './components/SearchBar';
import JournalistCard from './components/JournalistCard';

const App = () => {
  const [journalists, setJournalists] = useState([]);
  
  const fetchJournalists = async (query) => {
    try {
      const response = await fetch(`https://filthy-reeba-saelent.koyeb.app/fetch_journalists?query=${query}&language=en&page_size=10`);
      const data = await response.json();
      // Assuming the response is an array of journalist objects
      setJournalists(data);
    } catch (error) {
      console.error('Error fetching journalists:', error);
    }
  };

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-semibold mb-4">Journalist Search</h1>
      <SearchBar onSearch={fetchJournalists} />
      <div className="mt-8">
        {journalists.map((journalist, index) => (
          <JournalistCard key={index} journalist={journalist} />
        ))}
      </div>
    </div>
  );
};

export default App;
