import React, { useState, useEffect } from 'react';
import axios from 'axios';
import PatientCard from './PatientCard';

const PatientList = () => {
  const [patients, setPatients] = useState([]);

  useEffect(() => {
    const fetchPatients = async () => {
      const response = await axios.post('http://127.0.0.1:5000/process-fhir-data');
      setPatients(response.data);
    };

    fetchPatients();
  }, [])

  return (
    <div className="patient-list">
    {patients.map((patient, index) => (
      <PatientCard key={patient.id || index} patient={patient} />
    ))}
    </div>
  );
}

export default PatientList;
