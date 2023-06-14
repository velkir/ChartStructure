import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json
import time
import Data_preprocess

# Загрузка данных OHLC из CSV
df = pd.read_csv('ohlc.csv')
# df = Data_preprocess.convert_to_heiken_ashi(Data_preprocess.download_ccxt(Market="BTC/USDT", Since='2021-10-01T00:00:00Z', To='2023-06-23T00:00:00Z',Timeframe="1d"))


# Парсим JSON и добавляем линии на график
json_path = 'trends.json'
with open(json_path, 'r') as file:
    data = json.load(file)

# data = json.loads(json_string)

def extract_data(data):
    results = []
    for d in data:
        results.append({
            "start_point": d['point0'],
            "start_timestamp": datetime.strptime(d['timestampstart'], "%Y-%m-%dT%H:%M:%S"),
            "end_point": d['point1'],
            "end_timestamp": datetime.strptime(d['timestampend'], "%Y-%m-%dT%H:%M:%S")
        })
        if 'children' in d and d['children']:
            results.extend(extract_data(d['children']))
    return results

def extract_nested_data(data):
    results = []
    for d in data:
        results.extend(extract_data([d]))
    return results

fig = go.Figure(data=[go.Ohlc(x=df['timestamp'],
                open=df['OPEN'],
                high=df['HIGH'],
                low=df['LOW'],
                close=df['CLOSE'])])

extracted_data = extract_nested_data(data)

for line in extracted_data:
    fig.add_trace(go.Scatter(
        x=[line['start_timestamp'], line['end_timestamp']],
        y=[line['start_point'], line['end_point']],
        mode='lines',
        name=str(line['start_timestamp']) + ' to ' + str(line['end_timestamp']),
        line=dict(color='purple')  # Можно выбрать цвет линий
    ))

# Добавим текущий timestamp в название файла
current_time = time.strftime("%Y%m%d-%H%M%S")
fig.write_image(f"data/chart_{current_time}.jpg", scale=10, width=1920, height=1024)  # Сохраняем в jpg формате с более высоким разрешением
fig.show()