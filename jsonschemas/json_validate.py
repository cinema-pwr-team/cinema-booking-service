from flask import request
import json
from jsonschema import validate, ValidationError


def validate_request_json(received_request: request, jsonschema_path):
    try:
        incoming_json = received_request.get_json()
    except Exception:
        raise ValidationError("Malformed JSON data")

    with open(jsonschema_path) as validator_file:
        json_validator = json.load(validator_file)
        try:
            validate(incoming_json, schema=json_validator)
            return incoming_json
        except ValidationError as err:
            raise ValidationError(err.message)


def validate_bytes_json(received_bytes: bytes, jsonschema_path):
    json_data = received_bytes.decode('utf-8')
    try:
        incoming_json = json.loads(json_data)
    except Exception:
        raise ValidationError("Malformed JSON data")

    with open(jsonschema_path) as validator_file:
        json_validator = json.load(validator_file)
        try:
            validate(incoming_json, schema=json_validator)
            return incoming_json
        except ValidationError as err:
            raise ValidationError(err.message)
