import numpy as np

def generar_celdas_random(altura, anchura, porcentaje):
    total_celdas = int((porcentaje / 100) * altura * anchura)
    coordenadas_celdas = []

    for _ in range(total_celdas):
        while True:
            coordenada = (np.random.randint(0, altura), np.random.randint(0, anchura))
            if coordenada not in coordenadas_celdas:
                coordenadas_celdas.append(coordenada)
                break

    return coordenadas_celdas

# Ejemplo de uso:
altura_ejemplo = 5
anchura_ejemplo = 7
porcentaje_celdas_random = 20
celdas_aleatorias = generar_celdas_random(altura_ejemplo, anchura_ejemplo, porcentaje_celdas_random)

print("Celdas aleatorias:", celdas_aleatorias)
