import sys
from unit import Unit, Archer, Cavalry, Infantry, Worker
from civilization import Civilization
import pandas as pd


def unit_counter(civilization:object, obj:object) -> int:
    """
    Cuenta cuántas unidades de un tipo específico hay en una civilización.

    Parámetros:
    civilization (object): La civilización que contiene las unidades.
    obj (object): El tipo de unidad que se desea contar.

    Returns:
    int: El número de unidades del tipo especificado en la civilización.
    """
    cnt_unit = 0
    for unit in civilization.units:
        if isinstance(unit, obj):
            cnt_unit +=1
    return cnt_unit

def print_phase1_report(civilization):
    """
    Imprime un reporte de la fase 1 de la civilización, mostrando los recursos
    y los tipos de unidades.

    Parámetros:
    civilization (object): La civilización para la cual se genera el reporte.
    """
    def unit_report(civilization, unit_type):
        """
        Crea un informe de las unidades de un tipo específico en la civilización.

        Parámetros:
        civilization (object): La civilización que contiene las unidades.
        unit_type (object): El tipo de unidad que se desea incluir en el informe.

        Returns:
        str: Una cadena que contiene todas las unidades de ese tipo.
        """
        units = [str(unit) for unit in civilization.units if isinstance(unit, unit_type)]
        return ', '.join(units)

    report = f"""
----------------------------------------
{civilization.name} Resources: {civilization.resources}
Worker : {unit_report(civilization, Worker)}
Archer : {unit_report(civilization, Archer)}
Cavalry : {unit_report(civilization, Cavalry)}
Infantry : {unit_report(civilization, Infantry)}
"""
    print(report)


def print_phase2_production(civilization, resources, N):
    """
    Imprime un reporte de la fase 2 de la civilización, mostrando la producción de unidades
    en función de los recursos disponibles.

    Parámetros:
    civilization (object): La civilización que está produciendo unidades.
    resources (int): Los recursos disponibles para crear unidades.
    N (int): El número de turno actual.
    """
    def unit_creation_report(civilization, resources, N):
        """
        Determina si la civilización puede crear una nueva unidad, según los recursos disponibles.

        Parámetros:
        civilization (object): La civilización que puede crear una unidad.
        resources (int): Los recursos disponibles.
        N (int): El número de turno actual.

        Returns:
        str: El reporte de la unidad creada o un mensaje indicando que no se puede crear ninguna unidad.
        """
        if N % 4 == 3:
            resources_need = 30
        else:
            resources_need = 60
        
        if resources > resources_need:
            unit = civilization.units[-1]  # Última unidad creada
            return str(unit)
        else:
            return f"{civilization.name} cannot create any unit right now."

    report = f"""
----------------------------------------
    {unit_creation_report(civilization,resources,N)}
"""
    print(report)


def select_worker_alive(civilization):
    """
    Selecciona un trabajador (worker) vivo de la civilización.

    Parámetros:
    civilization (object): La civilización para la cual se busca un trabajador vivo.

    Returns:
    object: El trabajador vivo seleccionado, o None si no se encuentra ninguno.
    """
    for unit in civilization.units:
        if unit.is_debilitated() == False and isinstance(unit, Worker):
            return unit
    return None

def select_first_unit_alive(civilization):
    """
    Selecciona la primera unidad no debilitada de la civilización, priorizando las unidades que no son trabajadores.

    Parámetros:
    civilization (object): La civilización para la cual se selecciona una unidad.

    Returns:
    object: La unidad seleccionada, ya sea un trabajador o una unidad no trabajadora.
    """
    for unit in civilization.units:
        if unit.is_debilitated() == False and not isinstance(unit, Worker):
            return unit
    return select_worker_alive(civilization)


def select_opponent_alive(civilization, soldier):
    """
    Selecciona un oponente vivo de la civilización que pueda ser atacado por el soldado.

    Parámetros:
    civilization (object): La civilización del oponente.
    soldier (object): El soldado que busca un oponente.

    Returns:
    object: El oponente seleccionado.
    """
    # Solo se consideran las unidades no trabajadores primero
    military_units = [unit for unit in civilization.units if unit.is_debilitated() == False and not isinstance(unit, Worker)]
    
    # Si no hay unidades militares, se seleccionan los trabajadores
    if not military_units:
        return select_worker_alive(civilization)
    
    # Prioridad 1: Unidades donde el atacante tiene ventaja (+1 de efectividad)
    for unit in military_units:
        if soldier.effectiveness(unit) == 1:
            return unit
    
    # Prioridad 2: Unidades donde el atacante tiene efectividad neutral (0)
    for unit in military_units:
        if soldier.effectiveness(unit) == 0:
            return unit
    
    # Prioridad 3: Unidades donde el atacante tiene desventaja (-1 de efectividad)
    for unit in military_units:
        if soldier.effectiveness(unit) == -1:
            return unit
    
    # Esto no debería ocurrir si military_units no está vacío
    return None
            


def attack(attacker, civilization_attacked):
    """
    Realiza un ataque de un atacante a una civilización atacada y retorna el daño causado.

    Parámetros:
    attacker (object): La unidad atacante.
    civilization_attacked (object): La civilización que está siendo atacada.

    Returns:
    tuple: El atacante, el objetivo y el daño causado.
    """
    target = select_opponent_alive(civilization_attacked, attacker)
    if attacker is None or target is None:
        return None
    damage = attacker.attack(target)
    return (attacker, target, damage)

def all_soldiers_debilitated(civilization):
    """
    Verifica si todos los soldados de una civilización están debilitados.

    Parámetros:
    civilization (object): La civilización a verificar.

    Returns:
    bool: True si todos los soldados están debilitados, False de lo contrario.
    """
    for unit in civilization.units:
        if unit.is_debilitated == False and not isinstance(unit, Worker):
            return False
    return True

def print_phase3_battle(civilization1, civilization2, battle_data, N):
    """
    Imprime el reporte de la fase 3 del combate entre dos civilizaciones.

    Parámetros:
    civilization1 (object): La primera civilización.
    civilization2 (object): La segunda civilización.
    battle_data (list): Los datos de la batalla a ser registrados.
    N (int): El número de turno actual.
    """
    print(f"\nFase 3: Estado de la Batalla")
    print("----------------------------------------")
    print("Ataques alternos (Cremallera)")
    
    # Preparar los atacantes de ambas civilizaciones (unidades no trabajadores con hp > 0)
    attackers1 = [unit for unit in civilization1.units if unit.hp > 0 and not isinstance(unit, Worker)]
    attackers2 = [unit for unit in civilization2.units if unit.hp > 0 and not isinstance(unit, Worker)]
    
    # Si todas las unidades militares están derrotadas, usar trabajadores
    if not attackers1 and any(unit.hp > 0 and isinstance(unit, Worker) for unit in civilization1.units):
        attackers1 = [unit for unit in civilization1.units if unit.hp > 0 and isinstance(unit, Worker)]
    
    if not attackers2 and any(unit.hp > 0 and isinstance(unit, Worker) for unit in civilization2.units):
        attackers2 = [unit for unit in civilization2.units if unit.hp > 0 and isinstance(unit, Worker)]
    
    # Batalla en patrón de cremallera
    i = 0
    while i < len(attackers1) and i < len(attackers2):
        # La civilización 1 ataca
        attacker = attackers1[i]
        result = attack(attacker, civilization2)
        if result:
            attacker, target, damage = result
            print(f"{civilization1.name} - {attacker} ataca a {civilization2.name} - {target} con daño {damage} (hp={target.hp}/{target.total_hp}).")
            if target.hp <= 0:
                print(f"{target} ha sido derrotado.")
            
            # Registrar datos de la batalla: (número_turno, civilización_atacante, id_atacante, tipo_atacante, civilización_objetivo, id_objetivo, tipo_objetivo, daño)
            battle_data.append((
                N,  # Número de turno actual
                civilization1.name,
                attacker.name,
                attacker.__class__.__name__,
                civilization2.name,
                target.name,
                target.__class__.__name__,
                damage
            ))
        
        # La civilización 2 ataca
        attacker = attackers2[i]
        result = attack(attacker, civilization1)
        if result:
            attacker, target, damage = result
            print(f"{civilization2.name} - {attacker} ataca a {civilization1.name} - {target} con daño {damage} (hp={target.hp}/{target.total_hp}).")
            if target.hp <= 0:
                print(f"{target} ha sido derrotado.")
            
            # Registrar datos de la batalla
            battle_data.append(( 
                N,  # Número de turno actual
                civilization2.name,
                attacker.name,
                attacker.__class__.__name__,
                civilization1.name,
                target.name,
                target.__class__.__name__,
                damage
            ))
        
        i += 1
    
    # Si la civilización 1 tiene más atacantes, continúan atacando
    if i < len(attackers1):
        print("#Fin de la secuencia alterna: Una civilización no tiene más atacantes")
        print(f"#Las unidades restantes de la civilización más fuerte (por ejemplo, {civilization1.name}) ahora atacan en secuencia")
        
        for j in range(i, len(attackers1)):
            attacker = attackers1[j]
            result = attack(attacker, civilization2)
            if result:
                attacker, target, damage = result
                print(f"{civilization1.name} - {attacker} ataca a {civilization2.name} - {target} con daño {damage} (hp={target.hp}/{target.total_hp}).")
                if target.hp <= 0:
                    print(f"{target} ha sido derrotado.")
                
                # Registrar datos de la batalla
                battle_data.append




if __name__ == "__main__":

    # Leer el archivo de configuración desde la línea de comandos o usar el predeterminado
    config_file = sys.argv[1] if len(sys.argv) > 1 else "battle1.txt"

    # Intentar abrir el archivo especificado
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: El archivo '{config_file}' no existe.", file=sys.stderr)
        sys.exit(1)

    # Resto del código de la simulación...
    print(f"Leyendo configuración desde: {config_file}")

    civ1_data = lines[0].split(":")
    civ1_name = civ1_data[0]
    resources1 = int(civ1_data[1])
    
    civ2_data = lines[1].split(":")
    civ2_name = civ2_data[0]
    resources2 = int(civ2_data[1])
    
    turns_line = lines[2]
    parts = turns_line.replace(":", ",").split(",")
    turns = int(parts[1].strip())

    # Leer la cantidad inicial de cada tipo de unidad
    workers_line = lines[3]
    workers = int(workers_line.split(":")[1].strip())

    archers_line = lines[4]
    archers = int(archers_line.split(":")[1].strip())

    cavalry_line = lines[5]
    cavalry = int(cavalry_line.split(":")[1].strip())

    infantry_line = lines[6]
    infantry = int(infantry_line.split(":")[1].strip())

    # Crear instancias de civilización
    units1 = []
    units2= []
    civilization1 = Civilization(civ1_name, resources1, units1)
    print (f"[TODO: Create civilization: {civ1_name} with {resources1} initial resources]")
    civilization2 = Civilization(civ2_name, resources2, units2)
    print (f"[TODO: Create civilization: {civ2_name} with {resources2} initial resources]")

    # Crear unidades según la cantidad especificada en el fichero de batalla escogido
    for _ in range(workers):
        civilization1.train_unit('Worker')
        civilization2.train_unit('Worker')
    workers1 = unit_counter(civilization1, Worker)
    workers2 = unit_counter(civilization2, Worker)

    print (f"[TODO: Create {workers1} workers for {civ1_name}]")
    print (f"[TODO: Create {workers2} workers for {civ2_name}]")
    
    for _ in range(archers):
        civilization1.train_unit('Archer')
        civilization2.train_unit('Archer')
    archers1 = unit_counter(civilization1, Archer)
    archers2 = unit_counter(civilization2, Archer)

    print (f"[TODO: Create {archers1} archers for {civ1_name}]")
    print (f"[TODO: Create {archers2} archers for {civ2_name}]")

    for _ in range(cavalry):
        civilization1.train_unit('Cavalry')
        civilization2.train_unit('Cavalry')
    cavalry1 = unit_counter(civilization1, Cavalry)
    cavalry2 = unit_counter(civilization2, Cavalry)

    print (f"[TODO: Create {cavalry1} cavalry for {civ1_name}]")
    print (f"[TODO: Create {cavalry2} cavalry for {civ2_name}]")

    for _ in range(infantry):
        civilization1.train_unit('Infantry')
        civilization2.train_unit('Infantry')
    infantry1 = unit_counter(civilization1, Infantry)
    infantry2 = unit_counter(civilization2, Infantry)

    print (f"[TODO: Create {infantry1} infantry for {civ1_name}]")
    print (f"[TODO: Create {infantry2} infantry for {civ2_name}]")

    battle_list = []

    for N in range(turns):
        civilization1.collect_resources()
        civilization2.collect_resources()

        print(f' TURN {N} PHASE 1 REPORT')
        print_phase1_report(civilization1)
        print_phase1_report(civilization2)

        resources1 = civilization1.resources
        resources2 = civilization2.resources

        if N % 4 == 0:
            civilization1.train_unit('Archer')
            civilization2.train_unit('Archer')
        elif N % 4 == 1:
            civilization1.train_unit('Cavalry')
            civilization2.train_unit('Cavalry')
        elif N % 4 == 2:
            civilization1.train_unit('Infantry')
            civilization2.train_unit('Infantry')
        else:
            civilization1.train_unit('Worker')
            civilization2.train_unit('Worker')

        print(f' TURN {N} PHASE 2 PRODUCTION')
        print_phase2_production(civilization1, resources1, N)
        print_phase2_production(civilization2, resources2, N)

        # Simulación de ataque
        attacker_1 = select_first_unit_alive(civilization1)
        attacker_2 = select_first_unit_alive(civilization2)
        print_phase3_battle(civilization1, civilization2, battle_list, N)
    # print_statistics(battle_list)

    data = pd.DataFrame(battle_list, columns=['Turn', 'AttackerCiv', 'AttackerName', 'AttackerType', 'TargetCiv', 'TargetName', 'TargetType', 'Damage'])
    print(data)

    group_col = ["AttackerName", "AttackerCiv"]
    target_col = "Damage"
    data_pandas1 = data.groupby(group_col).agg({target_col :["mean"]})
    print ("##############################")
    print ("   Daño agrupado por unidad      ")
    print ("##############################\n")
    print (data_pandas1)

    group_col = ["AttackerType", "AttackerCiv"]
    target_col = "Damage"
    data_pandas2 = data.groupby(group_col).agg({target_col :["mean"]})
    print ("##################################")
    print (" Daño agrupado por tipo de unidad      ")
    print ("##################################\n")
    print (data_pandas2)

    group_col = ["AttackerType", "AttackerCiv", "TargetType"]
    target_col = "Damage"
    data_pandas3 = data.groupby(group_col).agg({target_col :["mean"]})
    print ("##################################################")
    print (" Daño agrupado por tipo de unidad a los otros tipos      ")
    print ("##################################################\n")
    print (data_pandas3)

                  



    

    