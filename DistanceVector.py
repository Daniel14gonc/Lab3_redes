class DistanceVector(object):

    def __init__(self):
        self.hop_table = {}
        self.pedir()
    
    def pedir(self):
        self.me = input("Ingresa el nombre del nodo> ")
        self.nodos = input("Ingresa todos los nodos de la red> ").split(",")
        self.vecinos = input("Ingresa los vecinos separados por coma> ").split(",")
        self.vecinos = sorted(self.vecinos)
        self.hop_table[self.me] = self.me
        for vecino in self.vecinos:
            self.hop_table[vecino] = vecino
        self.pesos = input("Ingresa los pesos de los vecinos separados por coma> ").split(",")
        self.tamaño = len(self.nodos)
        self.tabla = {}
        infinitos = []
        cont = 0
        tabla_array =[]
        for n in self.nodos:
            if n == self.me:
                tabla_array.append([n, 0])
            elif n in self.vecinos:
                tabla_array.append([n, int(self.pesos[cont])])
                cont += 1
            else:
                tabla_array.append([n, float("inf")])
            infinitos.append([n, float("inf")])
            
        self.tabla[self.me] = tabla_array
        for n in self.nodos:
            if n != self.me:
                self.tabla[n] = infinitos
        # self.tabla = eval("{'X': [['X', 0], ['Y', 2], ['Z', 7]], 'Y': [['X', 2], ['Y', 0], ['Z', 1]], 'Z': [['X', 7], ['Y', 1], ['Z', 0]]}")
            
        print(self.tabla)

    def receive_info_from_node(self):
        sender = input("Ingresa el nombre del nodo que envia> ")
        info = input("Ingresa la informacion que envia> ")
        self.tabla[sender] = eval(info)
        print(self.tabla[sender])
    
    def brute_force(self,key,Node):
        array = self.tabla[key]
        for n in array:
            if n[0] == Node:
                return n
            
    def set_new_cost(self,key,Node,cost):
        array = self.tabla[key]
        for n in array:
            if n[0] == Node:
                n[1] = cost
        
        
    def update_table(self):
        for n in self.nodos:
            if n != self.me:
                objetivo,costo = self.brute_force(self.me, n)
                for n1 in self.nodos:
                    if n1 != self.me and n1 != objetivo:
                        costo1 = self.brute_force(n1,objetivo)[1]
                        costo2 = self.brute_force(self.me,n1)[1]
                        if costo1 + costo < costo2:
                            self.set_new_cost(self.me,n1,costo1 + costo)
                            self.hop_table[n1] = objetivo
                
    
    def get_own_table(self):
        return self.tabla[self.me]
    
    def get_next_node(self, destination):
        return self.hop_table[destination]
        
    def receive_message(self, emisor, receptor, mensaje):
        if receptor == self.me:
            print(mensaje)
        else:
            print("Emisor: ", emisor)
            print("Enviar mensaje:", mensaje)
            print("Siguiente nodo:", self.get_next_node(receptor))
        
    def send_message(self):
        print("Enviar mensaje:", mensaje)
        print("Siguiente nodo:", self.get_next_node(receptor))
        
distanceVector = DistanceVector()
opcion = -1
while opcion != "6":
    print("1. Recibir informacion de un nodo")
    print("2. Obtener tabla de enrutamiento")
    print("3. Recibir mensaje")
    print("4. Enviar mensaje")
    print("5. Actualizar tabla")
    print("6. Salir")
    opcion = input("Ingresa una opcion> ")
    if opcion == "1":
        distanceVector.receive_info_from_node()
    elif opcion == "2":
        print(distanceVector.get_own_table())
    elif opcion == "3":
        emisor = input("Ingresa el nombre del nodo emisor> ")
        receptor = input("Ingresa el nombre del nodo receptor> ")
        mensaje = input("Ingresa el mensaje> ")
    elif opcion == "4":
        emisor = input("Ingresa el nombre del nodo emisor> ")
        receptor = input("Ingresa el nombre del nodo receptor> ")
        mensaje = input("Ingresa el mensaje> ")
        print("Enviar mensaje a: ", distanceVector.get_next_node(receptor))
    elif opcion == "5":
        distanceVector.update_table()
        print(distanceVector.tabla)
        