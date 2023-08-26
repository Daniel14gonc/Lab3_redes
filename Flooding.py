
class Flooding(object):
    
    def __init__(self):
        self.pedir()

    def pedir(self):
        self.me = input("Ingresa el nombre del nodo> ")
        misvecinos = input("Ingresa los vecinos separados por coma> ")
        self.vecinos = misvecinos.split(",")
    
    def send_message(self, message, destino):
        print(f"Enviando mensaje a mis vecinos:  {self.vecinos} ")
        print("Destinatario del mensaje: ", destino)
        print(f"Tabla de visitados: [{self.me}]")
        print("Mensaje: ", message)
    
    def receive_message(self, message, emisor, tabla_visitados):
        if destino == self.me:
            print(f"Mensaje recibido de: {emisor} el mensaje es: {mensaje}")
        elif self.me in tabla_visitados:
            print("Mensaje ya enviado, no es necesario reenviarlo")
        else:
            print("Enviando mensaje a mis vecinos: ", self.vecinos)
            print(f"Destinatario del mensaje: {destino} emisor: {emisor}")
            print("Tabla de visitados: [", tabla_visitados+f", {self.me}] ")

flooding = Flooding()

opcion = "0"
while opcion != "3":
    print("\n\n1. Enviar mensaje")
    print("2. Recibir mensaje")
    print("3. Salir")
    opcion = input("Ingrese opcion> ")
    if opcion == "1":
        mensaje = input("Ingrese el mensaje> ")
        destino = input("Ingrese el destino> ")
        flooding.send_message(mensaje, destino)
    elif opcion == "2":
        recibido = input("Ingrese el mensaje de la forma 'destino,mensaje,emisor'> ")
        tupla = recibido.split(",")
        destino = tupla[0]
        mensaje = tupla[1]
        emisor = tupla[2]
        tabla_visitados = input("Ingrese la tabla de visitados de la forma 'nodo1,nodo2,nodo3'> ")
        flooding.receive_message(mensaje, emisor, tabla_visitados)
        