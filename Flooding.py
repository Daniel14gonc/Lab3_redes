from Nodo import Node
from Text_Manager import *
import xmpp
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream import ET
import json

class Flooding(Node):

    def __init__(self, data):
        super().__init__(data)

    async def menu_algoritmos(self):
        op = ''
        while op != '2':
            op = await flooding_menu()
            if op == '1':
                await self.input_message()
            
        
        await self.deleteaccount()
        

    async def input_message(self):
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
        await self._send_message_neighbors(json_text)
        await pretty_print_async("Mensaje enviado", "green")

    async def _send_message_neighbors(self, message):
        for n in self.neighbors:
            self.send_message_xmpp(mensaje=message, destino=n)

    async def intercept_message(self, json_text):
        origen = json_text['headers']['origen']
        destino = json_text['headers']['destino']
        intermediarios = json_text['headers']['intermediarios']
        message = json_text['payload']
        
        if self.name_domain == destino:
            text = f"Contenido de mensaje: {message}"
            await pretty_print_async(text, "aqua")
        elif self.name_domain not in intermediarios:
            json_text['headers']['intermediarios'].append(self.name_domain)
            text = json.dumps(json_text)
            de = destino.replace("@alumchat.xyz","").replace("archila161250","").split("/")[0]
            await self._send_message_neighbors(text)
            await pretty_print_async(f"Mensaje reenviado de:'{de}' a vecinos", "magenta")
        else:
            await pretty_print_async(f"Mensaje ya había pasado por el nodo. Se aborta", "yellow")