import React from 'react';

const PatientCard = ({ patient }) => {
  return (
    <div className="patient-card">
      <h3>{patient.name}</h3>
      <p><strong>Birth Date:</strong> {patient.birthDate}</p>
      <p><strong>Gender:</strong> {patient.gender}</p>
      <p><strong>Address:</strong> {patient.address}</p>
    </div>
  );
}

export default PatientCard;