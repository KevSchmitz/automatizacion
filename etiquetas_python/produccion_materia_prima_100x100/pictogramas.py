from pathlib import Path
import csv

csv_file = Path(__file__).parent / "mp_pictogramas.csv"

raw_materials = []

with open(csv_file, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, delimiter=";")

    for rm in reader:
        raw_materials.append(rm)
