#from linked_ordered_positional_list import LinkedOrderedPositionalList as ListaOrdenada
from array_ordered_positional_list import ArrayOrderedPositionalList as ListaOrdenada
from inventario import Pieza
from catalogo import Inventario, Catalogo

def read_orders(catalogo, inventario, path="pedidos.txt"):
    """
    Lee un archivo de pedidos y procesa cada orden verificando la disponibilidad
    del modelo en el catálogo. Si está disponible, se realiza el pedido.

    Parámetros:
    
    catalogo : Catalogo
        Objeto que contiene los modelos disponibles.
    inventario : Inventario
        Objeto que gestiona las piezas disponibles.
    path : str, opcional
        Ruta al archivo de pedidos, por defecto "pedidos.txt".
    """
    with open(path, encoding="utf-8") as f:
        for l in f.readlines():
            ls = l.strip().split(",")
            customer, model_name = ls[0], ls[1]
            print(f"Nuevo pedido: {model_name} - {customer}")
            disponible = catalogo.buscar_modelo(model_name)
            if disponible:
                catalogo.realizar_pedido(model_name, inventario)
        inventario.reordenar_piezas()

def read_parts(path="piezas.txt"):
    """
    Lee un archivo de piezas y construye un objeto Inventario con las piezas leídas.

    Parámetros:
    
    path : str, opcional
        Si no se introduce ningún texto se leerá el archivo modelos.txt .

    Returns:
    
    Inventario
        Objeto con las piezas leídas del archivo.
    """
    inventario = Inventario()
    with open(path, encoding="utf-8") as f:
        for l in f.readlines():
            ls = l.strip().split(",")
            part_name, qty = ls[0], int(ls[1])
            pieza = Pieza(part_name, qty)
            inventario.añadir_pieza(pieza)
        return inventario 

def read_models(path="modelos.txt"):
    """
    Lee un archivo de modelos y construye un objeto Catalogo con los modelos y
    las piezas asociadas.

    Parámetros:
    
    path : str, opcional
        Si no se introduce ningún texto se leerá el archivo modelos.txt .

    Returns:
    
    Catalogo
        Contiene los modelos y sus piezas asociadas leídas del archivo.
    """
    with open(path, encoding="utf-8") as f:
        catalogo = Catalogo()
        for l in f.readlines():
            ls = l.strip().split(",")
            model_name, part_name, qty = ls[0], ls[1], int(ls[2])
            pieza = Pieza(part_name, qty)
            # Añadir al catálogo el modelo y la pieza
            catalogo.añadir_modelo(model_name, pieza)
        return catalogo

			
if __name__ == "__main__":
    inventario = read_parts()
    inventario.print_inventario()
    catalogo = read_models()
    catalogo.print_catalogo() 
    read_orders(catalogo,inventario)
    inventario.print_inventario()
    catalogo.print_catalogo()
    

            