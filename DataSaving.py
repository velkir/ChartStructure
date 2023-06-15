import json

def save_to_json(rootTrends):
    json_data = [trend.to_dict() for trend in rootTrends]
    json_final = json.dumps(json_data)
    with open('trends.json', 'w') as file:
        file.write(json_final)
