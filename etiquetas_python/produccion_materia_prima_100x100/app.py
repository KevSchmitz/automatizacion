import csv
from datetime import datetime
import win32print
from pathlib import Path
from pictogramas import raw_materials

base_path = Path(__file__).resolve().parent
csv_path = base_path / 'data.csv'

check_calidad = r"^FT64,472^A0R,96,74^FH\^FDCC = OK ^FS"

pics_por_codigo = {m["COD ARONOVA"]: m['Pictogramas'] for m in raw_materials}

logo_aronova = r'''^FO0,320^GFA,17280,17280,00036,:Z64:
eJztmr9uFDEQxm1tDnc5KNA1ERta2hSUu0hBtNAjlkcgElKaCC88BSVPwCvcRqKkSIFEhdgSUYRDSnFFcsb2keSQ8HyfxCm6I/6iKM1Pk1n/Gc/Yo1RWVlZWVlZWVlZWVlZWVlZWVtZVS9cE0xLMhGCmBHNWY8Z1BIMd0m6GHWocdmjoesgYd4L/GeOQJb6+Ihyy7pSw47CdBjtUGQfn3mp3Bu14j1pkR43cEbRTQIesGsApq4ipb4glVBEzbw1e0lWF58JavMUqYm1YYofh2fKbELuDJ0upEk56cJlwB3+5JtzhYhRElMbuKN0TTI2ZtVQdJTPfg3oR0S5IXtFzZr3sqN1du/sI7tRXygA7YbUaZKeYYTtmhu0MCTuW8McfX0NgR7uvatjJTOHGLWJGZ2VXAqaalj0KQfakdCh2uH7ogB0ffww6vP2MFujc8fFHo2Mw5HVVDxg/VQMZ4eJYh5krVk0wmy1EcLYREk2cIFqHM1YHl1gMLnC7ewYdhcbtNugMG56GHS+rnODzMixCxNhu/isyrbfVAib4BOyEbwLxJ57vILbMGcIOiIfFFDO0nQLYmaygHcBQdojx0UsaZ3re0dk0IxhmPVP7osP7K+5TYIfZ7z5owLjBxB8mjjHxUOF0jIvPTJxnzgt1DyPU+bV20reCbspMzJ/lxTFn5JHm8/mOYFqCqUVGHR8f/yBukgxRWw6JO7uSuPtD+WEQChtBuIKnyuriCoenWa3hGaza8OB7G2V7iGhiePSShof59BHBlG48Hr+TmQbfA4QjBcYfu5z7hAFxL2GYe4mb8ed/1AbBvG8hwpzvJZEnNFw92APkOteDIWxUgFnDenBZdcpV1l+DVasr6XHu/93ONa8H4dHM1YMPV6seZOIzVw9OlEGQrwdNC00p02FmSNgpMaIqgnlKMMxDGcEURMoK3x0U3KdRVEaPkcFyMnFt8WcVOIPeaOAzvl/P0J3bFj7o+m0Kt4XPRT9hZtZi5jFCvD8Q4eacqQaZ+oIp45iH6uU5xKxmyqFvmFmWQ9wIEWFjhDcGs8GoUhc5FPsBvEPSm1x8j/MObUpMGGTtjp5JTFyGbvpKYuIg7/88EKqneU/Xzs+p4NC8f+Pp3smW8M/iJduWPr0jMLGfZEs7yU7sS9nUbtxLDp3VyujP4i1QaEwpXk/EbRb6bbQ+slIcqrxD+vVbaaBD/4/Sh5+sxFSln46uFdeiHXmHav3l8KVgJ7TYPden0uljQ39UrT+WQriPfVbb+kMpOBT7tWotPsLHvq9t1UoDHfvHav/3RXopxj60bf93Ox1hYz+bt3PfpGNM9buzaUdIW5vQX+ftPCk/pO2cXxuXfdqf85tu4br2om9QiB4X/Yf7B0nm4lzeeZtCLvsh95ITf9lcd/dNirlsrnvwqE4wC2lCKrNd7BdNpXeLB4FJDNBi/2rqmnAxDU0yCz6YxEXQYl/ujT7BXLqjNl78nflDzwkmKysra630C0HNr34=:1A14
^FO512,544^GFA,01536,01536,00012,:Z64:
eJztUzFOxTAMdcIfIqYeIWLiGOVI3MB0+uISRExVeoNOFSf4N0DcIIiFoSIkbZxYyJ1hwFPy8uJnOy8A//FXQ7G1RpljrIxbI+OoRTihokDKIgrY7UhILwts6QUBk1ES4OcZNwc4CSwM3rLjT1xnvsXGvyuy6QIOA/FRvewrm/DhcST+cvV6KarOT/O54G8xXqirZ+8dCb/HuJT0ME6T26bUAYT7p1DSg3dDurB3tvbqAeC0XZ9TQdTZJ0BP/BHQ3RZ+IDxt3RmdLpMLXVbZ6xlv0FA9K5vafN2muFZfWfCZWwb9VRkGPDZ+rCudcCvggDNCnf9HKSeHd66+V2j8XH9934Xj2smGk/1z5Lf8ktWfHbSCuJ9PjM/9r/jH4+l7LsDs37V+D/8j/79KpvxKfANnSlm+:A11B'''

# --- TEMPLATE ZPL ---
template = r"""
CT~~CD,~CC^~CT~
^XA~TA000~JSN^LT0^MNW^MTT^PON^PMN^LH0,0^JMA^PR2,2~SD18^JUS^LRN^CI0^XZ
^XA
^MMT
^PW799
^LL0799
^LS0
{LOGO}
{MATERIA_PRIMA}
^FT696,56^A0R,62,62^FH\^FD{COD_ARO}^FS
{PICTOGRAMAS}
^BY2,3,78^FT681,529^BCR,,Y,N
^FD{COD_ARO}^FS
^FT413,58^A0R,41,43^FH\^FDProveedor: {PROVEEDOR}^FS
^FT311,58^A0R,41,43^FH\^FDLote: {MM}^FS
^FT209,58^A0R,41,43^FH\^FDFecha: {FECHA_INGRESO}^FS
^FT107,58^A0R,41,43^FH\^FDPeso: {PESO} Kg^FS
^PQ1,0,1,Y^XZ
"""

# --- CAMBIÁ ESTE NOMBRE SI TU IMPRESORA TIENE OTRO NOMBRE EN WINDOWS ---
printer_name = "ZDesigner GK420t (Copiar 2)"

# --- FUNCION PARA IMPRIMIR ---
def imprimir_zpl(zpl_code):
    printer_handle = win32print.OpenPrinter(printer_name)
    win32print.StartDocPrinter(printer_handle, 1, ("Etiqueta", None, "RAW"))
    win32print.StartPagePrinter(printer_handle)
    win32print.WritePrinter(printer_handle, zpl_code.encode("utf-8"))
    win32print.EndPagePrinter(printer_handle)
    win32print.EndDocPrinter(printer_handle)
    win32print.ClosePrinter(printer_handle)

def tamano_fuente(string: str):
    cantidad_palabras = len(string)

    font_width = 70
    
    if cantidad_palabras > 20:
        font_width = 50


    return fr"^FT530,50^A0R,70,{font_width}^FB480,2,0,L,0^FH\^FD{string.upper()}^FS"

def agregar_pictogramas(pictogramas_str: str):
    pictogramas_generados = []

    eje = {
        "x": 520,
        "y": 600
    }

    pictograma_dibujo = {
        "cutaneo": r"""^GFA,00768,00768,00012,:Z64:eJxjYBgFNAAcqx/A2fL/P4Ao7gUMDFr///8AC31gYP0PZe//wbAfxq7/wwxk/v8DYv//xw9i/0NikyDOjiTODRev/8MIF7f/wbAeZq880LXxUDZXA9D5+yFsMGCEuB8CtBZQLYwGBQAAch5hFA==:E428""",
        "respiratorio": r"""^GFA,01152,01152,00012,:Z64:eJztkjFOw0AQRWcJFkgUrlCqaK9BgWSnyA1ipWGVY1DaN6Cly1FYCaUmFFGarGQpRdIlFkiJBPgzu4nXW9JAxRTW02j8/eePif7rr+o6bTkpW853LePgUZil507Qv8Cn5zjgXjCfBH0ZcNAXxhgv/4KqaOQXWHj5LZ6bfm9qppqioZNZ4UHTk9PKq1zqCHDud7UsY6Cw8q9KaWWMdu5v5QZAad1X2ZgRO+u+ZndcB+f+nKeNXcK6zG2fP5DzY3xifGyos2WuibJZnwYDZY5La7pkNe6LLOOUxQh7+259Q3R1nFdmKTJ11OdEzhr9Lr76DXOaRXLyE5nlUM15fub8P8Zl7vwLVHdSdwFt9y0hdcftSzzc05FymSZvmBQUu5vJPUYpidTluca6yTOamnna5r/ydxmh8veaBHdXP7hvyFEwH/4zAu8Bh//bzDPZVZu6T+nX6huVKuXZ:11A8""",
        "inflamable": r"""^GFA,01152,01152,00012,:Z64:eJztkTFOw0AQRddxJFtYitPQWTIlEkXarQiH4DAuVsoKCiLlEpQoJ3CXSJyAG1CipKGMAtnP7MzYzgWQKNjq6e/On9k/xvzSuThjN2BxGLj+7HGE954zbJWWZgbfeyzgk4rZGuABB9WBJ4hTmwAbfIhODK1uUsKgPtnAbXkkXnvP+lssOEW25SO6aldmzNx3Uuw2wJF9qswvIEM0+WRERs+sT8dU8C3+eV6im3NqerZXkUOXTUU+/OXWmLwAvtYvkhl/gUqaeHkD7uwkIq5oI0cnr3otHWzkOThT1rUB6fmqm59fS3ANz7PT+aO7bKC1eQrdjKvGiT439nbi1ca4OtuS/Z3kuTr2+ZSvOj35l3tgL0YuO5HNvfin3QvSz9imCP2+EoSFMu09zHWnjj5Y65zXZhZGQfQYjhnOxg98uTX/54+dH9Tk2G0=:1552""",
        "ambiental": r"""^GFA,02048,02048,00016,:Z64:eJzt0j1OwzAYgOHP/VE6oJKhiA5VbXECRsTQeGj3MrBVKkfowIiUIDEwcgN6A66QqkKsvQEWXCAVrYhQWmOn9S87C1jK8OiNLccxwP/43RGKh3omfkfmjXbZU+1WOd+8sesMJXt3yj4J3Pm5dtlRYTkBgvKmNkpFzzowUT0FUmVnwIxpkF3XU2UG5JBlTb3eBOjxbH2jnYk+57nplOJXvtl/QBe299OIc75fD0MswDdHVFmSM7U/jMqsDwjfSqvVhV+4WUx6Lp0Yz6QXxix252fSBbrUXW6OP6kl8CruD3jM16pve0D441bPLzpA4+ex9pfoEQvUDvByBBSnSO0QszaQgKnjFT2U56+OX/QH8X9Y+R9Lp8Oy17Sp/P9QsSw7Uk6I/P/m+2hL3I+RcXIgetN4URc9MM5BrFDVB4gLoBTMBcVbIMS6wphDi+6useo1HXe9Tl2jqWe3J3DlOAW/g9dDzw3PNcfMc/bDFceF1wu3f67gwnL08VY7d/qsP7D9ntyd2F4CtfcfMTh1vmcCLdtdAhXn+0JAQ8s98dh9DO5owP/4u+MbwVO5cQ==:142E""",
        "corrosion": r"""^GFA,02048,02048,00016,:Z64:eJztkzFLw0AUx1+81jiE1EWokNJ+hI4BByMEunbI0aVgoV8gQqWOcXNydvSbeKVDtjq5KZy6t3EQupR4SZuXvAzWVcgL3N0vf967y/9dAKr476HxPn0RR1Qv8T59H/8l36Rc9yjfB4S/3/qEn9e0nlujDKag3N5cvqALig+C9updIIce1HqznOfLO2BSIn+pXBb5yNLsKH1UOP8QtKKejLJLvl+LMmapDpFNdPCtkm79rt9kHtY3KU8MIGGblC2dcvOwpLuU2Zqy5lCGDkXlAQmjXL+0v82y1bZ7Q9QbQapjfksko49NXstkzL9/+JpMk8yfxsMimaLmjqenoTq9hjy2w0dgt+j/tBX6dS/v39hejJaF/k6Pe1f8Ou//B5ij8yC/Hy5w4YIuxI4lrNSygezo+sw7GeD9kqY+j5/izyDTjdqFx13uYD5kpdPwQRPFX7gLDDpnAbKlDOQ81w31HAko6MoZrL7V6RaJsw5UUUU5fgAEqI4K:D463"""
    }

    pictogramas = pictogramas_str.split(",") 
    
    pictogramas = [p.strip() for p in pictogramas]

    if pictogramas:
        print("Agregando pictogramas:")
        for i, pictograma in enumerate(pictogramas):
            if not pictograma == '':
                eje["y"] = 600 if i % 2 == 0 else 675
                eje_pictograma = fr"^FO{eje['x']},{eje['y']}"
                print(eje_pictograma + "\n" + pictograma_dibujo[pictograma])
                pictogramas_generados.append(eje_pictograma + "\n" + pictograma_dibujo[pictograma])
                eje["x"]-=80
            
    return "\n".join(pictogramas_generados)


# --- LEER CSV Y ENVIAR A IMPRIMIR ---
with open(csv_path, newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=";")
    for i, row in enumerate(reader):
 
        row["LOGO"] = check_calidad

        row["MATERIA_PRIMA"] = tamano_fuente(row["MATERIA_PRIMA"])

        # Formateo de fecha y peso
        fecha_obj = datetime.strptime(row["FECHA_INGRESO"], "%d/%m/%Y")
        row["FECHA_INGRESO"] = fecha_obj.strftime("%b %Y").upper()

        row["PESO"] = f"{float(row['PESO'].replace(',', '.')):.2f}"
        row["CAPACIDAD_BIDON"] = float(row["CAPACIDAD_BIDON"].replace(',', '.'))

        codigo = row["COD_ARO"]

        pictogramas = []

        # Verificar si hay pictogramas en la info de la MP
        if codigo in pics_por_codigo:
            pictogramas = pics_por_codigo[codigo]

        row["PICTOGRAMAS"] = agregar_pictogramas(pictogramas)

        # Generar ZPL
        zpl = template.format(**row)

        # print(zpl)

        # Determinar cantidad de copias
        copias = 2 if (
            row["CAPACIDAD_BIDON"] > 30 
            or row["ESTADO"]
            ) else 1

        # Enviar a imprimir
        for _ in range(copias):
            imprimir_zpl(zpl)

        print(f"✅ Etiqueta {i+1} enviada a la Zebra")