from flask import Flask, request, jsonify
from flask_cors import CORS

from fhirclient.models import bundle as b
from fhirclient.models import patient as p


import json
import os

app = Flask(__name__)
CORS(app)


def process_fhir_data(fhir_data):
    patient_details = []
    condition_details = []
    observation_details = []

    bundle = b.Bundle(fhir_data)

    for entry in bundle.entry:
        if entry.resource.resource_type == 'Patient':
            patient_details.append(get_patient_details(entry.resource))
        elif entry.resource.resource_type == 'Condition':
            condition_details.append(get_condition_details(entry.resource))
        elif entry.resource.resource_type == 'Observation':
            observation_details.append(get_observation_details(entry.resource))

    data = {'patient': patient_details,
            'conditions': condition_details,
            'observations': observation_details}

    print(data)

    return data


def get_condition_details(condition):
    condition_details = {}
    if condition.code:
        condition_details['conditionName'] = condition.code.text
    if condition.onsetDateTime:
        onset = condition.onsetDateTime.isostring  # when symptom started

        if condition.abatementDateTime:
            abatement = condition.abatementDateTime.isostring  # when treated
            duration = f"{onset} - {abatement}"
            condition_details['duration'] = duration
        condition_details['duration'] = f'{onset} - present'
    return condition_details


def get_observation_details(observation):
    observation_details = {}
    if observation.code:
        observation_details['observationType'] = observation.code.text

    # value can be a quantity, codeableConcept or string
    if observation.valueQuantity:
        value = observation.valueQuantity.value
        unit = observation.valueQuantity.unit
        formatted_value = f"{value} {unit}"
        observation_details['value'] = formatted_value
    elif observation.valueCodeableConcept:
        observation_details['value'] = observation.valueCodeableConcept.text
    elif observation.valueString:
        observation_details['value'] = observation.valueString

    if observation.effectiveDateTime:
        date = observation.effectiveDateTime.isostring
        observation_details['date'] = date
    return observation_details


def get_patient_details(patient):
    patient_details = {}
    patient_name = patient.name[0]
    given_name = ' '.join(
        patient_name.given) if patient_name.given else ''
    family_name = patient_name.family if patient_name.family else ''
    if given_name or family_name:
        formatted_name = f"{given_name} {family_name}".strip()
        birth_date = patient.birthDate.isostring
        gender = patient.gender
        patient_details = {
            'name': formatted_name,
            'birthDate': birth_date,
            'gender': gender
        }
    return patient_details


# endpoint to process fhir data
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


@app.route('/')  # default route
def index():
    return "FHIR Backend Running"


if __name__ == '__main__':
    app.run(debug=True)
