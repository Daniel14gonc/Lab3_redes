# Laboratorio 3 Parte 2

## Integrantes
* Sebastián Aristondo Pérez
* Daniel Gonzalez Carrillo

## Descripción
En este laboratorio se implementaron los algoritmos de enrutamiento: 
- Link State
- Flooding
- Distance Vector

Para simular los nodos de una red se utilizaron clientes de XMPP, de forma que se pudiera usar el protocolo para
enviar mensajes entre nodos, simulando una red.

## Uso

Para poder usar el programa se debe crear un ambiente virtual:

```bash
  python -m venv myenv
```

En lugar de 'myenv' puede ir cualquier nombre que se le quiera dar al ambiente virtual. Luego, para activar el ambiente
se usa

```bash
  ./myenv/Scripts/activate
```
En la terminal.

Para instalar las librerías en el ambiente virtual se debe usar 

```bash
  pip install -r requirements.txt
```

Luego para correr el programa

```bash
  python main.py
```

Donde se tendrán opciones para elegir que algorimto utilizar.
