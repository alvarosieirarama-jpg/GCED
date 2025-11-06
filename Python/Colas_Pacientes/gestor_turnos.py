# Martín Quinteiro González   martin.quinteiro.gonzalez@udc.es
# Álvaro Sieira Rama          alvaro.sieira.rama@udc.es

from array_queue import ArrayQueue
from paciente import Paciente

class GestorColas:
    """
    Clase GestorColas que gestiona las colas de pacientes según su tipo de consulta y urgencia.
    Esta clase contiene varios métodos para almacenar pacientes en colas y gestionar el proceso
    de espera y consulta en función de su tipo de urgencia.

    Métodos
    -------
    almacenar_paciente(paciente, tiempo_actual):
        Clasifica los pacientes en colas de acuerdo con su tipo de consulta y urgencia.

    gestion_paciente(paciente, tiempo_actual, lista_penalizaciones, lista_tiempo_espera):
        Realiza la gestión de un paciente durante el proceso de consulta, realizando distintas acciones
        en función del tiempo de espera y la prioridad.
    """
    
    def __init__(self, general_priority, general_no_priority, specialist_priority, specialist_no_priority, priorizacion):
        """
        Inicializa el gestor de colas con las colas correspondientes para pacientes generales y especialistas,
        tanto con prioridad como sin ella.
        
        Parámetros:
        -----------
        general_priority : ArrayQueue
            Cola de pacientes generales con prioridad.
        general_no_priority : ArrayQueue
            Cola de pacientes generales sin prioridad.
        specialist_priority : ArrayQueue
            Cola de pacientes especialistas con prioridad.
        specialist_no_priority : ArrayQueue
            Cola de pacientes especialistas sin prioridad.
        priorizacion : list
            Lista de identificadores de pacientes que han sido priorizados.
        """
        self.general_priority = general_priority
        self.general_no_priority = general_no_priority
        self.specialist_priority = specialist_priority
        self.specialist_no_priority = specialist_no_priority
        self.priorizacion = []
    
    @property
    def general_priority(self):
        """
        Getter para la cola de pacientes generales con prioridad.
        """
        return self._general_priority
        
    @general_priority.setter
    def general_priority(self, value:ArrayQueue):
        """
        Setter para la cola de pacientes generales con prioridad. Se asegura de que el valor sea una instancia de ArrayQueue.
        
        Parámetros:
        ----------
        value : ArrayQueue
            Valor que se asignará a la cola de pacientes generales con prioridad.
            
        Excepciones:
        ------------
        ValueError
            Si el valor no es una instancia de ArrayQueue, se lanzará una excepción.
        """
        if isinstance(value, ArrayQueue):
            self._general_priority = value
        else:
            raise ValueError("general_priority must be a non-empty array")
    
    @property
    def general_no_priority(self):
        """
        Getter para la cola de pacientes generales sin prioridad.
        """
        return self._general_no_priority
        
    @general_no_priority.setter
    def general_no_priority(self, value:ArrayQueue):
        """
        Setter para la cola de pacientes generales sin prioridad. Se asegura de que el valor sea una instancia de ArrayQueue.
        
        Parámetros:
        ----------
        value : ArrayQueue
            Valor que se asignará a la cola de pacientes generales sin prioridad.
            
        Excepciones:
        ------------
        ValueError
            Si el valor no es una instancia de ArrayQueue, se lanzará una excepción.
        """
        if isinstance(value, ArrayQueue):
            self._general_no_priority = value
        else:
            raise ValueError("Name must be a non-empty array")
    
    @property
    def specialist_priority(self):
        """
        Getter para la cola de pacientes especialistas con prioridad.
        """
        return self._specialist_priority
        
    @specialist_priority.setter
    def specialist_priority(self, value:ArrayQueue):
        """
        Setter para la cola de pacientes especialistas con prioridad. Se asegura de que el valor sea una instancia de ArrayQueue.
        
        Parámetros:
        ----------
        value : ArrayQueue
            Valor que se asignará a la cola de pacientes especialistas con prioridad.
            
        Excepciones:
        ------------
        ValueError
            Si el valor no es una instancia de ArrayQueue, se lanzará una excepción.
        """
        if isinstance(value, ArrayQueue):
            self._specialist_priority = value
        else:
            raise ValueError("Name must be a non-empty array")
    
    @property
    def specialist_no_priority(self):
        """
        Getter para la cola de pacientes especialistas sin prioridad.
        """
        return self._specialist_no_priority
        
    @specialist_no_priority.setter
    def specialist_no_priority(self, value:ArrayQueue):
        """
        Setter para la cola de pacientes especialistas sin prioridad. Se asegura de que el valor sea una instancia de ArrayQueue.
        
        Parámetros:
        ----------
        value : ArrayQueue
            Valor que se asignará a la cola de pacientes especialistas sin prioridad.
            
        Excepciones:
        ------------
        ValueError
            Si el valor no es una instancia de ArrayQueue, se lanzará una excepción.
        """
        if isinstance(value, ArrayQueue):
            self._specialist_no_priority = value
        else:
            raise ValueError("Name must be a non-empty array")
    
    def almacenar_paciente(self, paciente, tiempo_actual):
        """
        Clasifica un paciente según su tipo de consulta y urgencia, y lo agrega a la cola correspondiente.
        
        Parámetros:
        -----------
        paciente : class
            Instancia de la clase Paciente, que contiene la información del paciente.
        tiempo_actual : int
            El tiempo actual de ejecución (es decir, el tiempo en el que el paciente llegó).
        
        Retorna:
        --------
        None
        """
        paciente.tiempo_llegada = tiempo_actual
        if paciente.tipo_consulta == "general":
            if paciente.urgencia == "priority" or paciente.priorizacion:
                self.general_priority.enqueue(paciente)
            else:
                self.general_no_priority.enqueue(paciente)
        else:
            if paciente.urgencia == "priority" or paciente.priorizacion:
                self.specialist_priority.enqueue(paciente)
            else:
                self.specialist_no_priority.enqueue(paciente)
    
    def gestion_lista_espera(self, cola_admision):
        """
        Gestiona el proceso completo de un paciente en la cola de espera, incluyendo la asignación de consultas y
        la priorización si es necesario.

        Parámetros:
        -----------
        cola_admision : ArrayQueue
            Cola de pacientes en espera que aún no han sido procesados.

        Retorna:
        --------
        list
            Una lista con los detalles de los pacientes procesados y sus tiempos de espera.
        """
        
        def pasa_paciente_a_consulta(lista, cnt, lista_pandas, lista_pacientes_priorizados):
            """
            Mueve un paciente de la cola de espera a la consulta, actualizando su tiempo de entrada y priorización si es necesario.
            
            Parámetros:
            -----------
            lista : ArrayQueue
                La cola de pacientes a gestionar.
            cnt : int
                El contador del tiempo actual.
            lista_pandas : list
                Lista donde se almacenan los resultados de la gestión de pacientes.
            lista_pacientes_priorizados : list
                Lista que contiene los identificadores de los pacientes priorizados.
            
            Retorna:
            --------
            paciente : class
                El paciente que fue movido a consulta.
            """
            paciente = lista.dequeue()
            paciente.tiempo_entrada_consulta = cnt
            if cnt - paciente.tiempo_llegada > 7 and paciente.IDPac not in self.priorizacion:
                self.priorizacion.append(paciente.IDPac)
                print(f'{cnt+1}: Priorización activa {paciente.IDPac}')
            
            print(f'{cnt+1}: {paciente.IDPac} entra {paciente.tipo_consulta}/{paciente.urgencia} '
                  f'ADM:{paciente.tiempo_llegada}, INI: {paciente.tiempo_entrada_consulta}, EST: {paciente.tiempo_estimado}')
            if paciente.IDPac in self.priorizacion:
                priority = True
            else:
                priority = False
            if paciente.IDPac in lista_pacientes_priorizados:
                if paciente.tipo_consulta == 'general':
                    cola_de_espera = 'general_priority'
                else:
                    cola_de_espera = 'specialist_priority'
                lista_pacientes_priorizados.remove(paciente.IDPac)
            else:
                if paciente.tipo_consulta == 'general':
                    cola_de_espera = 'general_no_priority'
                else:
                    cola_de_espera = 'specialist_no_priority'
            lista_pandas.append([paciente.IDPac, paciente.tipo_consulta, priority, cola_de_espera, 
                                 (paciente.tiempo_entrada_consulta - paciente.tiempo_llegada)])
            return paciente
        
        def fin_consulta(paciente, cnt):
            """
            Finaliza la consulta de un paciente si el tiempo actual es mayor que el tiempo estimado de consulta.
            
            Parámetros:
            -----------
            paciente : class
                El paciente que se está gestionando.
            cnt : int
                El contador del tiempo actual.
            
            Retorna:
            --------
            paciente : class or None
                El paciente si aún no ha terminado la consulta, o None si ya ha finalizado.
            """
            if cnt >= paciente.tiempo_entrada_consulta + paciente.tiempo_estimado:
                print(f'{cnt+1}: {paciente.IDPac} sale {paciente.tipo_consulta}/{paciente.urgencia} '
                      f'ADM:{paciente.tiempo_llegada}, INI: {paciente.tiempo_entrada_consulta}, '
                      f'EST./TOTAL: {paciente.tiempo_estimado}/{cnt-paciente.tiempo_llegada}')
                return None
            else:
                return paciente
        
        def gestion_consulta(paciente, priority, no_priority, cnt, lista_pandas, lista_pacientes_priorizados):
            """
            Gestiona el proceso de consulta de un paciente, moviéndolo entre las colas de espera y la consulta,
            dependiendo de su estado y prioridad.
            
            Parámetros:
            -----------
            paciente : class or None
                El paciente que se está gestionando.
            priority : ArrayQueue
                La cola de pacientes con prioridad.
            no_priority : ArrayQueue
                La cola de pacientes sin prioridad.
            cnt : int
                El contador del tiempo actual.
            lista_pandas : list
                Lista que contiene los resultados de la gestión de pacientes.
            lista_pacientes_priorizados : list
                Lista de los pacientes que han sido priorizados.
            
            Retorna:
            --------
            paciente : class or None
                El paciente que está siendo gestionado, o None si ya ha terminado su consulta.
            """
            if paciente == None:
                if not priority.is_empty():
                    paciente = pasa_paciente_a_consulta(priority, cnt, lista_pandas, lista_pacientes_priorizados)
                elif not no_priority.is_empty():
                    paciente = pasa_paciente_a_consulta(no_priority, cnt, lista_pandas, lista_pacientes_priorizados)
            else:
                paciente = fin_consulta(paciente, cnt)
                if paciente == None:
                    paciente = gestion_consulta(paciente, priority, no_priority, cnt, lista_pandas, lista_pacientes_priorizados)
            return paciente
        
        cnt = 0
        paciente_general = None
        paciente_specialist = None
        lista_pandas = []
        lista_pacientes_priorizados = []
        
        while True:
            if cnt % 3 == 0:
                if not cola_admision.is_empty():
                    paciente = cola_admision.dequeue()
                    paciente.tiempo_llegada = int(cnt)
                    if paciente.IDPac in self.priorizacion:
                        paciente.priorizacion = True
                        self.priorizacion.remove(paciente.IDPac)
                        print(f'{cnt}: Priorización aplicada {paciente.IDPac}')
                        lista_pacientes_priorizados.append(paciente.IDPac)
                    self.almacenar_paciente(paciente, cnt)
                    print(f'{cnt+1}: {paciente.IDPac} en cola {paciente.tipo_consulta}/{paciente.urgencia} EST:{paciente.tiempo_estimado}')
            
            paciente_general = gestion_consulta(paciente_general, self.general_priority, self.general_no_priority, cnt, lista_pandas, lista_pacientes_priorizados)
            paciente_specialist = gestion_consulta(paciente_specialist, self.specialist_priority, self.specialist_no_priority, cnt, lista_pandas, lista_pacientes_priorizados)

            if cola_admision.is_empty() and self.general_priority.is_empty() and self.general_no_priority.is_empty() \
                and self.specialist_no_priority.is_empty() and self.specialist_priority.is_empty() \
                and paciente_general == None and paciente_specialist == None:
                return lista_pandas
            else:
                cnt += 1
