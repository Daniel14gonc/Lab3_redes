import heapq

class LinkState(object):
    
    def __init__(self):
        self.pedir()

    def pedir(self):
        self.me = input("Ingresa el nombre del nodo> ")
        self.get_topology()
        self.dijkstra()
    
    def get_topology(self):
        print("La topologia se obtiene del archivo topology_LinkState.txt")
        try:
            with open("topology_LinkState.txt", "r") as archivo:
                self.topology = eval(archivo.read())
        except:
            print("La topología no se cargo correctamente")
        
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
    
    def receive_message(self, emisor, receptor, mensaje):
        if receptor == self.me:
            print("El destino del mensaje era el nodo actual")
            print(mensaje)
        else:
            print("Emisor: ", emisor)
            print("Enviar mensaje:", mensaje)
            print("El siguiente nodo al que se debe mandar es", self.get_next_node(receptor))


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
        mensaje = input("Ingrese el mensaje de la forma 'emisor,destino,mensaje'> ")
        mensaje = mensaje.split(",")
        mensaje = [x.strip() for x in mensaje]
        node.receive_message(mensaje[0], mensaje[1], mensaje[2])