#http://dev.markitondemand.com/MODApis/#doc_quote


import requests
import json


def json_to_csv(json_record):
    csv_record = ""
    csv_record += json_record['Status']
    csv_record += "," + str(parsed_json['High'])
    csv_record += "," + parsed_json['Name']
    csv_record += "," + str(parsed_json['LastPrice'])
    csv_record += "," + parsed_json['Timestamp']
    csv_record += "," + parsed_json['Symbol']
    csv_record += "," + str(parsed_json['ChangePercent'])
    csv_record += "," + str(parsed_json['Volume'])
    csv_record += "," + str(parsed_json['ChangePercentYTD'])
    csv_record += "," + str(parsed_json['MSDate'])
    csv_record += "," + str(parsed_json['ChangeYTD'])
    csv_record += "," + str(parsed_json['MarketCap'])
    csv_record += "," + str(parsed_json['Open'])
    csv_record += "," + str(parsed_json['Change'])
    csv_record += "," + str(parsed_json['Low'])
    return csv_record


resp = requests.get('http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol=AAPL')

print(resp)
print(resp.json())

parsed_json = json.loads(resp.content)
print("Staus: " + parsed_json['Status'])
print("High: " + str(parsed_json['High']))
print("Name: " + parsed_json['Name'])
print("Last Price: " + str(parsed_json['LastPrice']))
print("Timestamp: " + parsed_json['Timestamp'])
print("Symbol: " + parsed_json['Symbol'])
print("Change Percent: " + str(parsed_json['ChangePercent']))
print("Volume: " + str(parsed_json['Volume']))
print("Change Percent Year to Date: " + str(parsed_json['ChangePercentYTD']))
print("MSDate: " + str(parsed_json['MSDate']))
print("Change Year to Date: " + str(parsed_json['ChangeYTD']))
print("Market Cap: " + str(parsed_json['MarketCap']))
print("Open: " + str(parsed_json['Open']))
print("Change: " + str(parsed_json['Change']))
print("Low: " + str(parsed_json['Low']))


fo = open("foo.txt", "w")
fo.write( "Python is a great language.\nYeah its great!!\n")

# Close opend file
fo.close()

#if resp.status_code != 200:
    # This means something went wrong.
    #raise ApiError('GET /tasks/ {}'.format(resp.status_code))
#for todo_item in resp.json():
 #s   print('{} {}'.format(todo_item['id'], todo_item['summary']))