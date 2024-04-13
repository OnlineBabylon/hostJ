// src/components/JournalistCard.js
import React from 'react';

const JournalistCard = ({ journalist }) => {
  const { Person, Company } = journalist;
  
  return (
    <div className="bg-white shadow-lg rounded-lg p-4 mb-4">
      <h2 className="text-lg font-semibold">{Person.Name}</h2>
      <p className="text-gray-600 mb-2">Title: {Person.Title}</p>
      <p className="text-gray-600 mb-2">Employment: {Person.Employment}</p>
      <p className="text-gray-600 mb-2">Location: {Person.Location}</p>
      <p className="text-gray-600 mb-2">Email: {Person.Email}</p>
      <p className="text-gray-600 mb-2">Linkedin: {Person.Linkedin}</p>
      <p className="text-gray-600 mb-2">Phone: {Company.Phone}</p>
      <p className="text-gray-600 mb-2">Twitter: {Company.Twitter}</p>
      <p className="text-gray-600 mb-2">Linkedin: {Company.Linkedin}</p>
      <p className="text-gray-600 mb-2">Company: {Company.Name}</p>
      <p className="text-gray-600 mb-2">Description: {Company.Description}</p>
      <p className="text-gray-600 mb-2">Location: {Company.Location}</p>
      <p className="text-gray-600 mb-2">Domain: {Company.Domain}</p>
    </div>
  );
};

export default JournalistCard;
