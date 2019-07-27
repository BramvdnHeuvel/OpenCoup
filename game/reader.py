import json

def read_model(file_name):
    json_data = open(file_name)
    data  = json.load(json_data)
    return data['data']

def write_model(model, file_name='models/recent/last-training.json'):
    with open(file_name, 'w') as outfile:
        json.dump({'data': model.data}, outfile)