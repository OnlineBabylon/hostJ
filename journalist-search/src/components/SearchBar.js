// src/components/SearchBar.js
import React, { useState } from 'react';

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  const handleChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-center">
      <input
        type="text"
        value={query}
        onChange={handleChange}
        placeholder="Search journalists..."
        className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500"
      />
      <button type="submit" className="ml-2 px-4 py-2 bg-blue-500 text-white rounded-md">
        Search
      </button>
    </form>
  );
};

export default SearchBar;
