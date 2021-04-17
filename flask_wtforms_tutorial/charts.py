'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 

This is where you should add your code to function query the api
'''
import requests
from datetime import datetime
from datetime import date
import pygal
import requests
import json


#api docs https://www.alphavantage.co/documentation/
def getData(time_series,symbol,chart_type,start_date,end_date):
    api_key = "65210ZZ38CVFIWM4"

    apistring = "https://www.alphavantage.co/query?function="
    if (time_series == "1"):
        time_series = "TIME_SERIES_INTRADAY"
        time = "Time Series (30min)"
    elif (time_series == "2"):
        time_series = "TIME_SERIES_DAILY"
        time = "Time Series (Daily)"
    elif (time_series == "3"):
        time_series = "TIME_SERIES_WEEKLY"
        time = "Weekly Time Series"
    elif (time_series == "4"):
        time_series = "TIME_SERIES_MONTHLY"
        time = "Monthly Time Series"
    apistring = (apistring + (time_series + "&symbol=" + symbol))
    if (time_series == "TIME_SERIES_INTRADAY"):
        apistring += "&interval=30min"
    apistring = apistring + ("&apikey=" + api_key)
    

    
    data = requests.get(apistring).json()
 
  
    
    # variables for data transfer to lists.
    x = 0
    newdata = {}
    datedata = []
    newdate = []
    opendata = []
    highdata =[]
    lowdata = []
    closeddata = []
  
    try:
        for key, value in data[time].items():
            datedata = list(data[time].keys())
            x+=1
            holder = {x : value}
            newdata.update(holder)
    except KeyError:
            err = "error"
            return err        
    
    for i in range(0, len(datedata)):
        if(datedata[i] >= start_date and datedata[i] <= end_date):
            newdate.append(datedata[i])
            opendata.append(newdata[i + 1]['1. open'])
            highdata.append(newdata[i + 1]['2. high'])
            lowdata.append(newdata[i + 1]['3. low'])
            closeddata.append(newdata[i + 1]['4. close'])
   
    # method to convert data in list to float for chart data.
    def convert(data):
        for i in range(0, len(data)):
            data[i] = float(data[i])
        return data
    
    # if statement to choose a line or bar chart and display onto default browser.
    if (chart_type == '1'):
        bar_chart = pygal.Bar(x_label_rotation = 70)
        bar_chart.title = ('Stock Data for ' + symbol + ": " + start_date + ' to ' + end_date)
        newdate.reverse()
        bar_chart.x_labels = newdate
        opendata.reverse()
        bar_chart.add('Open', convert(opendata)) 
        highdata.reverse()
        bar_chart.add('High',  convert(highdata))
        lowdata.reverse()
        bar_chart.add('Low',   convert(lowdata))
        closeddata.reverse()
        bar_chart.add('Close', convert(closeddata)) 
        return bar_chart.render_data_uri()
        pass
    if (chart_type == '2'):
        line_chart = pygal.Line(x_label_rotation = 70)
        line_chart.title = ('Stock Data for ' + symbol + ": " + start_date + ' to ' + end_date)
        newdate.reverse()
        line_chart.x_labels = newdate
        opendata.reverse()
        line_chart.add('Open', convert(opendata)) 
        highdata.reverse()
        line_chart.add('High',  convert(highdata))
        lowdata.reverse()
        line_chart.add('Low',   convert(lowdata))
        closeddata.reverse()
        line_chart.add('Close', convert(closeddata))
        return line_chart.render_data_uri()
        pass



