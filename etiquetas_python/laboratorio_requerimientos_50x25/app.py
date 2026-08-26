import csv
from datetime import datetime
import win32print
from pathlib import Path

main_route = Path(__file__).resolve().parent
csv_route = main_route / 'data.csv'

printer_name = "ZDesigner GK420t (Copiar 2)"

clientes = []


template1 = r"""
CT~~CD,~CC^~CT~
^XA~TA000~JSN^LT0^MNW^MTT^PON^PMN^LH0,0^JMA^PR2,2~SD18^JUS^LRN^CI0^XZ
^XA
^CI28
^MMT
^PW823
^LL0200
^LS0
^FO0,0^GFA,03072,03072,00024,:Z64:
eJztkK9OAzEYwL9ej3Vhl65LSKg4/kgUOYL5FDneYI+wvcFQ4NZliAkyjSQ8AfIU6YKAR0AgmmBOnuMEyTgBu4pWoBD016pffvnafACB/0u3OQq+7w9bIARMCQhWiQHEG09VhtFaKdmvE9S48QQmSFYrLdM0EVq2/cJgT5lSIudYFm3/ofMOXFRyxJi4rNqH1+aFQ1ZLQ+fF1LT+XF/HMHiTOSFVNmr9++yGAy5vm75Gqx+TuOmfm55NhG796bzT9E+FoUtEy+/Spj9ZveYkFXvWIs62Iw6FqsveAvuWT2PCYKyvsk4imLVNzun83ig8O+Zo+yQls/VMy4NPVtm+i2Aeler2SlpHlochTMBB9ABHLg/CaQHu3Jrknt54/NCtufrdfOqZTzxz9j1+x62Be7zn+1B5vKePDt2eedbv+04gEAgEAn/OFx7qUug=:E93B
^FO384,0^GFA,04096,04096,00032,:Z64:
eJzt0LFKw0Acx/H/5VIvSEnrIO2Q0oyOHQMOvQ7i6gMUjG9whY6C/1KoTvUFHHwMJ/3HluY17gEcFDo4FGpEcLkjNzgJ9yVTPvy4SwB8vn+RBBkC/DxGJ4DIPyPAIeIdpIYnbEadXQh0Q1cbRoZHfEZxHANpnS/A9OSc0VgIWZCalGemt54DGPB7XEGWzV/QcLE/kIrdUglJb7U37x/EYZrCUr9C1JrNTRdJM1dsPa32/aI0nUfR9z6r9qe4MJ09dAeKbXrVflJsTIenbpqyZVztNb5Z9u8XbdVYi1KOR3Rt2es0ynjMCxzkmFlcqaTXCVnxoSZk81w3W7vq/+/10LofkWhsQ5CXsk9tiwfI0fL6t2Nkss6hdg3QqGc4dLhweOA4f/rH8/sObzp86/BHh6t6dn2+cLhrf1TPkDn2juv7fD6fz+fz/Zu+AKYhV3s=:E5D9
{NOMBRE2}
{ROTULO2}
{CLIENTE2}
^FT386,31^A0I,23,21^FH\^FDFecha: {FECHA}^FS
{NOMBRE1}
{ROTULO1}
{CLIENTE1}
^FT806,31^A0I,23,21^FH\^FDFecha: {FECHA}^FS
^PQ1,0,1,Y^XZ
"""

template2 = r"""
CT~~CD,~CC^~CT~
^XA~TA000~JSN^LT0^MNW^MTT^PON^PMN^LH0,0^JMA^PR2,2~SD18^JUS^LRN^CI0^XZ
^XA
^CI28
^MMT
^PW799
^LL0200
^LS0
{CLIENTE1}
{CLIENTE2}
^PQ1,0,1,Y^XZ

"""




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


def linea_rotulo(rotulo: str, x, y, aplicacion: str):
    if aplicacion != "":
        return f'^FT{x},{y}^A0I,23,21^FH\\^FDAplicacion: {aplicacion.upper()}^FS'
    else:
        return f'^FT{x},{y}^A0I,23,21^FH\\^FD Rot: {rotulo.upper()}^FS' if rotulo else f'^FT{x},{y}^A0I,23,21^FH\\^FD {"":<10} ^FS'


def linea_nombre(nombre: str, x):
    y = 140
    lines = 1

    if len(nombre) > 28:
        y = 130
        lines = 2

    return f"^FT{x},{y}^A0I,37,25^FB344,{lines},0,C^FH\^FD{nombre.upper()}^FS"

def linea_cliente(cliente:str, x:int):
    return f"^FT{x},59^A0I,23,21^FH\^FDCliente: {cliente.upper()}^FS" if cliente else ""
            

def etiqueta_cliente(cliente:str, x:int):

    lineas = 1
    y = 75
    font = {
        "size": 75,
        "weight": 55
    }

    if len(cliente) >= 12:
        lineas = 2

    if len(cliente) > 20:
        font["size"] = 55
        font["weight"] = 35

    if lineas > 1:
        y = 40

    str = f"^FWI ^FO{x},{y} ^A0N,{font['size']},{font['weight']} ^FB380,{lineas},0,C ^FD{cliente.upper()}^FS"
    
    return str



def generar_zpl(csv_path):
    hoy = datetime.now().strftime("%d/%m/%Y")
    etiquetas = []

    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        filas = list(reader)

        for i in range(0, len(filas), 2):
            fila1 = filas[i]
            fila2 = filas[i + 1] if i + 1 < len(filas) else {"NOMBRECLIENTE": "", "ROTULO": "", "CLIENTE": "", "APLICACION": ""}

            rotulo1 = linea_rotulo(fila1["ROTULO"].upper(), 806, 87, fila1["APLICACION"])
            rotulo2 = linea_rotulo(fila2["ROTULO"].upper(), 386, 87, fila2["APLICACION"])

            nombre1 = linea_nombre(fila1.get("NOMBRE","").upper(),792)
            nombre2 = linea_nombre(fila2.get("NOMBRE","").upper(),385)

            if fila1['CLIENTE'] and fila1['CLIENTE'].upper() not in clientes:
                clientes.append(fila1['CLIENTE'].upper())
            
            if fila2['CLIENTE'] and fila2['CLIENTE'].upper() not in clientes:
                clientes.append(fila2['CLIENTE'].upper())

            cliente1 = linea_cliente(fila1["CLIENTE"],806)
            cliente2 = linea_cliente(fila2["CLIENTE"],386)

            zpl = template1.format(
                NOMBRE1 = nombre1,
                CLIENTE1 = cliente1,
                ROTULO1=rotulo1,
                NOMBRE2= nombre2,
                CLIENTE2 = cliente2,
                ROTULO2=rotulo2,
                FECHA=hoy,
            )
            etiquetas.append(zpl)

    return etiquetas



def generar_zpl_clientes(clientes):
    etiquetas = []

    for i in range(0,len(clientes),2):
        cliente1 = clientes[i]
        cliente2 = clientes[i+1] if i+1 < len(clientes) else ''

        linea_cliente1 = etiqueta_cliente(cliente1, 420)
        linea_cliente2 = etiqueta_cliente(cliente2, 10)

        zpl = template2.format(
            CLIENTE1= linea_cliente1,
            CLIENTE2= linea_cliente2
        )

        etiquetas.append(zpl)
        

    return etiquetas


if __name__ == "__main__":
    etiquetas = generar_zpl(csv_route)
    imprimir_zpl(etiquetas, printer_name)
    etiquetas = generar_zpl_clientes(clientes)
    imprimir_zpl(etiquetas, printer_name)
