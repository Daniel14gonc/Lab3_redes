from Nodo import Node
from Text_Manager import *
import xmpp
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream import ET
import json
import heapq
import asyncio
import datetime
import copy


class DistanceVector(Node):
    def __init__(self, data):
        super().__init__(data)
        self.ready = False
        self.temporizador = None
        self.tiempo = 30
        self.already_started = False
        self.converged = False
        self.tabla = {}
        self.create_table()
        self.old_table = self.tabla.copy()
        self.hop_table = {self.name_domain: self.name_domain}
        self.infinity = 1000000000000
        self.table_timestamp = {}
        for n in self.neighbors:
            self.hop_table[n] = n
        

    def create_table(self):
        self_entry = {self.name_domain: 0} 
        for n in self.neighbors:
            if n != self.name_domain:
                self_entry[n] = 1
        
        self.tabla[self.name_domain] = self_entry
    
    async def add_entry_to_table(self, node, entry,tiempo):
        if node not in self.table_timestamp:
            self.table_timestamp[node] = tiempo
            self.tabla[node] = entry
            await pretty_print_async(f"tabla recibida de {node}: {entry}","yellow")
        
        elif self.table_timestamp[node] < tiempo:
            self.table_timestamp[node] = tiempo
            self.tabla[node] = entry
            await pretty_print_async(f"tabla recibida de {node}: {entry}","yellow")
        else:
            pass
        

        self.tabla[node] = entry
        await pretty_print_async(f"tabla recibida de {node}: {entry}","yellow")

    async def add_node_to_table(self, node):
        self_table = self.tabla[self.name_domain]
        if node not in self_table:
            self_table[node] = self.infinity
        self.tabla[self.name_domain] = self_table
        

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
        # if not self.already_started:
        await self.activate_timer()
        await self._send_flooding_message()
            

    async def _send_flooding_message(self):
        origen = self.name_domain
        # Obtener la fecha y hora actual
        fecha_hora_actual = datetime.datetime.now()

        # Convertir la fecha y hora actual en un timestamp UNIX
        timestamp = fecha_hora_actual.timestamp()
        message = {
                "type": "info",
                "headers": {
                    "origen": origen,
                    "intermediarios": [origen],
                    "timestamp": timestamp,
                },
                "payload": self.tabla[origen]
        }
        
        message = json.dumps(message)

        await self._send_message_neighbors(message)

    async def _send_message_neighbors(self, message):
        for n in self.neighbors:
            self.send_message_xmpp(mensaje=message, destino=n)
    
    def brute_force(self,key,Node):
        table_values = self.tabla[key]
        if Node not in table_values:
            table_values[Node] = self.infinity
        
        self.tabla[key] = table_values
        return Node, table_values[Node]
            
    def set_new_cost(self, key, Node, cost):
        table_values = self.tabla[key]
        table_values[Node] = cost
        
    async def recalculate_table(self):
        for n in self.tabla:
            if n != self.name_domain:
                objetivo, costo = self.brute_force(self.name_domain, n)
                for n1 in self.tabla:
                    if n1 != self.name_domain and n1 != objetivo:
                        costo1 = self.brute_force(n1,objetivo)[1]
                        costo2 = self.brute_force(self.name_domain,n1)[1]
                        if costo1 + costo < costo2:
                            self.set_new_cost(self.name_domain,n1,costo1 + costo)
                            self.hop_table[n1] = objetivo
        
        # if self.old_tabla == self.tabla:
        #     await pretty_print_async("Convergencia alcanzada", "green")
        
        # self.old_table = self.tabla.copy()
    
    def get_next_node(self, destination):
        try:
            return (True, self.hop_table[destination])
        except:
            return (False, destination)

    async def algoritmo(self):
        await self.recalculate_table()
    
    async def set_ready(self):
        await pretty_print_async("\nTiempo de espera terminado. Estoy listo para mandar mensajes.\n", "magenta")
        await pretty_print_async(">", "none")
        self.ready = True
        # await self.algoritmo()

    async def iniciar_temporizador(self, tiempo_espera):
        await pretty_print_async(f"Es necesario esperar {tiempo_espera} segundos para iniciar el algoritmo", "yellow")
        await asyncio.sleep(tiempo_espera)
        await self.set_ready()
        
    async def activate_timer(self):
        if self.temporizador is not None:
            self.temporizador.cancel()
        self.temporizador = asyncio.create_task(self.iniciar_temporizador(self.tiempo))

    async def check_convergence(self):
        return self.tabla[self.name_domain] == self.old_table[self.name_domain]

    async def update_table(self, origin, entry,tempo):
        self.old_table = copy.deepcopy(self.tabla)
        await self.add_node_to_table(origin)
        await self.add_entry_to_table(origin, entry,tempo)
        await self.algoritmo()
        if await self.check_convergence():
            await pretty_print_async("Convergencia alcanzada", "green")
            self.converged = True
        else:
            await self.activate_timer()
            await self._send_flooding_message()
        

    async def handle_info_message(self, json_text):
        origen = json_text['headers']['origen']
        intermediarios = json_text['headers']['intermediarios']
        try:
            tempo = json_text['headers']['timestamp']
        except:
            fecha_hora_actual = datetime.datetime.now()
            tempo = fecha_hora_actual.timestamp()
        
        payload = json_text['payload']
        await pretty_print_async(payload, "yellow")
        if self.name_domain not in intermediarios and not self.ready:
            json_text['headers']['intermediarios'].append(self.name_domain)
            message = json.dumps(json_text)
            await self._send_message_neighbors(message)
            await self.update_table(origen, payload,tempo)
            
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
            exists, siguiente= self.get_next_node(user)
            if not exists:
                await pretty_print_async("El nodo destino no existe", "red")
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
            if self.name_domain == destino:
                text = f"Origen de mensaje: {origen}"
                await pretty_print_async(text, "aqua")
                text = f"Contenido de mensaje: {message}"
                await pretty_print_async(text, "aqua")
            else:
                text = json.dumps(json_text)
                de = clean_nombre(origen)
                exists, siguiente = self.get_next_node(destino)
                if not exists:
                    await pretty_print_async("El nodo destino no existe", "red")
                    return
                # await pretty_print_async(f"{str(siguiente)}", "magenta")
                siguiente_text = clean_nombre(siguiente)
                destino_text = clean_nombre(destino)
                self.send_message_xmpp(mensaje=text, destino=siguiente)
                await pretty_print_async(f"Mensaje proveniente: '{de}',para {destino_text}. Reenviando a '{siguiente_text}' ", "magenta")

        else:
            await pretty_print_async("Esperando a que la topología se complete, no es posible enviar mensajes", "yellow")
   
      
    async def intercept_message(self, json_text):
        type = json_text['type']
        if type == 'info':
            await self.handle_info_message(json_text)
        else:
            await self.handle_message(json_text)