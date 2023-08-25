import heapq

class LinkState(object):
    
    def __init__(self):
        self.pedir()

    def pedir(self):
        self.me = input("Ingresa el nombre del nodo> ")
        misvecinos = input("Ingresa los vecinos separados por coma> ")
        pesosvecinos = input("Ingresa los pesos de los vecinos separados por coma> ")

        misvecinos = misvecinos.split(",")
        misvecinos = [x.strip() for x in misvecinos]
        pesosvecinos = pesosvecinos.split(",")
        pesosvecinos = [int(x.strip()) for x in pesosvecinos]
        
        self.neighbors = list(zip(misvecinos, pesosvecinos))
        self.get_topology()
        self.dijkstra()
    
    def get_topology(self):
        self.topology = {
            "A": [("B", 2)], 
            "B": [("A", 2), ("C", 4), ("D", 5)],
            "C": [("B", 4), ("D", 1)],
            "D": [("B", 5), ("C", 1)]
        }
        
    def dijkstra(self):
        self.distances = {}
        self.previous = {}
        self.queue = []
        
        for node in self.topology:
            if node == self.me:
                self.distances[node] = 0
                heapq.heappush(self.queue, (0, node))
            else:
                self.distances[node] = float("inf")
                heapq.heappush(self.queue, (float("inf"), node))
            self.previous[node] = None
        
        while self.queue:
            u = heapq.heappop(self.queue)
            u = u[1]
            for v in self.topology[u]:
                alt = self.distances[u] + v[1]
                if alt < self.distances[v[0]]:
                    self.distances[v[0]] = alt
                    self.previous[v[0]] = u
                    for i in range(len(self.queue)):
                        if self.queue[i][1] == v[0]:
                            self.queue[i] = (alt, v[0])
                            heapq.heapify(self.queue)
    
        # Creación y almacenamiento de la tabla de enrutamiento
        self.routing_table = {}
        for node, previous_node in self.previous.items():
            if previous_node is not None:
                path = self.get_path(node)
                self.routing_table[node] = (path, self.distances[node])

    def get_path(self, destination):
        path = [destination]
        while self.previous[destination] is not None:
            destination = self.previous[destination]
            path.insert(0, destination)
        return path
    
    def get_next_node(self, destination):
        path = self.get_path(destination)
        if len(path) > 1:
            return path[1]
        return path[0]

    def print_routing_table(self):
        print("Tabla de enrutamiento para el nodo", self.me)
        for node, (path, distance) in self.routing_table.items():
            print("Destino:", node)
            print("Camino:", " -> ".join(path))
            print("Distancia:", distance)
            print("-" * 20)
    
    def print_distances(self):
        for node in self.distances:
            print("Distancia de {} a {} es {}".format(self.me, node, self.distances[node]))


node = LinkState()
opcion = -1
while opcion != "3":
    print("\n\n1. Enviar mensaje")
    print("2. Recibir mensaje")
    print("3. Salir")
    opcion = input("Ingrese opcion> ")
    if opcion == "1":
        mensaje = input("Ingrese el mensaje> ")
        destino = input("Ingrese el destino> ")
        siguiente = node.get_next_node(destino)
        print("El mensaje es", mensaje)
        print("El siguiente nodo al que se debe mandar es", siguiente)
    elif opcion == "2":
        mensaje = input("Ingrese el mensaje de la forma 'destino,mensaje'> ")
        mensaje = mensaje.split(",")
        if mensaje[0] == node.me:
            print("El destino del mensaje era el nodo actual")
            print("El mensaje es", mensaje[1])
        else:
            print("El mensaje es", mensaje[1])
            print("El siguiente nodo al que se debe mandar es", node.get_next_node(mensaje[0]))