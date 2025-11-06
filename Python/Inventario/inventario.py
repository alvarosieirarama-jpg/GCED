
class Pieza:
    """
    Clase que representa una pieza con un nombre y una cantidad.
    
    Atributos:
    
    nombre_pieza : str
        Nombre identificador de la pieza.
    cantidad : int
        Cantidad disponible de la pieza.
    """

    def __init__(self, nombre_pieza, cantidad):
        """
        Inicializa una instancia de la clase Pieza.

        Parámetros;
        
        nombre_pieza : str
            Nombre de la pieza.
        cantidad : int
            Cantidad de la pieza.
        """
        self.nombre_pieza = nombre_pieza
        self.cantidad = cantidad

    @property
    def nombre_pieza(self):
        """
        Getter para obtener el nombre de la pieza.

        Returns:
        
        str
            El nombre de la pieza.
        """
        return self._nombre_pieza
        
    @nombre_pieza.setter
    def nombre_pieza(self, value:str):
        """
        Setter para establecer el nombre de la pieza.

        Parámetros:
        
        value : str
            Nuevo nombre para la pieza.

        Raises:
        
        ValueError
            Si el valor no es una cadena.
        """
        if isinstance(value, str):
            self._nombre_pieza = value
        else:
            raise ValueError("pieza must be a non-empty str")

    @property
    def cantidad(self):
        """
        Getter para obtener la cantidad de la pieza.

        Returns:
       
        int
            Cantidad disponible de la pieza.
        """
        return self._cantidad
        
    @cantidad.setter
    def cantidad(self, value:int):
        """
        Setter para establecer la cantidad de la pieza.

        Parámetros:
       
        value : int
            Nueva cantidad de la pieza.

        Raises:
       
        ValueError
            Si el valor no es un entero.
        """
        if isinstance(value, int):
            self._cantidad = value
        else:
            raise ValueError("titulo must be an integer")
        
    def __str__(self):
        """
        Devuelve una representación en cadena del objeto Pieza.

        Returns:
        
        str
        """
        return f"Pieza(pieza={self.nombre_pieza}, cantidad={self.cantidad})"
    
    def __gt__(self, pieza):
        """
        Compara si la cantidad de esta pieza es mayor que la de otra.

        Parámetros:
        
        pieza : Pieza
            Otra instancia de la clase Pieza.

        Returns:
        
        bool
            True si esta pieza tiene mayor cantidad que la otra.
        """
        if self.cantidad > pieza.cantidad:
            return True

    def __eq__(self, pieza):
        """
        Compara si el nombre de esta pieza es igual al de otra.

        Parámetros:
        
        pieza : Pieza
            Otra instancia de la clase Pieza.

        Returns:
       
        bool
            True si los nombres de las piezas son iguales.
        """
        if self.nombre_pieza == pieza.nombre_pieza:
            return True

    def __ge__ (self, pieza):
        """
        Compara si la cantidad de esta pieza es mayor o igual que la de otra.

        Parámetros:
        
        pieza : Pieza
            Otra instancia de la clase Pieza.

        Returns:
       
        bool
            True si esta pieza tiene mayor o igual cantidad que la otra.
        """
        if self.cantidad >= pieza.cantidad:
            return True
