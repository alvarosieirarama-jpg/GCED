# -*- coding: utf-8 -*-
from paciente import Paciente
from avl_tree import AVL
import copy
import ast

def read_patients(ruta_csv):
    """
    Lee pacientes desde un archivo CSV y los inserta en un árbol AVL.

    Args:
        ruta_csv (str): Ruta del archivo CSV que contiene los datos de los pacientes.

    Returns:
        AVL: Árbol AVL con los pacientes insertados, indexados por su DNI.
    """
    import csv

    with open(ruta_csv, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        arbol = AVL()
        for fila in lector:
            dni = fila["DNI"]
            nombre = fila["Nombre"]
            sexo = fila["Sexo"]
            edad = fila["Edad"]
            diagnosticos = ast.literal_eval(fila["Diagnosticos"])
            alergias = ast.literal_eval(fila["Alergias"])
            fecha_ultima_visita = fila["FechaUltimaVisita"]
            print(f'TODO: insert patient {dni} in ALV tree')  # Línea de depuración
            paciente = Paciente(dni, nombre, sexo, edad, diagnosticos, alergias, fecha_ultima_visita)
            arbol[dni] = paciente
        return arbol

def base_combinada(arbol_a, arbol_b):
    """
    Combina dos bases de datos de pacientes en un solo árbol AVL.

    Si un paciente aparece en ambos árboles, se conserva la información del
    paciente con la última fecha de visita. Se combinan diagnósticos y alergias sin duplicados.

    Args:
        arbol_a (AVL): Primer árbol AVL de pacientes.
        arbol_b (AVL): Segundo árbol AVL de pacientes.

    Returns:
        AVL: Árbol AVL combinado con los datos unificados de ambos árboles.
    """
    base_combinada = AVL()

    for paciente in arbol_a:
        paciente_a = copy.deepcopy(arbol_a[paciente])
        base_combinada[paciente] = paciente_a

    for paciente in arbol_b:
        paciente_b = copy.deepcopy(arbol_b[paciente])
        if paciente not in base_combinada:
            base_combinada[paciente] = paciente_b
        else:
            if paciente_b.fecha_ultima_visita > base_combinada[paciente].fecha_ultima_visita:
                save = copy.deepcopy(base_combinada[paciente])
                base_combinada[paciente] = paciente_b
                paciente_b = copy.deepcopy(save)
            for diagnostico in paciente_b.diagnosticos:
                if diagnostico not in base_combinada[paciente].diagnosticos:
                    base_combinada[paciente].diagnosticos.append(diagnostico)
            for alergia in paciente_b.alergias:
                if alergia not in base_combinada[paciente].alergias:
                    base_combinada[paciente].alergias.append(alergia)

    return base_combinada

def base_comun(arbol_a, arbol_b):
    """
    Genera una base de datos común con los pacientes que están presentes en ambos árboles.

    Si un paciente aparece en ambos árboles, se conserva la información del
    paciente con la última fecha de visita y se unifican diagnósticos y alergias sin duplicados.

    Args:
        arbol_a (AVL): Primer árbol AVL de pacientes.
        arbol_b (AVL): Segundo árbol AVL de pacientes.

    Returns:
        AVL: Árbol AVL con los pacientes comunes a ambos árboles.
    """
    base_comun = AVL()

    for paciente in arbol_a:
        if paciente in arbol_b:
            paciente_a = copy.deepcopy(arbol_a[paciente])
            paciente_b = copy.deepcopy(arbol_b[paciente])
            if paciente_b.fecha_ultima_visita > paciente_a.fecha_ultima_visita:
                base_comun[paciente] = paciente_b
                paciente_b = copy.deepcopy(paciente_a)
            else:
                base_comun[paciente] = paciente_a
            for diagnostico in paciente_b.diagnosticos:
                if diagnostico not in base_comun[paciente].diagnosticos:
                    base_comun[paciente].diagnosticos.append(diagnostico)
            for alergia in paciente_b.alergias:
                if alergia not in base_comun[paciente].alergias:
                    base_comun[paciente].alergias.append(alergia)

    return base_comun

if __name__ == "__main__":
    # Carga las bases de datos de pacientes desde archivos CSV
    arbol_saludplus = read_patients("pacientes_saludplus.csv")
    arbol_vitalclinic = read_patients("pacientes_vitalclinic.csv")

    while True:
        # Mostrar el menú de opciones
        print("\n--- Menú de opciones ---")
        print("1. Generar base combinada")
        print("2. Generar base común")
        print("3. Salir del programa")

        opcion = input("Ingrese el número de la opción que desee: ")

        if opcion == "1":
            base_combinada = base_combinada(arbol_saludplus, arbol_vitalclinic)
            print("Base combinada:")
            for paciente in base_combinada:
                print(base_combinada[paciente])

        elif opcion == "2":
            base_comun = base_comun(arbol_vitalclinic, arbol_saludplus)
            print("Base común:")
            for paciente in base_comun:
                print(base_comun[paciente])

        elif opcion == "3":
            print("Saliendo del programa...")
            break
