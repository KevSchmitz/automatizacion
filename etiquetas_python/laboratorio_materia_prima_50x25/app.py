import csv
import win32print

template = """CT~~CD,~CC^~CT~
^XA~TA000~JSN^LT0^MNW^MTT^PON^PMN^LH0,0^JMA^PR2,2~SD18^JUS^LRN^CI0^XZ
^XA
^MMT
^PW823
^LL0200
^LS0
^FO0,0^GFA,03072,03072,00024,:Z64:
eJztkDFLxDAYhtNE+gUpIYLQwIVr8Bd07CR3OLje4t7zF+RAxcEh9Jf0p/SmW1wcxLWT693geINWHL5y9w2Cg0Me+JaHBxJexiKRyB+R/NwY51jLOOsdYwG1wdew1ynszXXSoTzUvVIVV0rejvrXl53NLXzd1Q3ybBtax6ep42q+xc/er7WHIvUA8zfsl03pxKRxQvQN9iuhvTjbeFGsN9hfcOm4eXdC9s/Y5yfGg37wYGZP2E+lLHl1WXJTV9hbe25zXdjcLB6xz2SqpFEqU92ozzTAx7APdBp7Voow7NmyMYkfZjycn7lD9c2M8OG4Tna/64HIBdELopdEb4n+lPB3hHeEXxzXnMip70cikUjkH/IJlSsyCw==:3F44
^FO384,0^GFA,03584,03584,00028,:Z64:
eJztkbFqwzAQQGWp+EQxQoWCBRWx6Bd49FQSOnTN0t3tFyiQlg4dhL/En+JMWbp0KF09dU2Gjhkal07n5Aid9UCLHg+kO8YikUjkdJK/M8Y51jLOesdYQE3wNex0Cjtzl3QoC3WvVMWVko+j7uN9a3ML+3N7jxzbhNbxSeq4mm3wU55W2kOReoDZJ3YPTenEVeOE6BvsFkJ7cbH2olitsbvm0nHz5YTs37DLz4wH/ezBTF+xm0hZ8uqm5KausLP20ua6sLmZv2CXyVRJo1SmulGXaYDvYZ7QaexYKcKwh3Yk9gP1w/gPr4+5w9e/TAkXjqtk+78OiEwQnSA6SXSW6M4JtyScI9z8uOJERn0vEolEIpFT+QEWnDIL:B74B
^FO0,0^GFA,03328,03328,00104,:Z64:
eJxjYBheoP4/PcAPBge6+IZj1J5Re+hqD73yzygYBaNgFIyCUTAKRsFAAQCgNs4d:5D3C
^FO384,0^GFA,01792,01792,00008,:Z64:
eJxjYEAH////AdMNDCyj9Cg9So/So/QoDa8XhhcAAJePaf0=:48F0

^BY2,3,49^FT803,40^BCI,,Y,N
^FD{COD_ARO1}^FS
{NOMBRE1}
^BY2,3,49^FT378,37^BCI,,Y,N
^FD{COD_ARO2}^FS
{NOMBRE2}
^PQ1,0,1,Y^XZ
"""
# Genera la linea de codigo para el nombre de la etiqueta
def generar_linea_nombre(nombre: str, x: int, y: str = 140) -> str:
    linea_nombre = f"^FT{x},{y}^A0I,28,28^FB381,2,0,L^FH\^FD {nombre} ^FS"
    return linea_nombre

def generar_zpl(csv_path):
    etiquetas = []

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        filas = list(reader)

        for i in range(0, len(filas), 2):

            # Etiqueta 1
            fila1 = filas[i]
            nombre1 = fila1['NOMBRE'].upper().strip()
            linea_nombre1 = generar_linea_nombre(nombre1, x=803)
            codigo_aronova1 = fila1["COD_ARO"].upper().strip()

            # Etiqueta 2
            fila2 = filas[i + 1] if i + 1 < len(filas) else {"NOMBRE": "", "COD_ARO": ""}
            nombre2 = fila2['NOMBRE'].upper().strip()
            linea_nombre2 = generar_linea_nombre(nombre2, x=387)
            codigo_aronova2 = fila2["COD_ARO"].upper().strip()

            zpl = template.format(
                NOMBRE1= linea_nombre1,
                COD_ARO1= codigo_aronova1,
                NOMBRE2= linea_nombre2,
                COD_ARO2= codigo_aronova2
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
    etiquetas = generar_zpl("data.csv")
    imprimir_zpl(etiquetas, printer_name="ZDesigner GK420t (Copiar 2)")
