import win32print

def get_default_printer():
    return  win32print.GetDefaultPrinter()

def calcular_limites(valor):
    return {"li": valor * 0.995, "ls": valor * 1.005}


def esta_en_rango(valor, promedio):
    return promedio * 0.995 <= valor <= promedio * 1.005
