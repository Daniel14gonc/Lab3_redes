from Nodo import Node
from Text_Manager import *
import xmpp
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream import ET
import json
import datetime

class Flooding(Node):

    def __init__(self, data):
        super().__init__(data)
        self.mensajes_recibidos = {}
    

    async def menu_algoritmos(self):
        op = ''
        while self.is_connected:
            op = await flooding_menu()
            if op == '1':
                await self.input_message()
            if op == '2':
                self.is_connected = False

    def get_time_stamp(self):
        return datetime.datetime.now().timestamp()     
    
    def verify_duplicated_message(self,origen,timestamp):  
        if origen not in self.mensajes_recibidos:
            self.mensajes_recibidos[origen] = timestamp
            return False
        else:
            if timestamp > self.mensajes_recibidos[origen]:
                self.mensajes_recibidos[origen] = timestamp
                return False
            else:
                return True

    async def input_message(self):
        user, message = await self.menu_mensajes_priv()
        origen = stupid_name(self.name_domain)
        user = stupid_name(user)
        json_message = {
            "type": "message",
            "headers": {
                "origen": origen,
                "destino": user,
                "intermediarios": [origen],
                "timestamp": self.get_time_stamp()
            },
            "payload": message
        }
        json_text = json.dumps(json_message)        
        await self._send_message_neighbors(json_text)
        await pretty_print_async("Mensaje enviado", "green")

    async def _send_message_neighbors(self, message):
        for n in self.neighbors:
            self.send_message_xmpp(mensaje=message, destino=n)

    async def intercept_message(self, json_text):
        origen = json_text['headers']['origen']
        origen = origen + "@alumchat.xyz"
        destino = json_text['headers']['destino']
        intermediarios = json_text['headers']['intermediarios']
        message = json_text['payload']
        new_origen = clean_nombre(origen)
        self_name = stupid_name(self.name_domain)
        if self_name == destino and self.verify_duplicated_message(origen, json_text['headers']['timestamp']) == False:
            text = f"Origen de mensaje: {new_origen}"
            await pretty_print_async(text, "aqua")
            text = f"Contenido de mensaje: {message}"
            await pretty_print_async(text, "aqua")
        elif self_name not in intermediarios:
            json_text['headers']['intermediarios'].append(self_name)
            text = json.dumps(json_text)
            de = clean_nombre(origen)
            await self._send_message_neighbors(text)
            await pretty_print_async(f"Mensaje reenviado de:'{de}' a vecinos", "magenta")
        else:
            await pretty_print_async(f"Mensaje ya había pasado por el nodo. Se aborta", "yellow")