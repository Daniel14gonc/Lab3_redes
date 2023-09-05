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
    elif color == "yellow":
        print("\033[93m {}\033[00m" .format(text))
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
    elif color == "yellow":
        await aprint("\033[93m {}\033[00m" .format(text))
    else:
        await aprint(text)
        
        
def valid_input_string(text):
    input_data = input(text)
    while input_data == "":
        pretty_print("Input vacio, porfavor ingrese lo solicitado","red")
        input_data = input(text)
    return input_data

async def valid_input_string_async(text):
    input_data = await  ainput(text)
    while input_data == "":
        pretty_print_async("Input vacio, porfavor ingrese lo solicitado","red")
        input_data = await  ainput(text)
    return input_data


async def valid_input_int_async(text, rango):
    input_data = await ainput(text)
    valid = False
    while input_data == "" or not input_data.isnumeric() or not valid:
        if input_data.isnumeric():
            input_data_int = int(input_data)
            if input_data_int > 0 and input_data_int <= rango:
                valid  = True
                break
        await pretty_print_async("El input debe de ser un número entre las opciones y no puede ser vacío","red")
        input_data = await ainput(text)
    
    return input_data

def clean_nombre(nombre):
    return nombre.replace("@alumchat.xyz","").replace("archila161250","").split("/")[0]

def ask_data(diferent):
    data = {}
    
    nombre = valid_input_string("Ingresa el nombre del nodo> ")
    
    data["nombre"] = 'Archila161250'+nombre+'@alumchat.xyz'
    
    if diferent:
        vecinos = valid_input_string("Ingresa los vecinos separados por coma> ").split(",")
        cantidad = valid_input_string("Ingrese la cantidad total de nodos en la topología> ")
        data["cantidad"] = cantidad
    else:
        vecinos = valid_input_string("Ingresa los vecinos separados por coma> ").split(",")
        
    temp_vecinos = []
    for vecino in vecinos:
        texto = 'Archila161250'+vecino.strip()+"@alumchat.xyz"
        temp_vecinos.append(texto.lower())
    data["vecinos"] = temp_vecinos
    
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
    
    return (data,opcion)

async def flooding_menu():
    await pretty_print_async("\n", "green")
    await pretty_print_async("1. Enviar mensaje", "green")
    await pretty_print_async("2. Cerrar nodo", "green")
    op = await valid_input_int_async("> ",2)
    return op

async def link_state_menu():
    await pretty_print_async("\n", "green")
    await pretty_print_async("1. Iniciar flooding", "green")
    await pretty_print_async("2. Enviar mensaje", "green")
    await pretty_print_async("3. Cerrar nodo", "green")
    op = await valid_input_int_async("> ", 3)
    return op