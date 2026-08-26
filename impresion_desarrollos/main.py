from pathlib import Path
from datos import get_desarrollos
from template import fill_template
from excel import open_excel, load_wb, print_wb


def main():
    # 1. Obtener datos del archivo csv
    data = get_desarrollos()
    
    if not data:
        print("No hay desarrollos para imprimir")
        return

    # 2. Abrir Excel en segundo plano y enviar el archivo temporal a imprimir
    excel = open_excel()


    for desarrollo in data:
        try:    
        # 3. Inyectar datos en la plantilla de Excel y guardar el archivo temporal
            temp_file_path = fill_template([desarrollo])
            # 4. Imprimir el archivo temporal
            workbook = load_wb(excel, temp_file_path)
            print_wb(workbook)
            # 5. Cerrar Excel y eliminar el archivo temporal
            workbook.Close(SaveChanges=False)
            excel.Quit()
        
        finally:
            if Path(temp_file_path).exists():
                Path(temp_file_path).unlink()

main()