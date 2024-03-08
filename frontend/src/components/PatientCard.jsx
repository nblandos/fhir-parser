import React from "react";

const PatientCard = ({ patient }) => {
  console.log(patient[0]);

  return (
    <div className="patient-card">
      <h3>{patient.name}</h3>
      <p>{patient.birthDate}</p>
    </div>
  );
};

export default PatientCard;
