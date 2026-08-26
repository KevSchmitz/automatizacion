import csv
from datetime import datetime
import win32print
from pathlib import Path

base_path = Path(__file__).resolve().parent
csv_path = base_path / "data.csv"
logo = r"""A,03584,03584,00028,:Z64:
eJztkjFLw0AYht9LrBexNHWyQ0pudBLHgAW7+Qe6G3BwvU46FPkkoB3E3yO4XMjQTfwBDilZHBy6WbA0pltOuBsKLpJnueHhyUfuO6DhX8OA7ubs/hYOPAfOsjqwdGiKo5rjFHD4JUfAy1b6CllzLvVcdHyXPD+h7B6iPkxV3YBnKuizdP6gdfh43qOIJXk7Ql4k07zelYu+kixbBBMsxrNS1bvvvEcximfvBOI0eaG6k/KgcpdBICHDu1TrRC4oR/HUjiHOKNO6sZIqx9XDpivVTHORijddMhUQBRXapfXVcChZwd4lxilda26fKI6R0WeEeULHmgtTJSWbqcmEzVN1qzmfkYjchKIeo4QGmuMM3fDQRRAepl8UaG63Wp2/dqnN1yjJ051frW7Fqd1a4ULpXbV5ByZGcI3u0Wiws2N2Vm4sLrK4kVk5wuzYm+WbS0u3sHSWedySdSzufLtxW1/nxKwcz+xsv2d+Y0DL4hoaGhoaGhr+mh9Hnm7Z:A74E"""

template = r"""CT~~CD,~CC^~CT~
^XA~TA000~JSN^LT0^MNW^MTT^PON^PMN^LH0,0^JMA^PR2,2~SD18^JUS^LRN^CI0^XZ
^XA
^MMT
^PW823
^LL0200
^LS0
^FO0,0^GF{LOGO}
^FO410,0^GF{LOGO}
{NOMBRE1}
^FT809,125^A0I,32,26^FB381,1,0,C^FH\^FDD{DESARROLLO1}^FS
^FT809,85^A0I,32,26^FB381,1,0,C^FH\^FD{CATEGORIA1}^FS
^FT809,20^A0I,20,21^FH\^FDCliente: {CLIENTE1}^FS
^FT388,20^A0I,20,21^FH\^FDCliente: {CLIENTE2}^FS
{NOMBRE2}
^FT388,125^A0I,32,26^FB381,1,0,C^FH\^FDD{DESARROLLO2}^FS
^FT388,85^A0I,32,26^FB381,1,0,C^FH\^FD{CATEGORIA2}^FS
^PQ1,0,1,Y^XZ
"""

def nombre_cliente(cliente: str, x: int):
    name_length = len(cliente)
    width = 20
    height = 20

    if name_length > 14:
        width = 16

    return f"FT{x},20^A0I,{height},{width}^FH\^FDCliente: {cliente.upper()}^FS"

def nombre_producto(producto: str, x: int):
    name_length = len(producto)
    width = 26
    height = 32
    lines = 1

    if name_length > 26:
        width = 20

    return f"^FT{x},165^A0I,{height},{width}^FB381,{lines},0,C^FH\^FD{producto.upper()}^FS"

def generar_zpl(csv_path):
    
    etiquetas = []

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        filas = list(reader)

        for i in range(0, len(filas), 2):


            fila1 = filas[i]
            fila2 = filas[i + 1] if i + 1 < len(filas) else {"NOMBREPRODUCTO": "", "DESARROLLO": "","CATEGORIA": "", "CLIENTE": ""}

            producto1 = nombre_producto(fila1["NOMBREPRODUCTO"], 809)
            producto2 = nombre_producto(fila2["NOMBREPRODUCTO"], 388)

            nombre_cliente1 = nombre_cliente(fila1["CLIENTE"], 809)
            nombre_cliente2 = nombre_cliente(fila2["CLIENTE"], 388)

            zpl = template.format(
                NOMBRE1= producto1,
                DESARROLLO1=fila1.get("DESARROLLO", "").upper().zfill(4),
                CATEGORIA1=fila1.get("CATEGORIA", "").upper(),
                CLIENTE1= nombre_cliente1.upper(),
                NOMBRE2= producto2,
                DESARROLLO2=fila2.get("DESARROLLO", "").upper().zfill(4),
                CATEGORIA2=fila2.get("CATEGORIA", "").upper(),
                CLIENTE2= nombre_cliente2.upper(),
                LOGO = logo
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
    etiquetas = generar_zpl(csv_path)
    # for etiqueta in etiquetas:
        # print(etiqueta)
    imprimir_zpl(etiquetas, printer_name="ZDesigner GK420t (Copiar 2)")
