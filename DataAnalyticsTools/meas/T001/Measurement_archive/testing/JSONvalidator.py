import json
from jsonschema import validate, ValidationError

# Pfade zu den Dateien
schema_file = '../../battery_schema.json'
data_file = '../../battery_data.json'

# JSON Schema laden
with open(schema_file, 'r') as sf:
    schema = json.load(sf)

# JSON Daten laden
with open(data_file, 'r') as df:
    data = json.load(df)

# Validierung
try:
    validate(instance=data, schema=schema)
    print("JSON-Data is valid.")
except ValidationError as e:
    print(f"JSON-data is not valid: {e.message}")
