from constants import BASE_DIR,FECHA_HOY
from certificados_automatizados.main import certificados_automatizados

def main():
    certificados_automatizados(BASE_DIR, FECHA_HOY)

main()