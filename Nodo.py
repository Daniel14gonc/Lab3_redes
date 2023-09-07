from Text_Manager import *
import xmpp
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream import ET
import asyncio



def register(client, password):

        jid = xmpp.JID(client)
        account = xmpp.Client(jid.getDomain(), debug=[])
        account.connect()
        # return True si el registro fue exitoso
        return bool(
            xmpp.features.register(account, jid.getDomain(), {
                'username': jid.getNode(),
                'password': password
            })) 

class Node(slixmpp.ClientXMPP):
    def __init__(self,data):
        self.name = data["nombre"]
        self.neighbors = data["vecinos"]
        super().__init__(self.name, self.name)
        self.name_domain = self.name.lower()
        self.is_connected = False
        self.prefijo = "archila161250"
        
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # Ping
        self.register_plugin('xep_0045') # MUC
        self.register_plugin('xep_0085') # Notifications
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub
        
        self.add_event_handler("session_start", self.LogIn)
        self.add_event_handler('subscription_request', self.suscripcion_entrante)
        self.add_event_handler("message", self.message)
        
    
    
    
    async def start_all(self,result):
        result.set_result(True)
        await ainput("Al presionar Enter se agregaran los vecinos")
        await self.add_neighbors()
        try:
            await self.menu_algoritmos()
        except Exception as e:
            await pretty_print_async(e,"red")
        
        
    async def LogIn(self,event):
        
        try :
            # Obtener roster al inicar sesión para cargar todo
            #-------------------------------------------------
            self.send_presence()
            await self.get_roster()
            self.is_connected = True
            await pretty_print_async("Conectado correctamente","green")
            #-------------------------------------------------
            
            try:
                loop = asyncio.get_event_loop()
                result= asyncio.Future()
                menu = asyncio.create_task(self.start_all(result))
                await menu
                if result.result():
                    await pretty_print_async("Desconectando...","red")
                    self.is_connected = False
                    menu.cancel()
                    self.disconnect()
                    
                    
            except:
                print("\033[31m\nError:\nAlgo inesperado ha pasado revisa tu conexión\033[0m")
                self.is_connected = False
            
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

    async def menu_algoritmos(self):
        pass      

    def send_message_xmpp(self,destino,mensaje):
        self.send_message(mto=destino,mbody=mensaje,mtype='chat')
        
        
    async def intercept_message(self, json_text):
        pass
    
            
    async def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            try:
                emisor = str(msg['from'])
                emisor = emisor.replace(self.prefijo,"").replace("@alumchat.xyz","").split("/")[0]
                json_text = eval(msg['body'])
                await pretty_print_async(f"Mensaje recibido de '{emisor}'","green")
                await self.intercept_message(json_text)
            except Exception as e:
                await pretty_print_async("Formato del json es incorrecto","red")
                await pretty_print_async(e,"red")
                
        
        
    async def get_contacts(self):
        #Obtener contactos
        await self.get_roster()
        roster = self.client_roster
        concats = roster.keys()
        
        concats = [jid for jid in roster.keys() if jid != self.name_domain]


        
        Lista_contactos = {}
        
        if not concats:
            return Lista_contactos
        
        # Recorrer cada contacto y obtener su estado
        # Unicamente manejamos NC = "No conectado" y YC = "Conectado"
        # El objetivo es utilizarlo para notificaciones de conectados y desconectados  
        for u in concats:
            Lista_contactos[u] = "NI" 
            
        return Lista_contactos
        
        
    async def menu_mensajes_priv(self):
        enviar_a = await self.get_contacts()
        await aprint('\033[92mLista de contactos:\033[0m')
        cont=1
        dicct = {}
        #Obtener los contactos que no son grupos
        for key in enviar_a.keys():
            if "conference.alumchat.xyz" not  in key:
                await aprint('\033[38;5;208m',cont,')\033[96m',key,'\033[0m')
                dicct[cont] = key
                cont+=1
        await aprint('\033[38;5;208m',cont,')\033[96m Ingresar manualmente')
        dicct[cont] = "Ingresar manualmente"
        valido = False
        
        #verificar que la opción sea válida para seleccionar usuario a enviar
        while not valido:
            try:
                op = await ainput("Ingresa el número del contacto al que deseas enviar un mensaje:")
                op = int(op)
                if op > 0 and op <= len(enviar_a)+1:
                    valido = True
                else:
                    await pretty_print_async("Ingresa un número válido","red")
            except ValueError:
                await pretty_print_async("Ingresa un número válido","red")   
                
        if op == cont: # Ingresar manualmente
            dicct[cont] = await ainput("Ingresa el nombre del usuario al que deseas enviar un mensaje (sin dominiio ni prefijo):")
            dicct[op] = self.prefijo+dicct[op]+"@alumchat.xyz"
        men = await ainput("Ingresa el mensaje que deseas enviar:")
        return (dicct[op].lower(),men)  
    
    
    

            
        
    


        

    
    
    