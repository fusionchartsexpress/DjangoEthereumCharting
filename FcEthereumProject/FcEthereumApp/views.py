import json
import requests
from django.shortcuts import render
from django.http import HttpResponse
from collections import OrderedDict

# Add your access key for coinlayer
ACCESS_KEY = 'YOUR_KEY'

# Include the `fusioncharts.py` file that contains functions to embed the charts.
from .fusioncharts import FusionCharts

# Call the coinlayer API and get the rates and return the array of key-value pairs
# Key is label and value is the ETH price
def get_data_arr():
  json_data_arr = []
  for i in range(31):
      # Construct the query
      date = '2021-01-'+ '{:02d}'.format(i+1)
      query = 'http://api.coinlayer.com/' + date
      query += '?access_key=' + ACCESS_KEY 
      query += '&symbols=ETH'
      # Get the response
      response = requests.get(query)
      # Check if response is OK
      if response.status_code != 200:
        return [{'label': 'error', 'value': 0}]
      # Status is OK  
      data = response.json()
      obj = {'label': date, 'value': data['rates']['ETH']}
      json_data_arr.append(obj)
  return json_data_arr      

def renderChart(request):
  # The `chartConfig` dict contains key-value pairs of data for chart attribute
  chartConfig = OrderedDict()
  chartConfig["caption"] = "Ethereum Rates for January 2021"
  chartConfig["subCaption"] = "Source:  https://coinlayer.com"
  chartConfig["xAxisName"] = "Date"
  chartConfig["yAxisName"] = "Price (USD)"
  chartConfig["numberSuffix"] = "$"
  chartConfig["theme"] = "fusion"
# Chart data is passed to the `dataSource` parameter, like a dictionary in the form of key-value pairs.
  dataSource = OrderedDict()
  dataSource["chart"] = chartConfig
  dataSource["data"] = get_data_arr() 
  


# Create an object for the line chart using the FusionCharts class constructor
# The chart data is passed to the `dataSource` parameter.
  line_chart = FusionCharts("line", "Historical-Ethereum", "800", "600", "chart-container", "json", dataSource)
  return render(request, 'index.html', {
    'output': line_chart.render()
})