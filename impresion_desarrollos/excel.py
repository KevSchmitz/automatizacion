import win32com.client as win32

def open_excel():
    # 3. Iniciar excel en segundo plano para imprimir
    excel = win32.Dispatch("Excel.Application")
    excel.Visible = False # No mostrar la ventana de Excel
    return excel

def load_wb(excel, file_path):
    workbook = excel.Workbooks.open(file_path)
    return workbook

def print_wb(workbook):
    workbook.PrintOut()
    print("El archivo se imprimió correctamente")