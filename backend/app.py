from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os


app = Flask(__name__)
CORS(app)


def process_fhir_data(fhir_data):
    processed_patients = []
    for entry in fhir_data['entry']:
        if entry['resource']['resourceType'] == 'Patient':
            patient_data = entry['resource']

            name = patient_data['name'][0]['family'] + \
                ', ' + ' '.join(patient_data['name'][0]['given'])
            birthDate = patient_data['birthDate']
            gender = patient_data['gender']
            address = ', '.join(patient_data['address'][0].get('line', [])) + ', ' + \
                patient_data['address'][0].get('city', '') + ', ' + \
                patient_data['address'][0].get('state', '')

            processed_patients.append({
                'name': name,
                'birthDate': birthDate,
                'gender': gender,
                'address': address
            })

    return processed_patients


@app.route('/process-fhir-data', methods=['POST'])
def process_fhir_data_route():
    directory = 'data'
    processed_data = []

    for filename in os.listdir(directory):  # processes every json file
        with open(os.path.join(directory, filename)) as f:
            fhir_data = json.load(f)
            processed_data.append(process_fhir_data(fhir_data))

    return jsonify(processed_data)


@app.route('/')
def index():
    return "FHIR Backend Running"


if __name__ == '__main__':
    app.run(debug=True)
