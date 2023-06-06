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