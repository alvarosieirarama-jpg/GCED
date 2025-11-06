from abc import ABC, abstractmethod
from math import floor

class Unit(ABC):
    """
    Clase abstracta que representa una unidad genérica en el juego.
    Las subclases de esta clase deben implementar el método `effectiveness`.

    Atributos:
        _name (str): El nombre de la unidad.
        _strength (int): La fuerza de ataque de la unidad.
        _defense (int): La defensa de la unidad.
        _hp (int): Los puntos de salud actuales de la unidad.
        _total_hp (int): Los puntos de salud totales de la unidad.
        _unit_type (str): El tipo de unidad (Archer, Cavalry, Infantry o Worker).
    """

    def __init__(self, name, strength, defense, hp, total_hp, unit_type):
        """
        Inicializa una nueva unidad con los atributos dados.

        Atributos:
            name (str): El nombre de la unidad.
            strength (int): La fuerza de ataque de la unidad.
            defense (int): La defensa de la unidad.
            hp (int): Los puntos de salud actuales de la unidad.
            total_hp (int): Los puntos de salud totales de la unidad.
            unit_type (str): El tipo de unidad.
        """
        self._name = name
        self._strength = strength
        self._defense = defense
        self._hp = hp
        self._total_hp = total_hp
        self._unit_type = unit_type

    def attack(self, opponent: "Unit") -> int:
        """
        Realiza un ataque a otra unidad. Reduce los puntos de salud del oponente.

        Argumento:
            opponent (Unit): La unidad oponente a la que se atacará.

        Returns:
            int: El daño realizado en el ataque.
        """
        daño = 1
        opponent.hp = max(0, opponent.hp - daño) # Esto se hace para evitar los números negativos
        return daño

    def is_debilitated(self) -> bool:
        """
        Verifica si la unidad está debilitada (sin puntos de salud).

        Returns:
            bool: True si la unidad tiene 0 puntos de salud, False en caso contrario.
        """
        if self.hp == 0:
            return True # Con True se entiende que está debilitado.
        else:
            return False

    @abstractmethod
    def effectiveness(self, opponent: "Unit") -> int:
        """
        Método abstracto que determina la efectividad del ataque de esta unidad sobre otra unidad.
        Este método debe ser implementado por las subclases.

        Argumento:
            opponent (Unit): La unidad oponente a la que se evaluará la efectividad.

        Returns:
            int: Un valor que indica la efectividad (positivo, negativo o neutro).
        """
        pass # Es una instrucción de control que nos permite dejar la función vacía.

    def __str__(self):
        """
        Retorna una cadena que representa los atributos de la unidad.

        Returns:
            str: Una descripción detallada de la unidad, incluyendo nombre, tipo, fuerza, defensa, y salud.
        """
        return f"{self.name} ({self.unit_type}) Stats: ATT: {self.strength}, DEF: {self.defense}, HP:{self.hp}/{self.total_hp}"    

    # Métodos para propiedades y validaciones (name, strength, defense, etc.)

    @property 
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if isinstance(value, str) and len(value) > 0:
            self._name = value
        else:
            raise ValueError("Name must be a non-empty string") # Lanza manualmente una excepción

    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, value: int):
        if isinstance(value, int) and value >= 0:
            self._strength = value
        else:
            raise ValueError("Strength must be a non-negative integer")

    @property
    def defense(self):
        return self._defense

    @defense.setter
    def defense(self, value: int):
        if isinstance(value, int) and value >= 0:
            self._defense = value
        else:
            raise ValueError("Defense must be a non-negative integer")

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value: int):
        if isinstance(value, int) and value >= 0:
            self._hp = value
        else:
            self._hp = 0


    @property
    def total_hp(self):
        return self._total_hp

    @total_hp.setter
    def total_hp(self, value: int):
        if isinstance(value, int) and value >= 0:
            self._total_hp = value
        else:
            raise ValueError("Total health points must be a non-negative integer")

    @property
    def unit_type(self):
        return self._unit_type

    @unit_type.setter
    def unit_type(self, value: str):
        if isinstance(value, str) and len(value) > 0:
            self._unit_type = value
        else:
            raise ValueError("Unit type must be a non-empty string")


class Archer(Unit):
    """
    Subclase que representa una unidad de tipo arquero.

    Atributos:
        _arrows (int): Número de flechas disponibles para el ataque.
    """
    def __init__(self, name, strength, defense, hp, total_hp, arrows):
        """
        Inicializa una nueva unidad de tipo arquero.

        Argumentos:
            name (str): Nombre de la unidad.
            strength (int): Fuerza de ataque.
            defense (int): Defensa de la unidad.
            hp (int): Puntos de salud.
            total_hp (int): Puntos de salud máximos.
            arrows (int): Número de flechas disponibles para el ataque.
        """
        super().__init__(name=name, strength=strength, defense=defense, hp=hp, total_hp=total_hp, unit_type="Archer")
        self._arrows = arrows

    @property
    def arrows(self):
        return self._arrows

    @arrows.setter
    def arrows(self, value=5):
        if isinstance(value, int):
            self._arrows = value
        else:
            raise ValueError("Arrows must be an integer value")

    def effectiveness(self, p: Unit) -> int:
        """
        Determina la efectividad de un arquero contra otras unidades.

        Argumento:
            p (Unit): La unidad opuesta.

        Returns:
            int: Valor de efectividad contra la unidad.
        """
        if isinstance(p, Cavalry):
            return 1
        elif isinstance(p, Infantry):
            return -1
        else:
            return 0

    def attack(self, p: Unit) -> int:
        """
        Realiza un ataque con flecha a una unidad.

        Argumento:
            p (Unit): La unidad a la que se atacará.

        Returns:
            int: El daño realizado en el ataque.
        """
        if isinstance(p, Cavalry): # 
            factor = 1.5
        elif isinstance(p, Infantry):
            factor = 0.5
        else:
            factor = 1

        if self.arrows > 0:
            daño = max(1, floor(factor * self.strength) - p.defense)
            self.arrows -= 1
        else:
            daño = 1

        p.hp = max(0, p.hp - daño)
        return daño


class Cavalry(Unit):
    """
    Subclase que representa una unidad de tipo caballería.

    Atributos:
        _charge (float): El poder de carga de la unidad de caballería.
    """
    def __init__(self, name, strength, defense, hp, total_hp, charge):
        """
        Inicializa una nueva unidad de tipo caballería.

        Argumentos:
            name (str): Nombre de la unidad.
            strength (int): Fuerza de ataque.
            defense (int): Defensa de la unidad.
            hp (int): Puntos de salud.
            total_hp (int): Puntos de salud máximos.
            charge (float): Poder de carga de la unidad.
        """
        super().__init__(name=name, strength=strength, defense=defense, hp=hp, total_hp=total_hp, unit_type="Cavalry")
        self._charge = float(charge)

    @property
    def charge(self):
        return self._charge

    @charge.setter
    def charge(self, value=5):
        if isinstance(value, int):
            self._charge = value
        else:
            raise ValueError("Charge must be a float value")

    def effectiveness(self, p: 'Unit') -> int:
        """
        Determina la efectividad de la caballería contra otras unidades.

        Argumentos:
            p (Unit): La unidad opuesta.

        Returns:
            int: Valor de efectividad contra la unidad.
        """
        if isinstance(p, Infantry):
            return 1
        elif isinstance(p, Archer):
            return -1
        else:
            return 0

    def attack(self, p: Unit) -> int:
        """
        Realiza un ataque de carga contra una unidad.

        Argumentos:
            p (Unit): La unidad a la que se atacará.

        Returns:
            int: El daño realizado en el ataque.
        """
        if isinstance(p, Archer):
            factor = 0.5
        elif isinstance(p, Infantry):
            factor = 1.5
        else:
            factor = 1

        daño = max(1, floor(self.charge + factor * self.strength) - p.defense)
        p.hp = max(0, p.hp - daño)
        return daño


class Infantry(Unit):
    """
    Subclase que representa una unidad de infantería.

    Atributos:
        _fury (float): El nivel de furia de la unidad de infantería.
    """
    def __init__(self, name, strength, defense, hp, total_hp, fury):
        """
        Inicializa una nueva unidad de infantería.

        Argumentos:
            name (str): Nombre de la unidad.
            strength (int): Fuerza de ataque.
            defense (int): Defensa de la unidad.
            hp (int): Puntos de salud.
            total_hp (int): Puntos de salud máximos.
            fury (float): El poder de furia de la unidad.
        """
        super().__init__(name=name, strength=strength, defense=defense, hp=hp, total_hp=total_hp, unit_type="Infantry")
        self._fury = float(fury)

    @property
    def fury(self):
        return self._fury

    @fury.setter
    def fury(self, value=3):
        if isinstance(value, int):
            self._fury = value
        else:
            raise ValueError("Fury must be an integer value")

    def effectiveness(self, p: Unit) -> int:
        """
        Determina la efectividad de la infantería contra otras unidades.

        Argumento:
            p (Unit): La unidad opuesta.

        Returns:
            int: Valor de efectividad contra la unidad.
        """
        if isinstance(p, Archer):
            return 1
        elif isinstance(p, Cavalry):
            return -1
        else:
            return 0

    def attack(self, p: Unit) -> int:
        """
        Realiza un ataque de infantería contra una unidad.

        Argumento:
            p (Unit): La unidad a la que se atacará.

        Returns:
            int: El daño realizado en el ataque.
        """
        if isinstance(p, Cavalry):
            factor = 0.5
        elif isinstance(p, Archer):
            factor = 1.5
        else:
            factor = 1

        daño = max(1, floor(self.fury + factor * self.strength) - p.defense)
        p.hp = max(0, p.hp - daño)
        return daño


class Worker(Unit):
    """
    Subclase que representa una unidad de trabajo.

    Los trabajadores no tienen poder de ataque pero pueden reparar unidades aliadas.
    """

    def __init__(self, name, strength, defense, hp, total_hp):
        """
        Inicializa una nueva unidad de tipo trabajador.

        Arumentos:
            name (str): Nombre de la unidad.
            strength (int): Fuerza de ataque (aunque no se usa en combate).
            defense (int): Defensa de la unidad.
            hp (int): Puntos de salud.
            total_hp (int): Puntos de salud máximos.
        """
        super().__init__(name=name, strength=strength, defense=defense, hp=hp, total_hp=total_hp, unit_type="Worker")

    def effectiveness(self, p: Unit) -> int:
        """
        Los trabajadores no afectan a otras unidades en combate.

        Argumento:
            p (Unit): La unidad opuesta.

        Returns:
            int: Siempre devuelve -1, ya que no son efectivos en combate.
        """
        return -1

    def collect(self) -> int:
        """
        Los trabajadores recolectan recursos.

        Returns:
            int: Siempre devuelve 10 como cantidad de recursos recolectados.
        """
        return 10
