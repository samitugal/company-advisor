import csv
import plotly.graph_objects as go
import json

product_names = []
units_in_stock = []

with open('product_stock.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        product_names.append(row['product_name'])
        units_in_stock.append(int(row['units_in_stock']))

fig = go.Figure(data=[
    go.Bar(x=product_names, y=units_in_stock)
])

fig.update_layout(title='Product Stock Quantities', xaxis_title='Product Name', yaxis_title='Units in Stock')

graph_json = fig.to_json()

print(graph_json)