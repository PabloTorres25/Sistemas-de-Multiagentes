from typing import Tuple

# def coordenadas(tupla: Tuple[Tuple[Tuple[int, int], Tuple[int, int]]]) -> None:
#     for edificio in tupla:
#         for celda in edificio:
#                 print(celda[0],",",celda[1])

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

# for i in range(2):
#     print(i)

# alto = 24

# lista_celdas_giro: Tuple[Tuple[int, int], str] = (
#     ((1,1),"Ab"), ((2,2),"Ab") 
# )

# def traduccion(val1, val2):
#     return val1 - 1, alto - val2 

# lista_traducida =tuple((traduccion(tupla[0][0], tupla[0][1]), tupla[1]) for tupla in lista_celdas_giro)

# print(lista_traducida[1])
# pos_list = [(1, 22), 'Ab']
# lista_giros_traducida = (((0, 23), 'Ab'), ((1, 22), 'Ab'))

# print(pos_list)
# print(lista_giros_traducida)
# print(tuple(pos_list) in lista_giros_traducida)

#1. Si es necesario convertirlo a tupla

# lista_celdas_giro: Tuple[Tuple[int, int], str] = (
#     ((1,1),"Ab"), ((2,2),"Ab") 
# )

# lista_giros_coor = tuple(traduccion(tupla[0][0], tupla[0][1]) for tupla in lista_celdas_giro)
# print(lista_giros_coor)

# pos_list = [1, 22]
# print(tuple(pos_list) in lista_giros_coor)

import random



A: Tuple[Tuple[int, int], Tuple[str, str]] = (
    ((1,16), ("Ab","De")), ((1,2), ("X", "Y"))
)

def girar_con_opciones(pos_list, lista_celdas):
    pos_list = tuple(pos_list)
    for coor, direccion in lista_celdas:
            if pos_list == coor:
                direccion = random.choice(direccion)
                print("Tome la elección = ", direccion)
                return direccion 
    return None 

print(girar_con_opciones([1,2], A))