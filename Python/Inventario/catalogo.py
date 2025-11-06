#from linked_ordered_positional_list import LinkedOrderedPositionalList as ListaOrdenada
from array_ordered_positional_list import ArrayOrderedPositionalList as ListaOrdenada

class Inventario:
    
    def __init__(self):
        self.inventario = ListaOrdenada()
    def añadir_pieza(self, pieza):
        """
        Añade una pieza al inventario.
        
        Parameters:
        
        pieza : Pieza
            Objeto Pieza a añadir al inventario.
            
        Returns:
        
        None.
        """
        self.inventario.add(pieza)
   
    def print_inventario(self):
        """
        Imprime el inventario por pantalla en el formato especificado.
        
        Returns:
        
        None.
        """
        print("--------STOCK--------")
        piezas_str = " | ".join([f"{pieza.nombre_pieza}: {pieza.cantidad}" for pieza in self.inventario])
        print(piezas_str + " |")

    def eliminar_pieza(self, pieza, position):
        """
        Elimina una pieza del inventario.
        
        Parameters:
        
        pieza : Pieza
            Objeto Pieza a eliminar del inventario.
            
        Returns:
        
        None.
        """
        self.inventario.delete(position)
        print(f"Eliminada: Pieza {pieza.nombre_pieza}")

    def reordenar_piezas(self):
        position = self.inventario.first()
        lista = []
        while position != None:
            pieza = self.inventario.get_element(position)
            lista.append(pieza)
            position = self.inventario.after(position)
        self.inventario = ListaOrdenada()
        for pieza in lista:
            self.inventario.add(pieza)

    






class Catalogo:

    def __init__(self):
        self.catalogo = dict()

    def añadir_modelo(self, modelo, pieza):
        """
        Añade un modelo al catálogo.
        
        Parameters:
        
        modelo : str
            Nombre del modelo.
        pieza : str
            Nombre de la pieza.
            
        Returns:
        
        None.
        """
        if modelo not in self.catalogo:
            self.catalogo[modelo] = ListaOrdenada()
        self.catalogo[modelo].add(pieza)
    
    def print_catalogo(self):
        """
        Imprime el catálogo por pantalla en el formato especificado.
        
        Returns:
        
        None.
        """
        print("--------CATALOGO--------")
        for modelo, piezas in self.catalogo.items():
            piezas_str = " | ".join([f"{pieza.nombre_pieza}: {pieza.cantidad}" for pieza in piezas])
            print(f"<{modelo}>\n{piezas_str}")

    def buscar_modelo(self, modelo):
        """
        Busca un modelo en el catálogo.
        
        Parameters:
        
        modelo : str
            Nombre del modelo a buscar.
            
        Returns:
        
        bool
            True si el modelo existe en el catálogo, False en caso contrario.
        """
        if modelo not in self.catalogo:
            print(f"Pedido NO atendido. Modelo {modelo} fuera de catálogo.")
            return False
        else:
            print(f"<{modelo}>")
            for pieza in self.catalogo[modelo]:
                print(f"{pieza.nombre_pieza} - {pieza.cantidad}")
            print("\n")
            return True

    def comprobar_piezas(self, modelo, inventario):
        """
        Comprueba si las piezas de un modelo están disponibles en el inventario.
        
        Parameters:
        
        modelo : str
            Nombre del modelo a comprobar.
        inventario : Inventario
            Objeto Inventario para verificar la disponibilidad de piezas.
            
        Returns:
       
        bool
            True si todas las piezas están disponibles, False en caso contrario.
        """
        for pieza in self.catalogo[modelo]:
            position = inventario.inventario.first()
            pieza_existente = inventario.inventario.get_element(position)
            for _ in range(inventario.inventario.__len__()):
                if pieza_existente.nombre_pieza == pieza.nombre_pieza:
                    if pieza_existente.cantidad < pieza.cantidad:
                        return False
                else:
                    position = inventario.inventario.after(position)
                    pieza_existente = inventario.inventario.get_element(position)
        return True
    

    def eliminar_modelo(self, modelo):
        """
        Elimina un modelo del catálogo.
        
        Parameters:
       
        modelo : str
            Nombre del modelo a eliminar
        """
        if modelo in self.catalogo:
            del self.catalogo[modelo]
    
    def revision_modelos(self, pieza):
        lista = []
        for modelo, piezas in self.catalogo.items():
            position = piezas.first()
            pieza_existente = piezas.get_element(position)
            for _ in range(piezas.__len__()):
                if pieza_existente.nombre_pieza == pieza.nombre_pieza:
                    lista.append(modelo)
                else:
                    position = piezas.after(position)
                    pieza_existente = piezas.get_element(position)
        for modelo in lista:
            self.eliminar_modelo(modelo)
            print(f"Eliminado: Modelo {modelo} dependiente.")
        return True
    
    def gestion_excasez_piezas(self, modelo, inventario):
        """
        Gestiona la escasez de piezas en el inventario.
        
        Parameters:
       
        modelo : str
            Nombre del modelo a gestionar.
        inventario : Inventario
            Objeto Inventario para verificar la disponibilidad de piezas.
            
        Returns:
        
        None.
        """
        print(f"Pedido {modelo} NO atendido. Faltan:")
        for pieza in self.catalogo[modelo]:
            position = inventario.inventario.first()
            pieza_existente = inventario.inventario.get_element(position)
            for _ in range(inventario.inventario.__len__()):
                if pieza_existente.nombre_pieza == pieza.nombre_pieza:
                    if pieza_existente.cantidad < pieza.cantidad:
                        print(f"{pieza.nombre_pieza} - {pieza.cantidad - pieza_existente.cantidad}")
                else:
                    position = inventario.inventario.after(position)
                    pieza_existente = inventario.inventario.get_element(position)
        self.eliminar_modelo(modelo)
        print(f"Eliminado: {modelo}")

    
    def realizar_pedido(self, modelo, inventario):
        """
        Realiza un pedido de un modelo en el catálogo.
        
        Parameters:
        
        modelo : str
            Nombre del modelo a pedir.
        inventario : Inventario
            Objeto Inventario para verificar la disponibilidad de piezas.
            
        Returns:
       
        None.
        """
        if self.comprobar_piezas(modelo, inventario):
            print(f"Pedido atendido. Modelo {modelo} disponible.")
            for pieza in self.catalogo[modelo]:
                position = inventario.inventario.first()
                pieza_existente = inventario.inventario.get_element(position)
                for _ in range(inventario.inventario.__len__()):
                    if pieza_existente.nombre_pieza == pieza.nombre_pieza:
                        pieza_existente.cantidad -= pieza.cantidad
                        if pieza_existente.cantidad == 0:
                            inventario.eliminar_pieza(pieza,position)
                            self.revision_modelos(pieza)
                        break

                    else:
                        position = inventario.inventario.after(position)
                        pieza_existente = inventario.inventario.get_element(position)
        else:
            self.gestion_excasez_piezas(modelo, inventario)
            
    