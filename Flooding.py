
class Flooding(object):
    
    def __init__(self):
        self.pedir()

    def pedir(self):
        self.me = input("Ingresa el nombre del nodo> ")
        self.misvecinos = input("Ingresa los vecinos separados por coma> ")
        
    def flooding(self):
        opcion = "0"
        while opcion != "3":
            print("\n\n1. Enviar mensaje")
            print("2. Recibir mensaje")
            print("3. Salir")
            opcion = input("Ingrese opcion> ")
            if opcion == "1":
                mensaje = input("Ingrese el mensaje> ")
                destino = input("Ingrese el destino> ")
                vecinos = "".join(self.misvecinos.split(","))
                print("Enviando mensaje a mis vecinos: ", vecinos)
                print("Destinatario del mensaje: ", destino)
                print("Tabla de visitados: [{self.me}]")
            elif opcion == "2":
                recibido = input("Ingrese el mensaje de la forma 'destino,mensaje'> ")
                tupla = recibido.split(",")
                destino = tupla[0]
                mensaje = tupla[1]
                    
                tabla_visitados = input("Ingrese la tabla de visitados de la forma 'nodo1,nodo2,nodo3'> ")
                if destino == self.me:
                    print("Mensaje recibido: ", mensaje)
                elif self.me in tabla_visitados:
                    print("Mensaje ya visitado")
                else:
                    print("Enviando mensaje a mis vecinos: ", vecinos)
                    print("Destinatario del mensaje: ", destino)
                    print("Tabla de visitados: ", tabla_visitados+",{self.me}")

flooding = Flooding()
flooding.flooding()