import json

class Auto:
    def __init__(self, unique_id, model, origen, destino_or):
        self.unique_id = unique_id
        self.model = model
        self.origen = origen
        self.destino_or = destino_or
        self.next_state = None  # Añade el atributo next_state según tu lógica


def generar_json_autos(lista_autos):
    datos_autos = []

    for auto in lista_autos:
        datos_autos.append({
            "Id": auto.unique_id,
            "Origen": auto.origen,
            "Direccion": auto.destino_or,
            "Siguiente": auto.next_state
        })

    json_data = json.dumps(datos_autos, indent=4)
    return json_data

# Ejemplo de uso
lista_autos = [
    Auto(unique_id=1, model=None, origen="Origen1", destino_or="Destino1"),
    Auto(unique_id=2, model=None, origen="Origen2", destino_or="Destino2"),
    Auto(unique_id=3, model=None, origen="Origen2", destino_or="Destino2"),
    # Agregar más instancias de Auto si es necesario
]

json_autos = generar_json_autos(lista_autos)
print(json_autos)
