class Paciente:
    """
    Clase que representa a un paciente con información personal y médica.

    Atributos:
        _DNI (str): Documento Nacional de Identidad del paciente.
        _nombre (str): Nombre completo del paciente.
        _sexo (str): Sexo del paciente.
        _edad (int): Edad del paciente.
        _diagnosticos (list): Lista de diagnósticos médicos del paciente.
        _alergias (list): Lista de alergias conocidas del paciente.
        _fecha_ultima_visita (str): Fecha de la última visita médica del paciente.
    """

    def __init__(self, DNI, nombre, sexo, edad, diagnosticos, alergias, fecha_ultima_visita):
        """
        Inicializa una nueva instancia de la clase Paciente.

        Args:
            DNI (str): Documento Nacional de Identidad.
            nombre (str): Nombre del paciente.
            sexo (str): Sexo del paciente.
            edad (int): Edad del paciente.
            diagnosticos (list): Diagnósticos médicos.
            alergias (list): Alergias del paciente.
            fecha_ultima_visita (str): Fecha de la última visita médica.
        """
        self._DNI = DNI
        self._nombre = nombre
        self._sexo = sexo
        self._edad = edad
        self._diagnosticos = diagnosticos
        self._alergias = alergias
        self._fecha_ultima_visita = fecha_ultima_visita

    @property
    def DNI(self):
        """str: Obtiene o establece el DNI del paciente."""
        return self._DNI

    @DNI.setter
    def DNI(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._DNI = value
        else:
            raise ValueError("DNI must be a non-empty str")

    @property
    def nombre(self):
        """str: Obtiene o establece el nombre del paciente."""
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._nombre = value
        else:
            raise ValueError("nombre must be a non-empty str")

    @property
    def sexo(self):
        """str: Obtiene o establece el sexo del paciente."""
        return self._sexo

    @sexo.setter
    def sexo(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._sexo = value
        else:
            raise ValueError("sexo must be a non-empty str")

    @property
    def edad(self):
        """int: Obtiene o establece la edad del paciente."""
        return self._edad

    @edad.setter
    def edad(self, value):
        if isinstance(value, int) and value > 0:
            self._edad = value
        else:
            raise ValueError("edad must be a positive int")

    @property
    def diagnosticos(self):
        """list: Obtiene o establece la lista de diagnósticos médicos del paciente."""
        return self._diagnosticos

    @diagnosticos.setter
    def diagnosticos(self, value):
        if isinstance(value, list):
            self._diagnosticos = value
        else:
            raise ValueError("diagnosticos must be a list")

    @property
    def alergias(self):
        """list: Obtiene o establece la lista de alergias del paciente."""
        return self._alergias

    @alergias.setter
    def alergias(self, value):
        if isinstance(value, list):
            self._alergias = value
        else:
            raise ValueError("alergias must be a list")

    @property
    def fecha_ultima_visita(self):
        """str: Obtiene o establece la fecha de la última visita médica del paciente."""
        return self._fecha_ultima_visita

    @fecha_ultima_visita.setter
    def fecha_ultima_visita(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._fecha_ultima_visita = value
        else:
            raise ValueError("fecha_ultima_visita must be a non-empty str")

    def __str__(self):
        """
        Devuelve una representación en cadena de la información del paciente.

        Returns:
            str: Representación del objeto Paciente.
        """
        return (f"Paciente(DNI={self._DNI}, nombre={self._nombre}, sexo={self._sexo}, edad={self._edad}, diagnosticos={self._diagnosticos},"
                f"alergias={self._alergias}, fecha_ultima_visita={self._fecha_ultima_visita})")

    def __gt__(self, curso):
        """
        Compara dos pacientes por su DNI (mayor que).

        Args:
            curso (Paciente): Otro objeto Paciente.

        Returns:
            bool: True si el DNI del paciente actual es mayor.
        """
        return self._DNI > curso._DNI

    def __eq__(self, curso):
        """
        Compara si dos pacientes tienen el mismo DNI.

        Args:
            curso (Paciente): Otro objeto Paciente.

        Returns:
            bool: True si los DNIs son iguales.
        """
        return self._DNI == curso._DNI
