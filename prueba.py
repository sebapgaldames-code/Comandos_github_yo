import os
os.system("cls")
from pymongo import MongoClient
import json
import time

uri='mongodb://localhost:27017/'
client=MongoClient(uri)
db=client["eventos_db"]
col_invitados= db["invitados"]
col_eventos= db["eventos"]

def menu():
    print("-------- MENU EVENTOS --------")
    print("1. Cargar invitados Json")
    print("2. Cargar eventos Json")
    print("3. Ver invitados")
    print("4. Ver eventos")
    print("5. Buscar invitado y evento por nombre con $lookup")
    print("6. Validar acceso y estado de confirmacion")
    print("7. Buscar evento por fecha")
    print("8. Salir")
    opcion = input("Seleccione una opcion: ")
    return opcion

def cargar_invitados():
    try:
        archivo = open("invitados.json", "r")
        data_invitados = json.load(archivo)
        archivo.close()

        for invitado in data_invitados:
            col_invitados.insert_one(invitado)
        print("Invitados ingresados")

    except:
        print("Error al cargar invitados")

def cargar_eventos():
    try:
        archivo = open("eventos.json", "r")
        data_eventos = json.load(archivo)
        
        for eventos in data_eventos:
            col_eventos.insert_one(eventos)

    except:
        print("Error al cargar eventos")

def ver_invitados():
    rut = input("Ingrese el Rut del invitado que desea ver: ")
    invitado = col_invitados.find_one({"rut": rut})
    if invitado:
        print(f"Rut: {invitado['rut']}, Nombre: {invitado['nombre']}, Correo: {invitado['correo']}, Empresa: {invitado['empresa']}, Estado: {invitado['estado']}")
        time.sleep(2)
    else:
        print("Invitado no encontrado")

def ver_eventos():
    codigo = input("Ingrese el codigo del evento a revisar: ")
    evento = col_eventos.find_one({"codigo": codigo})
    if evento:
        print(f"Codigo: {evento['codigo']}, Nombre: {evento['nombre']}, Fecha: {evento['fecha']}, Lugar: {evento['lugar']}, Categoria: {evento['categoria']} ")
        time.sleep(2)
    else:
        print("Evento no encontrado")


def buscar_invitado_evento():
    evento_nombre = input("Ingrese el nombre del evento: ")
    pipeline = [
        {"$match": {"nombre": evento_nombre}},
        {"$lookup": {
            "from": "invitados",
            "localField": "invitados",
            "foreignField": "rut",
            "as": "detalles_invitados"
        }}
    ]
    resultado = list(db.eventos.aggregate(pipeline))
    if resultado:
        evento = resultado[0]
        print(f"Evento: {evento['nombre']}, Fecha: {evento['fecha']}, Lugar: {evento['lugar']}")
        print("Invitados:")
        for invitado in evento['detalles_invitados']:
            print(f"Nombre: {invitado['nombre']}, RUT: {invitado['rut']}, Confirmación: {invitado['confirmacion']}")
    else:
        print("Evento no encontrado.")

def validar_acceso():
    rut = input("Ingrese el RUT del cliente: ")
    evento_nombre = input("Ingrese el nombre del evento: ")
    invitado = col_invitados.find_one({"rut": rut})
    evento = col_eventos.find_one({"nombre": evento_nombre})
    if invitado and evento:
        if rut in evento['invitados']:
            print(f"Acceso permitido para {invitado['nombre']} al evento {evento['nombre']}. Confirmación: {invitado['confirmacion']}")
        else:
            print(f"Acceso denegado para {invitado['nombre']} al evento {evento['nombre']}. No está en la lista de invitados.")
    else:
        print("Invitado o evento no encontrado.")

def buscar_evento_fecha():
    fecha = input("Ingrese la fecha del evento (YYYY-MM-DD): ")
    eventos = col_eventos.find({"fecha": fecha})
    print(f"Eventos en la fecha {fecha}:")
    for evento in eventos:
        print(f"Nombre: {evento['nombre']}, Lugar: {evento['lugar']}, Categoria: {evento['categoria']}")

while True:
    opcion = menu()
    if opcion == "1":
        cargar_invitados()
    elif opcion == "2":
        cargar_eventos()
    elif opcion == "3":
        ver_invitados()
    elif opcion == "4":
        ver_eventos()
    elif opcion == "5":
        buscar_invitado_evento()
    elif opcion == "6":
        validar_acceso()
    elif opcion == "7":
        buscar_evento_fecha()
    elif opcion == "8":
        print("Saliendo del programa...")
        break
    else:
        print("Opcion no valida, intente nuevamente")