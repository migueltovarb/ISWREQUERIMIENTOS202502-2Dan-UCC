import os
import csv

ARCHIVO= "funciones.csv" "ventas.csv"

if os.path.exists(ARCHIVO):
    with open(ARCHIVO, newline="",encoding="utf=8") as f:
        funcion = list(csv.DictReader(f))
else:
    funcion = []

while True:
    print("----- VENTA DE BOLETOS ----")
    print('1. Registar Funcion')
    print('2. Funciones Disponibles')
    print('3. Salir')

    op = input("Seleccione una opción: ")

    if op == "1":
        nombre_funcion = input("Funcion: ")
        precio_funcion = input("Precio: ")
        hora_funcion = input("Hora:")

        funcion.append({"funcion": nombre_funcion, "Precio": precio_funcion, "Hora": hora_funcion})
        print("Funcion registrada.")

    elif op == "2":
        criterio = input("Buscar por nombre: ").lower()
        encontrados = [f for f in funcion if criterio in f["funcion"].lower()]
        if encontrados:
            for f in encontrados:
                print(f"- {f['funcion']}")
        else:
            print("No se encontró funcion.")

    elif op == "3":
        with open(ARCHIVO, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Funcion"])
            writer.writeheader()
            writer.writerows(funcion)
        print("Saliendo del programa")
        break
    else:
        print("Opción no existente.")