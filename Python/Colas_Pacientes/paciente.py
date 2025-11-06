# Martín Quinteiro González   martin.quinteiro.gonzalez@udc.es
# Álvaro Sieira Rama          alvaro.sieira.rama@udc.es


from array_queue import ArrayQueue

class Paciente:
    """
    Se crea la clase abstracta Paciente.
    Incluira diferentes atributos definidos en las siguientes partes del codigo.
    A continuacion introducimos los metodos principales:
    
    Methods
    ------------
    __str__():
        Devuelve un string mostrando los atributos de la clase."""
    
    def __init__(self, IDPac, tipo_consulta, urgencia, tiempo_estimado, tiempo_llegada,tiempo_entrada_consulta, priorizacion):
        """
        Esta es la funcion constructora de la clase Paciente:

        Parameters
        ----------
        IDPac : str
            Distingue los diversos Pacientes que se llevan a cabo.
        tipo_consulta : str
            Distingue a los usuarios.
        urgencia : str
            Distingue los recursos que se llevan a cabo.
        tiempo_llegada : int
            Reprsenta el tiempo esperado de una ejecucion.
        tiempo_inicio_ejecucion : int
            Representa el tiempo de inicio de la ejecucion.
        tiempo_ejecucion : int
            Representa el tiempo total de la ejecucion.

        Returns
        -------
        None.
        """
        self.IDPac = IDPac
        self.tipo_consulta = tipo_consulta
        self.urgencia = urgencia
        self.tiempo_llegada = None
        self.tiempo_estimado = tiempo_estimado
        self.tiempo_entrada_consulta = None
        self.priorizacion = False

    @property 
    def IDPac (self):
     return self._IDPac
     
    @IDPac.setter
    def IDPac(self, value:str):
      if isinstance(value, str) and len(value) > 0:
         self._IDPac = value
      else:
         raise ValueError("IDPac must be a non-empty string") # Se lanza un error de tipo ValueError 
                                                              # si el valor de 'IDPac' no es una cadena no vacía

    @property
    def tipo_consulta (self):
      return self._tipo_consulta
     
    @tipo_consulta.setter
    def tipo_consulta(self, value:str):
      if isinstance(value, str) and len(value) > 0:
         self._tipo_consulta = value
      else:
         raise ValueError("tipo_consulta must be a non-empty string")
    @property
    def urgencia (self):
      return self._urgencia
     
    @urgencia.setter
    def urgencia(self, value:str):
      if isinstance(value, str) and len(value) > 0:
         self._urgencia = value
      else:
         raise ValueError("urgencia must be a non-empty string")
      
    @property
    def tiempo_estimado(self):
        return self._tiempo_estimado
    
    @tiempo_estimado.setter
    def tiempo_estimado(self, value:int):
      if isinstance(value, int) and value >= 0:
         self._tiempo_estimado = value
      else:
         raise ValueError("tiempo_estimado must be a positive integer")

    

    def __str__(self):
        """
        Esta funcion devuelve una cadena de texto sobre los atributos de la clase Paciente.

        Returns
        ----------
        str: una cadena de texto sobre los atributos de la clase.
           
        """
        return f"{self.IDPac}, {self.tipo_consulta}, {self.urgencia}, {self.tiempo_estimado}, {self.tiempo_llegada}, {self.tiempo_entrada_consulta}, {self.priorizacion}"
        