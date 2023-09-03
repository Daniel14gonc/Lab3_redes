from aioconsole import ainput
from aioconsole import aprint


def pretty_print(text,color):
    
    if color == "red":
        print("\033[91m {}\033[00m" .format(text))
    elif color == "green":
        print("\033[92m {}\033[00m" .format(text))
    elif color == "aqua":
        print("\033[38;2;0;255;255m {}\033[00m" .format(text))
    elif color == "magenta":
        print("\033[95m {}\033[00m" .format(text))
    else:
        print(text)
        
async def pretty_print_async(text,color):
    
    if color == "red":
        await aprint("\033[91m {}\033[00m" .format(text))
    elif color == "green":
        await aprint("\033[92m {}\033[00m" .format(text))
    elif color == "aqua":
        await aprint("\033[38;2;0;255;255m {}\033[00m" .format(text))
    elif color == "magenta":
        await aprint("\033[95m {}\033[00m" .format(text))
    else:
        await aprint(text)
        
        
def valid_input_string(text,):
    input_data = input(text)
    while input_data == "":
        pretty_print("Input vacio, porfavor ingrese lo solicitado","red")
        input_data = input(text)
    return input_data

def ask_data(diferent):
    data = {}
    
    nombre = valid_input_string("Ingresa el nombre del nodo> ")
    
    data["nombre"] = nombre
    
    if diferent:
        vecinos = valid_input_string("Ingresa los vecinos separados por coma> ")
        cantidad = valid_input_string("Ingrese la cantidad total de nodos en la topología> ")
        data["cantidad"] = cantidad
    else:
        vecinos = valid_input_string("Ingresa los vecinos separados por coma> ").split(",")
    data["vecinos"] = vecinos.split(",")
    
    return data
            


def data_to_inicialize_node():
    valid = False
         
    while not valid:
        pretty_print("\n¿Que tipo de algoritmo desea utilizar?", "green")
        pretty_print("1. Distance Vector", "green")
        pretty_print("2. Link State", "green")
        pretty_print("3. Flooding", "green")

        opcion = input("Ingresa el numero de la opcion> ")
        
        if opcion in ["1","2","3"]:
            valid = True
        else:
            pretty_print("Opcion invalida","red")
            
    if opcion == "2":
        data = ask_data(True)
    else:
        data = ask_data(False)
    
    data["opcion"] = opcion
    return data