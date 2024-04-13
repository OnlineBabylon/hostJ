// src/components/JournalistCard.js
import React from 'react';

const JournalistCard = ({ journalist }) => {
  const { author, company, country, description, email, first_name, last_name, location, position, twitter, linkedin, name, phone, time_zone, domain } = journalist;
  
  const renderField = (label, value) => (
    <p className="text-gray-600 mb-2">
      <span className="font-semibold">{label}:</span> {value || 'N/A'}
    </p>
  );

  return (
    <div className="bg-white shadow-lg rounded-lg p-4 mb-4">
      <h2 className="text-lg font-semibold">Author: {author}</h2>
      <div className="mt-4">
        <h3 className="text-gray-800 text-lg font-semibold mb-2">Journalist Info</h3>
        {renderField('First Name', first_name)}
        {renderField('Last Name', last_name)}
        {renderField('Email', email)}
        {renderField('Country', country)}
        {renderField('Position', position)}
        {renderField('Twitter', twitter)}
        {renderField('Linkedin', linkedin)}
        {renderField('Phone', phone)}
        {renderField('Time Zone', time_zone)}
      </div>
      <div className="mt-4">
        <h3 className="text-gray-800 text-lg font-semibold mb-2">Company Info</h3>
        {renderField('Name', name)}
        {renderField('Description', description)}
        {renderField('Location', location)}
        {renderField('Domain', domain)}
      </div>
    </div>
  );
};

export default JournalistCard;
