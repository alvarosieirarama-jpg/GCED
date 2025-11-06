from unit import Unit, Archer, Infantry, Cavalry, Worker
from abc import ABC

class Civilization(ABC):
    """
    Se crea la clase abstracta trainer
    Incluira diferentes atributos definidos en las siguientes partes del código.
    A continuación introducimos los métodos principales:

    Métodos
    ------------
    select_first_unit(self):
       Esta función define la selección del primer unit de un entrenador

    all_debilitated(self)
        Función que comprueba si todos los units de un entrenador están debilitados

    __str__():
        Devuelve una representacion en formato cadena del objeto Unit

    select_next_unit(p:'Unit'):
        Función que define la selección del siguiente unit de un entrenador
    """

    def __init__(self, name, resources, units):
        """
        Esta es la función constructora de los objetos de la clase

        Parámetros
        ---------------
        name : str
            Representa el nombre del unit
        unit: list
            Representa la lista de units del entrenador

        Returns
        ---------------
        None.
        """
        self._name = name
        self._resources = resources
        self._units = units

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def resources(self):
        return self._resources

    @resources.setter
    def resources(self, value):
        self._resources = value

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        self._units.append(value)

    def train_unit(self, unit_type: str) -> Unit:
        """

        Returns
        ---------------
        Unit: devuelve un unit
            Si la vida del unit es mayor a 0 se devuelve un unit

        """
        i = 0
        if unit_type == 'Worker':
            resources_need = 30
        else:
            resources_need = 60
        if self.resources > resources_need:
            for unit in self.units:
                if unit.name.startswith(unit_type.lower()):
                    i +=1

            if unit_type == 'Archer':
                unit = Archer(f'archer_{i}',7,2,15,15,3)
                self.resources -= 60
            elif unit_type == 'Infantry':
                unit = Infantry(f'infantry_{i}',3,2,25,25,3)
                self.resources -= 60
            elif unit_type == 'Cavalry':
                unit = Cavalry(f'cavalry_{i}',5,2,25,25,5)
                self.resources -= 60
            else:
                unit = Worker(f'worker_{i}',1,0,5,5)
                self.resources -= 30

            self.units.append(unit)
            return unit

    def all_debilitated(self) -> bool:
        """

        Returns
        -----------------
        bool: comprueba si todos los unit están debilitados
        Si no lo están devuelve false, en cualquier otro caso devuelve true

        """
        for unit in self.units:
            if unit.hp > 0:
                return False
        return True # Con True se entiende que están todos debilitados.

    def collect_resources(self) -> None:
        """

        Parametros
        -----------------
        p : Unit
            Es la lista de los unit del entrenador

        Return
        ----------------
        Unit: devuelve el siguiente unit de la lista
        Por medio de los atributos effectiveness y agility de los unit
        decide cual va a ser el siguiente unit para entrar en la batalla

        """
        for unit in self.units:
            if isinstance(unit, Worker): # Con esta función se filtran los worker.
                self.resources += 10
