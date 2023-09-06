from Text_Manager import *
from Nodo import Node
from Nodo import *
from Flooding import Flooding
from LinkState import LinkState
from DistanceVector import DistanceVector
import asyncio

data, algoritmo = data_to_inicialize_node()
print(data)

node = None
bandera =0
while bandera < 1:
    
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    bandera =1
    
    if algoritmo == '1':
        exitoso = register(data['nombre'],data['nombre'])
        if exitoso:
            try:
                node = DistanceVector(data)
                node.connect(disable_starttls=True)
                node.process(forever=False)
            except Exception as e:
                pretty_print(e)
        else:
            pretty_print("Error al registrar el nodo","red")
    
    if algoritmo == '2':
        exitoso = register(data['nombre'],data['nombre'])
        if exitoso:
            try:
                node = LinkState(data)
                node.connect(disable_starttls=True)
                node.process(forever=False)
            except Exception as e:
                print(e)
        else:
            pretty_print("Error al registrar el nodo","red")
        
    
    if algoritmo == '3':
        exitoso = register(data['nombre'],data['nombre'])
        if exitoso:
            try:
                node = Flooding(data)
                node.connect(disable_starttls=True)
                node.process(forever=False)
            except Exception as e:
                print(e)
        else:
            pretty_print("Error al registrar el nodo","red")