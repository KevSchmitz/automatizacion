import csv
from datetime import datetime
import win32print
from pathlib import Path

main_route = Path(__file__).resolve().parent
csv_route = main_route / 'data.csv'

logo = """^GFA,02304,02304,00024,:Z64:
eJytVTuO2zAQHTIklhBSSIjUGQjhStg+PY3YZQAaEO+RIukJVzqG4SrIKfYIaVLnKhkOSX1serEGdiDJ5uj58c2HY4BXjb3++saa5aKzZZAai27pXNFfXZ5nyoU013QFNICn65behOvWegBewDMUz0p4D0V+me5rU3jzyMhiNlmmz/gV27xgh/3R7vcH1wxQE1SQn4Pu1ek0QgWgl4qHn8f668G6TwJqSn2dJOhRncZRVVcR7g9HuxPfnBCwo0hTuCffX878FFRvl3hGMdCHmwJZm791TdEm+SvN5zUmCU6Fir+6xwn4dkhfUyOIzNknf2ocHtkaxDPpQqbSlpFfUZFGf7XVzhkLnXQDyNzIJGvLzzrk/nnuGwppYNYGJR10RxP9FI/KD9xouYEFa4JkaQaT8G0k0z7wA26jo1/FbDQm8DNbG7vAk24VQ+lnehS7I36wDH4sEqRznHqqLyXIMuz3NuK/RL+84g/KZv0tS/wSajPjtYaoX3NsPfKHFXOGJf0SNrFi9BwzfyiEmuLF/AR+nApGwEYu8xPw1WVLhfOZP+LbrmlMC23snTZJ9UTsFSyqgflB/CCwC1oMg6QMif8MzxyT0gOPqfmV+C1zEoOs4SnOh9wX1EHhwVOlE5kbhER2GzqtM+GCOHCg4j5UN7DjZoTvGsOgYw77IsxR9jfNwyp0ZtqBijHG+SmdSR02wO4Ft3AGcl2j9QHP82o+ri1jL/ABbkyt8LO1ApNVGG40gAp4HPzf82lfmV8d/snwuNsiPvCror+GTdEPD+LVHfxmmkVvYQf4eBevi36JGSoZv4MXeTi/Ef8E5T/f9+N/DP8wf1POT/X7XPR//vfnIbx0MT//Aca0YiU=:C22D"""

template1 = """
CT~~CD,~CC^~CT~
^XA~TA000~JSN^LT0^MNW^MTT^PON^PMN^LH0,0^JMA^PR2,2~SD30^JUS^LRN^CI0^XZ
^XA
^CI28
^MMT
^PW823
^LL0200
^LS0

^FO416,0{LOGO}

^FO5,0{LOGO}
{NOMBRE1}
{NOMBRE2}
{ROTULO1}
{ROTULO2}
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


def linea_rotulo(rotulo: str, x):
    y = 40
    return f"^FT{x},{y}^A0I,22,26^FH\^FDCod: {rotulo}^FS"


def linea_nombre(nombre: str, x):
    y = 140
    lines = 1

    if len(nombre) > 17:
        y = 130
        lines = 2

    return f"^FT{x},{y}^A0I,37,31^FB295,{lines},0,C^FH\^FD{nombre.upper()}^FS"

          



def generar_zpl(csv_path):
    
    etiquetas = []

    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        filas = list(reader)

        for i in range(0, len(filas), 2):
            fila1 = filas[i]
            fila2 = filas[i + 1] if i + 1 < len(filas) else {"NOMBRECLIENTE": "", "ROTULO": "", "CLIENTE": "", "APLICACION": ""}

            rotulo1 = linea_rotulo(fila1["ROTULO"].upper(), 800)
            rotulo2 = linea_rotulo(fila2["ROTULO"].upper(), 380)

            nombre1 = linea_nombre(fila1.get("NOMBRE","").upper(),770)
            nombre2 = linea_nombre(fila2.get("NOMBRE","").upper(),350)

            zpl = template1.format(
                NOMBRE1 = nombre1,                
                ROTULO1=rotulo1,
                NOMBRE2= nombre2,
                ROTULO2=rotulo2,
                LOGO = logo
            )
            etiquetas.append(zpl)

    return etiquetas






if __name__ == "__main__":
    etiquetas = generar_zpl(csv_route)
    imprimir_zpl(etiquetas, printer_name="ZDesigner GK420t")
    
