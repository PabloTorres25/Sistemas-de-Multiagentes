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


# edificio = ((3,3),(12,6))



# def cubo(tupla: Tuple[Tuple[int,int]]) -> None:
#     print("Tupla: ")
#     rango = tupla[1][0] - tupla[0][0] + 1
#     print("Rango = ", rango)
#     for i in range(rango):
#         print(tupla[0][0] + i)



# cubo(edificio)

# lista_glorietas: Tuple[Tuple[Tuple[int, int], Tuple[int, int]]] = (
#     ((14,14),(15,15))
# )

#         ## Glorietas
# def dibujo_glorietas(tupla: Tuple[Tuple[Tuple[int, int], Tuple[int, int]]]):
#     print(tupla[1][0] - tupla[0][0])


# dibujo_glorietas(lista_glorietas)

for i in range(2):
    print(i)