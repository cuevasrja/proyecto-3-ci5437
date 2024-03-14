from typing import List
import json
import sys
import ics
from modules.time_converter import *
from modules.cnf_maker import table_variables

def make_ics(json_data: dict, model: List[int]) -> None:
    """
    Esta funcion toma la tabla de asignaciones de partidos y la convierte en un archivo .ics
    """
    # Obtenemos los datos del archivo JSON
    # nombre del torneo
    t_name: str = json_data["tournament_name"]
    # fecha de inicio del torneo
    start_date: str = json_data["start_date"]
    # hora de inicio de los juegos en cada dia
    start_time: str = json_data["start_time"]
    # participantes
    participants: List[str] = json_data["participants"]
    # Fecha de fin del torneo
    end_date: str = json_data["end_date"]
    # hora final de los juegos en cada dia
    end_time: str = json_data["end_time"]

    # Obtenemos los siguientes datos
    # Cantidad de participantes
    n: int = len(json_data["participants"])
    # Cantidad de dias que durara el torneo
    days: int = diff_days(start_date, end_date)
    # Calcular la diferencia en horas
    hours: int = diff_hours(start_time, end_time)

    # Obtener la tabla de variables
    table: List[List[List[List[int]]]] = table_variables(n, days, hours-1)

    # Crear un nuevo calendario
    c: ics.Calendar = ics.Calendar()

    # Crear un evento para cada partido
    for a in range(n):
        for b in range(n):
            if a == b:
                continue
            for d in range(days):
                for h in range(hours-1):
                    if model[table[a][b][d][h] - 1] > 0:
                        # Crear el evento
                        e: ics.Event = ics.Event()
                        e.name = f"{participants[a]} vs {participants[b]}"
                        # Calcular la fecha y hora del evento segun el indice de la tabla de variables
                        # Inicio del evento
                        e_date: str = calc_day(start_date, d)
                        e_start_time: str = calc_time(start_time, h)
                        e.begin = f"{e_date} {e_start_time}"
                        # Fin del evento
                        e_end_time: str = calc_time(e_start_time, 2)
                        e.end = f"{e_date} {e_end_time}"
                        # Agregar el evento al calendario
                        c.events.add(e)
                        print(f"Se ha creado el evento {e.name} el {e_date} a las {e_start_time}.")
                        print(f"El evento {e.name} termina a las {e_end_time}.\n")

    # Creamos el archivo .ics
    try:
        with open(f"{t_name}.ics", "r") as file:
            print(f"\033[93;1mWARNING:\033[0m El archivo {t_name}.ics ya existe, se sobreescribira.")
    except FileNotFoundError:
        # Si el archivo no existe, lo creamos
        with open(f"{t_name}.ics", "w") as file:
            file.writelines(c)
    print(f"Se ha creado el archivo {t_name}.ics")

