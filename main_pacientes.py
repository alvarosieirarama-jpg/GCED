# Martín Quinteiro González   martin.quinteiro.gonzalez@udc.es
# Álvaro Sieira Rama          alvaro.sieira.rama@udc.es

from array_queue import ArrayQueue
from paciente import Paciente
from gestor_turnos import GestorColas
import sys
import pandas as pd

if __name__ == "__main__":
    """
    Punto de entrada principal para la gestión de turnos de pacientes.
    Lee los datos de los pacientes desde un archivo de texto, los agrega a la cola de admisión,
    y gestiona las colas de espera.
    """

    cola_admision = ArrayQueue()  # Crear una cola de admisión para almacenar pacientes.
    
    with open("patients1.txt", "r", encoding="utf-8") as file:
        """
        Abre y lee el archivo de texto que contiene la información de los pacientes.
        Procesa cada línea del archivo y extrae los datos necesarios para crear instancias de pacientes.
        """
        for line in file:
            parts = line.strip().split()  # Dividir la línea en partes
            IDPac = parts[0]
            tipo_consulta = parts[1]
            urgencia = parts[2]
            tiempo_estimado = int(parts[3])

            """
            Crea una instancia de la clase Paciente con la información extraída de cada línea.
            Luego, agrega al paciente a la cola de admisión.
            """
            cola_admision.enqueue(Paciente(IDPac=IDPac, tipo_consulta=tipo_consulta, urgencia=urgencia, 
                                           tiempo_estimado=tiempo_estimado, tiempo_llegada=None, 
                                           tiempo_entrada_consulta=None, priorizacion=False))

    listas_espera = GestorColas(
        general_priority=ArrayQueue(), general_no_priority=ArrayQueue(), 
        specialist_no_priority=ArrayQueue(), specialist_priority=ArrayQueue(), priorizacion=[]
    )
    """
    Crea una instancia de GestorColas que gestionará diferentes colas de espera según las prioridades
    y tipos de consulta de los pacientes.
    """

    lista_pandas = listas_espera.gestion_lista_espera(cola_admision)
    """
    Utiliza el gestor de colas para organizar y gestionar la lista de espera de pacientes.
    La función 'gestion_lista_espera' procesa la cola de admisión y retorna la lista organizada.
    """

    data = pd.DataFrame(lista_pandas, columns=['IDPac', 'tipo_consulta', 'priorizacion', 'cola_espera', 'tiempo_espera'])
    """
    Convierte la lista de pacientes procesada en un DataFrame de pandas para facilitar su análisis.
    El DataFrame contiene columnas con la información relevante de los pacientes.
    """
    print(data, '\n')
    print(lista_pandas)

    group_col = ['tipo_consulta']
    target_col = "priorizacion"
    data_pandas1 = data.groupby(group_col).agg({target_col: ["mean"]})
    """
    Agrupa los datos por tipo de consulta y calcula la media de la priorización para cada grupo.
    El resultado es un análisis que muestra la priorización media según el tipo de consulta.
    """
    print("################################################")
    print("  Priorización media agrupada por tipo de consulta      ")
    print("###############################################\n")
    print(data_pandas1)

    group_col = ['cola_espera']
    target_col = "tiempo_espera"
    data_pandas1 = data.groupby(group_col).agg({target_col: ["mean"]})
    """
    Agrupa los datos por cola de espera y calcula el tiempo medio de espera para cada cola.
    Esto permite analizar el tiempo de espera promedio según las diferentes colas de pacientes.
    """
    print("##############################################")
    print(" Tiempo medio de espera agrupado por cola de espera      ")
    print("###############################################\n")
    print(data_pandas1)
