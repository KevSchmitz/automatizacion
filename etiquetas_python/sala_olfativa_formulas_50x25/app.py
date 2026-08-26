import csv
from datetime import datetime
import win32print
from pathlib import Path

template = r'''
CT~~CD,~CC^~CT~
^XA~TA000~JSN^LT0^MNW^MTT^PON^PMN^LH0,0^JMA^PR2,2~SD18^JUS^LRN^CI0^XZ
^XA
^CI28
^MMT
^PW823
^LL0200
^LS0
^FO384,0^GFA,01792,01792,00008,:Z64:
eJxjYEAH////ANMNDByj9Cg9So/So/QoDadh9cPwAACSM22F:2939
^FO0,0^GFA,03072,03072,00024,:Z64:
eJztkD1OwzAUgJ/jUFc0cl0JCQ/hZ2RCQSxvQuEGPUJ7gzLBVldl6IA6MyJOwJgJuWKAIzAwWGLJmI0MSCUDNB7sAXX1Z0+fPj1bDyAQ2I5ucxT83j92QAiYEhCsEgOIN56qDKO1UrJfJ6hx4wlMkKxWWqZpIrRs+4XBnjKlRM6xLNr+S+cduKrkiDFxXbUPr80bh6yWhs6LqWn9pb6NYfAhc0KqbNT6z9kdB1zeN32NVj8mcdO/Nj2bCN3683mn6V8KQ5eIlt+nTX+2es9JKg6sRVzsRhwKVZe9BfYtn8aEwVjfZJ1EMGubnNP5o1F4ccrR9klKZuuZlkffrLJ9F8E8K9XtlbSOLA9DmICD6AlOXB6E0wI8uDXJPb3x+KFbc/W/+dQzn3jmHHr8nlsD93jP96HyeE8fHbs986zf951AIBAIBLbgB3JnUug=:37BB
^FO352,0^GFA,04096,04096,00032,:Z64:
eJztkz1OwzAYQD/Hoa5o5LoSEh7Cz8iEgli+CYUb9AjtDcoEW12VoQPqzIg4AWMm5IoBjsDAYIklYzYyIJUIwYKtWAhGv3jy0/PnKApAIBD4pNs8Cr7WTzZACJgSEKwSA4gtT1WG0Vop2a8T1Gh5AhMkq5WWaZoILe1+YbCnTCmRcywLu3/TeQfOKjliTJxX9gXX5olDVktD58XU2P5UX8YweJE5IVU2sv3r7IoDLq+bvkZHPyZx0z82PZsIbfvjeafpHwpDl4gOv02b/mj1nJNU7Cjbn2xGHApVl70F9h0+jQmDsb7IOolgtgbO6fzWKDw55OjySUpm65mWe++scvkugrlXqtsraR05PAxh4tr+JrqDgzYPotUC3LRrknt64/HDds3V3+ZTz3ziOX/X47faNXCP97w+OH6p3/TRfrtnns/vu34gEAgEAoHA//ABjqdS6A==:314B
{NOMBRE1}
^FT805,116^A0I,34,28^FH\^FDFor: {FORMULA1}^FS
^FT385,83^A0I,24,24^FH\^FDLote: -^FS
^FT804,54^A0I,24,24^FH\^FDPeso: {ANALISTA1}^FS
^FT385,23^A0I,24,24^FH\^FDFecha: {FECHA}^FS
^FT804,84^A0I,24,24^FH\^FDLote: -^FS
^FT385,53^A0I,24,24^FH\^FDPeso: {ANALISTA2}^FS
^FT804,24^A0I,24,24^FH\^FDFecha: {FECHA}^FS
{NOMBRE2}
^FT388,116^A0I,34,28^FH\^FDFor: {FORMULA2}^FS
^PQ1,0,1,Y^XZ
'''

script_path = Path(__file__).parent
data_path =  script_path/ 'data.csv'

printer_name = "ZDesigner GK420t (Copiar 2)"


def nombre_formula(nombre: str, x: int):
    y = 158
    font_width = 28
    if len(nombre) >= 28:
        font_width = 24

    return f"^FT{x},{y}^A0I,34,{font_width}^FH\^FD{nombre.strip().upper()}^FS"


def generar_zpl(csv_path):
    hoy = datetime.now().strftime("%d/%m/%Y")
    etiquetas = []

    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        filas = list(reader)

        for i in range(0, len(filas), 2):
            fila1 = filas[i]
            fila2 = filas[i + 1] if i + 1 < len(filas) else {"NOMBRE": "", "FORMULA": "", "ANALISTA": ""}


            zpl = template.format(
                NOMBRE1=nombre_formula(fila1['NOMBRE'],805),
                FORMULA1=fila1.get("FORMULA", "").upper(),
                ANALISTA1=fila1.get("ANALISTA", "").upper(),
                NOMBRE2=nombre_formula(fila2['NOMBRE'],390),
                FORMULA2=fila2.get("FORMULA", "").upper(),
                ANALISTA2=fila2.get("ANALISTA", "").upper(),
                FECHA=hoy,
            )
            etiquetas.append(zpl)

    return etiquetas

def imprimir_zpl(zpl_commands, printer_name=None):
    if not printer_name:
        printer_name = win32print.GetDefaultPrinter()

    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        for i, zpl in enumerate(zpl_commands, 1):
            job = win32print.StartDocPrinter(hPrinter, 1, ("Etiqueta", None, "RAW"))
            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, zpl.encode('utf-8'))
            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)
            print(f"Etiqueta {i} enviada a la impresora.")
    finally:
        win32print.ClosePrinter(hPrinter)


if __name__ == "__main__":
    etiquetas = generar_zpl(data_path)
    imprimir_zpl(etiquetas, printer_name)
