from Text_Manager import *
import xmpp
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout

class Node(object):
    def __init__(self,data):
        self.name = data["nombre"]
        self.neighbors = data["vecinos"]
        self.is_connected = False
        
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # Ping
        self.register_plugin('xep_0045') # MUC
        self.register_plugin('xep_0085') # Notifications
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub
        
        self.add_event_handler("session_start", self.LogIn)
        self.add_event_handler('subscription_request', self.suscripcion_entrante)
        self.add_event_handler("message", self.message)
        
        self.inicialize_node()

        
    async def LogIn(self,event):
        
        try :
            # Obtener roster al inicar sesión para cargar todo
            #-------------------------------------------------
            self.send_presence()
            await self.get_roster()
            self.is_connected = True
            await pretty_print_async("Conectado correctamente","green")
            #-------------------------------------------------
            
        except IqError as errorIE:
            await pretty_print_async("Error:\nNo se pudo iniciar sesión","red")
            self.is_connected = False
            self.disconnect()
        except IqTimeout:
            await pretty_print_async("\nError:\nSe ha excedido el tiempo de respuesta","red")
            self.is_connected = False
            self.disconnect()
        
        except Exception as e:
            await pretty_print_async(e,"red")
            self.is_connected = False
            self.disconnect()
            
            
    async def suscripcion_entrante(self,presence):
        if presence['type'] == 'subscribe':
            try:
                self.send_presence_subscription(pto=presence['from'], ptype='subscribed')
                await self.get_roster()
            except IqError as e:
                await pretty_print_async(f"Problemas para enviar la solicitud: {e.iq['error']['text']}", "red")
            except IqTimeout:
                await pretty_print_async("\nError:\nSe ha excedido el tiempo de respuesta","red")

    async def add_neighbors(self):
        for neighbor in self.neighbors:
            try:
                self.send_presence_subscription(pto=neighbor, ptype='subscribe')
                await self.get_roster()
            except IqError as e:
                await pretty_print_async(f"Problemas para enviar la solicitud: {e.iq['error']['text']}", "red")
            except IqTimeout:
                await pretty_print_async("\nError:\nSe ha excedido el tiempo de respuesta","red")
            
    async def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            try:
                emisor = msg['from']
                json_text = eval(msg['body'])
                await pretty_print_async(f"Mensaje recibido de {emisor} contenido: {json_text}","green")


            except:
                await aprint("\033[31m]No se pudo recibir el archivo\033[0m")#cambiar


        
    async def inicialize_node(self):
        valid_register = self.register(self.name,self.name)
        
        if valid_register:
            self.LogIn()
            ainput("Al presionar Enter se agregaran los vecinos")
            await self.add_neighbors()
        else:
            await pretty_print_async("No se pudo registrar el nodo","red")
        pass
        
    def register(client, password):

        client ='Archila161250'+client+'@alumchat.xyz' # agregar dominio
        jid = xmpp.JID(client)
        account = xmpp.Client(jid.getDomain(), debug=[])
        account.connect()
        # return True si el registro fue exitoso
        return bool(
            xmpp.features.register(account, jid.getDomain(), {
                'username': jid.getNode(),
                'password': password
            }))  
        
    
    
    