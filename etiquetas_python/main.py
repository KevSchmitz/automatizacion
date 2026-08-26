from pathlib import Path

main_path = Path(__file__).resolve().parent
entrada = None
paths = {
  "desarrollos" : {"route":"laboratorio_desarrollos_50x25", "fn": "desarrollos_fn" },
  "mp_lab": {"route":"laboratorio_materia_prima_50x25", "fn":"mp_lab_fn"},
  "requerimientos": {"route":"laboratorio_requerimientos_50x25", "fn":"requerimientos_fn"},
}
options_length = len(paths)

def show_list(list):
  for i, item in enumerate(list):
    string = f"{i+1}. {item}"
    print(string)

  print('\n')


while entrada != 0:
  print('Escoja la etiqueta que desee utilizar. \n')
  show_list(paths)
  print('Para poder salir presione 0 \n')
  entrada = int(input('Ingrese una opcion: '))

  if entrada > options_length:
    print("Por favor ingrese un numero que este en la lista \n")

  for key, values in paths.items():
    print(values['route'])


  

