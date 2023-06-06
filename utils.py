import csv
import requests

# create a csv to use as a database
def create_csv(csv_name, lst_header):
    with open(f'{csv_name}.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(lst_header)
    return "csv created"

# convert csv to dict, keys are the headers and values are the value of each cell
def csv_to_dict(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

# use api to get ratio between USD and Rials
def get_currency(api_url='http://api.navasan.tech/latest/?api_key=freeIuhhwfyERXx6Xu06WJ3zDeNKC5eJ'):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return int(data["usd"]["value"])
        else:
            return f'Request failed with status code: {response.status_code}'
    except requests.exceptions.RequestException as e:
        return f'Request error: {e}'