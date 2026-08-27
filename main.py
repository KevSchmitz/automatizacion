from certificados_automatizados.lotes import get_lotes
from certificados_automatizados.productos import get_productos
from certificados_automatizados.excel import iniciar_excel, from_excel_to_pdf


def main():
    lotes = get_lotes()
    productos = get_productos(lotes)

    excel = iniciar_excel()

    for producto in productos:

        from_excel_to_pdf(producto, excel)


main()
