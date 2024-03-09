from flask import Flask, request, jsonify
from flask_cors import CORS

from fhirclient.models import bundle as b
from fhirclient.models import patient as p


import json
import os

app = Flask(__name__)
CORS(app)


def process_fhir_data(fhir_data):
    patient_data = {}

    bundle = b.Bundle(fhir_data)

    for entry in bundle.entry:
        if entry.resource.resource_type == 'Patient':
            patient = entry.resource
            patient_name = patient.name[0]
            given_name = ' '.join(
                patient_name.given) if patient_name.given else ''
            family_name = patient_name.family if patient_name.family else ''
            if given_name or family_name:
                formatted_name = f"{given_name} {family_name}".strip()
                birth_date = patient.birthDate.isostring
                patient_data = {
                    'name': formatted_name,
                    'birthDate': birth_date
                }
    return patient_data


@app.route('/process-fhir-data', methods=['GET'])
def process_fhir_data_route():
    directory = 'data'
    processed_data = []

    for filename in os.listdir(directory):  # processes every json file
        try:
            with open(os.path.join(directory, filename)) as f:
                fhir_data = json.load(f)
                processed_data.append(process_fhir_data(fhir_data))
        except Exception as e:
            app.logger.error(f"Failed to process file {filename}: {e}")

    return jsonify(processed_data)


@app.route('/')
def index():
    return "FHIR Backend Running"


if __name__ == '__main__':
    app.run(debug=True)
