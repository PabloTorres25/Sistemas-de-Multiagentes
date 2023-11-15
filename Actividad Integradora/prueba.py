from typing import Tuple

def coordenadas(tupla: Tuple[Tuple[Tuple[int, int], Tuple[int, int]]]) -> None:
    for edificio in tupla:
        for celda in edificio:
                print(celda[0],",",celda[1])

# lista_edificios: Tuple[Tuple[Tuple[int,int], Tuple[int,int]]] = (
#     ((3,3),(12,6)), 
#     ((3,9),(5,12)) 
# )

# coordenadas(lista_edificios)


edificio = ((3,3),(12,6))



def cubo(tupla: Tuple[Tuple[int,int]]) -> None:
    print("Tupla: ")
    rango = tupla[1][0] - tupla[0][0] + 1
    print("Rango = ", rango)
    for i in range(rango):
        print(tupla[0][0] + i)



cubo(edificio)