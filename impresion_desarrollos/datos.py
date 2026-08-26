import csv
from constants import BASE_DIR

def get_desarrollos():
    csv_path = BASE_DIR / 'data.csv'
    data = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        data = [row for row in reader]

    return data