from Nodo import Node
from Text_Manager import *
import xmpp
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream import ET
import json
import heapq
import asyncio


class LinkState(Node):
    def __init__(self, data):
        super().__init__(data)
        self.topology = {self.name_domain: self.neighbors.copy()}
        self.ready = False
        self.temporizador = None
        self.tiempo = 30
        self.already_started = False

    async def menu_algoritmos(self):
        op = ''
        while self.is_connected:
            op = await link_state_menu()
            if op == '1':
                await self.start_flooding()
            if op == '2':
                await self.input_message()
            if op == '3':
                self.is_connected = False
    
    async def start_flooding(self):
        if not self.already_started:
            await self.activate_timer()
            self.already_started = True
            await self._send_flooding_message()
            

    async def _send_flooding_message(self):
        origen = self.name_domain
        message = {
                "type": "info",
                "headers": {
                    "origen": origen,
                    "intermediarios": [origen]
                },
                "payload": [n.lower() for n in self.neighbors if n != origen]
        }
        
        message = json.dumps(message)

        await self._send_message_neighbors(message)

    async def _send_message_neighbors(self, message):
        for n in self.neighbors:
            self.send_message_xmpp(mensaje=message, destino=n)

    def add_node_to_topology(self, origin, neighbors):
        if origin not in self.topology:
            self.topology[origin] = neighbors

    async def algoritmo(self):
        try:
            self.dijkstra()
        except Exception as e:
            await pretty_print_async("Error en Dijkstra", "red")
            await pretty_print_async(e, "red")
    
    async def set_ready(self):
        await pretty_print_async("\nTiempo de espera terminado. Estoy listo para mandar mensajes.\n", "magenta")
        await pretty_print_async(">", "none")
        self.ready = True
        await self.algoritmo()

    async def iniciar_temporizador(self, tiempo_espera):
        await pretty_print_async(f"Es necesario esperar {tiempo_espera} segundos para iniciar el algoritmo", "yellow")
        await asyncio.sleep(tiempo_espera)
        await self.set_ready()
        
    async def activate_timer(self):
        if self.temporizador is not None:
            self.temporizador.cancel()
        self.temporizador = asyncio.create_task(self.iniciar_temporizador(self.tiempo))
        

    async def handle_info_message(self, json_text):
        origen = json_text['headers']['origen']
        intermediarios = json_text['headers']['intermediarios']
        payload = json_text['payload']
        self.add_node_to_topology(origen, payload)
        # await pretty_print_async(str(self.topology), "green")
        if self.name_domain not in intermediarios and not self.ready:
            json_text['headers']['intermediarios'].append(self.name_domain)
            message = json.dumps(json_text)
            await self._send_message_neighbors(message)
        
        await self.activate_timer()
        
    
    async def input_message(self):
        if self.ready:
            user, message = await self.menu_mensajes_priv()
            json_message = {
                "type": "message",
                "headers": {
                    "origen": self.name_domain,
                    "destino": user,
                    "intermediarios": [self.name_domain]
                },
                "payload": message
            }
            json_text = json.dumps(json_message)      
            siguiente = self.get_next_node(user)
            if siguiente is None:
                await pretty_print_async("No es posible enviar el mensaje, no existe una ruta", "red")
                return
            siguiente_text = clean_nombre(siguiente)
            self.send_message_xmpp(mensaje=json_text, destino=siguiente)
            await pretty_print_async(f"Enviando mensaje a '{siguiente_text}'", "magenta")
            await pretty_print_async("Mensaje enviado", "green")
        else:
            await pretty_print_async("Esperando a que la topología se complete, no es posible enviar mensajes", "yellow")

    async def handle_message(self, json_text):
        # await pretty_print_async(str(json_text), "green")
        if self.ready:
            origen = json_text['headers']['origen']
            destino = json_text['headers']['destino']
            message = json_text['payload']
            de = clean_nombre(origen)
            if self.name_domain == destino:
                text = f"Origen de mensaje: {de}"
                await pretty_print_async(text, "aqua")
                text = f"Contenido de mensaje: {message}"
                await pretty_print_async(text, "aqua")
            else:
                text = json.dumps(json_text)
                de = clean_nombre(origen)
                siguiente = self.get_next_node(destino)
                if siguiente is None:
                    await pretty_print_async("No es posible enviar el mensaje, no existe una ruta", "red")
                    return
                # await pretty_print_async(f"{str(siguiente)}", "magenta")
                siguiente_text = clean_nombre(siguiente)
                destino_text = clean_nombre(destino)
                self.send_message_xmpp(mensaje=text, destino=siguiente)
                await pretty_print_async(f"Mensaje proveniente: '{de}',para {destino_text}. Reenviando a '{siguiente_text}' ", "magenta")
        else:
            await pretty_print_async("Esperando a que la topología se complete, no es posible enviar mensajes", "yellow")
    
    def dijkstra(self):
        self.distances = {}
        self.previous = {}
        self.queue = []
        
        for node_upper in self.topology:
            node = node_upper.lower()
            if node == self.name_domain:
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
                alt = self.distances[u] + 1
                if alt < self.distances[v]:
                    self.distances[v] = alt
                    self.previous[v] = u
                    for i in range(len(self.queue)):
                        if self.queue[i][1] == v:
                            self.queue[i] = (alt, v)
                            heapq.heapify(self.queue)
    
        # Creación y almacenamiento de la tabla de enrutamiento
        self.routing_table = {}
        for node, previous_node in self.previous.items():
            if previous_node is not None:
                path = self.get_path(node)
                self.routing_table[node] = (path, self.distances[node])

    def get_path(self, destination):
        path = [destination]
        while destination in self.previous and self.previous[destination] is not None:
            destination = self.previous[destination]
            path.insert(0, destination)
            
        if len(path) == 1 and destination not in self.previous:
            return False, path
        
        return True, path
    
    def get_next_node(self, destination):
        result, path = self.get_path(destination)
        if not result:
            return None
        if len(path) > 1:
            return path[1]
        return path[0]
    
    async def intercept_message(self, json_text):
        type = json_text['type']
        if type == 'info':
            await self.handle_info_message(json_text)
        else:
            await self.handle_message(json_text)