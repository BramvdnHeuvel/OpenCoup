import json

def read_model(file_name):
    json_data = open(file_name)
    data  = json.load(json_data)
    return data['data']