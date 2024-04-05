import csv
import json
import base64
import uuid
import requests

import datetime

now = datetime.datetime.now()
CSV_FILE = "calls.csv"  # name of the CSV file to save the data to
WEBHOOK_URL = "https://webhook.site/7d1bf192-e010-4a09-ba05-c7818885e550"  # URL of the webhook to send data to
client_id = "TEST"


def sendtohook(file, url):
    # send the CSV data to the webhook
    response = requests.post(url, data=file)

    # check the response status code and content
    if response.status_code == 200:
        print("CSV data sent successfully!")
        print(response.content)
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["number", "timestamp", "name"])
    else:
        print("Error sending CSV data!")
        print(response.status_code)
        print(response.content)


def csvencode64(file):
    with open(file, 'rb') as csv_file:
        csv_bytes = csv_file.read()
        csv_base64 = base64.b64encode(csv_bytes).decode('utf-8')
    return csv_base64


def startdate(file):
    try:
        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            first_row = next(reader)  # Get the first row
            second_column = first_row[1]  # Get the second column of the first row
            return second_column
    except:
        return "No Records Found"


def enddate(file):
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        last_row = None
        for row in reader:
            last_row = row
    second_column = last_row[1]  # Get the second column of the last row
    if second_column == "timestamp":
        return "No Records Found"
    return second_column


def toJson(record_start, record_end, record_count, records):
    UUID = str(uuid.uuid4())
    data = {
        "record_start": record_start,
        "record_end": record_end,
        "record_format": "csv",
        "record_count": record_count,
        "records": records,
        "id": UUID,
        "id_client": client_id
    }

    json_data = json.dumps(data, indent=4)
    return json_data


def recordcount(file):
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        row_count = sum(1 for row in reader) - 1

    return row_count


try:
    sendtohook(toJson(startdate(CSV_FILE), enddate(CSV_FILE), recordcount(CSV_FILE), csvencode64(CSV_FILE)),
               WEBHOOK_URL)
except:
    print("An Error has occurred (check internet connection)")
print(now.strftime("%Y-%m-%d %H:%M:%S"))
