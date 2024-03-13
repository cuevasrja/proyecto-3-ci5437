import json
import math
import sys
import os
from typing import List
from datetime import datetime
from modules.cnf_maker import *
from modules.ics_converter import *

def main():
    # Obtener el archivo JSON
    file = sys.argv[1]
    print(f"Abriendo el archivo \033[92;1m{file}\033[0m...")

    # intentar abrir el archivo JSON
    try:
        with open(file, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"\033[91;1mERROR:\033[0m No existe el archivo {file}.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(
            f"\033[91;1mERROR:\033[0m Hay un problema con la forma en que formatea los datos JSON en el archivo {file}."
        )
        sys.exit(1)

    # guardar los datos en variables
    # nombre del torneo
    t_name = data["tournament_name"]
    # fecha de inicio del torneo
    start_date = data["start_date"]
    # fecha final del torneo
    end_date = data["end_date"]
    # hora de inicio de los juegos en cada dia
    start_time = data["start_time"]
    # hora final de los juegos en cada dia
    end_time = data["end_time"]
    # participantes
    participants = data["participants"]

    # obtenemos los siguientes datos
    # cantidad de participantes
    n = len(data["participants"])

    # el numero de participantes debe ser al menos 2, para que pueda ocurrir al menos un partido en el torneo
    if n < 2:
        print("\033[91;1mERROR:\033[0m El torneo debe tener al menos 2 participantes.")
        sys.exit(1)

    # cantidad de dias que durara el torneo
    days = (
        (datetime.strptime(end_date, "%Y-%m-%d"))
        - datetime.strptime(start_date, "%Y-%m-%d")
    ).days + 1

    # cantidad de horas que durara el torneo
    hora1 = datetime.strptime(start_time, "%H:%M:%S.%f").time()
    hora2 = datetime.strptime(end_time, "%H:%M:%S.%f").time()
    # Calcular la diferencia en horas
    diff_hours = (
        datetime.combine(datetime.min, hora2) - datetime.combine(datetime.min, hora1)
    ).total_seconds() // 3600
    hours = int(diff_hours)

    # verificar si los dias y horas son suficientes para que cada equipo compita
    # ademas, cada equipo juega 2*(n-1) veces, entonces debe haber al menos 2*(n-1) dias
    if not (
        days >= 2 * (n - 1) and hours >= 2 and days * (hours // 2) >= n * (n - 1)
    ):
        print(
            "\033[91;1mERROR:\033[0m No hay suficientes dias y horas para planear las fechas de los partidos del torneo."
        )
        sys.exit(1)

    print(f" - Nombre del torneo: \033[92;1m'{t_name}'\033[0m")
    print(f" - Participantes: \033[92;1m{', '.join(participants)}\033[0m")
    print(f" - El torneo durara \033[92;1m{days}\033[0m dias")
    print(f" - Con \033[92;1m{hours}\033[0m horas por dia\n")

    # traducir las restricciones a formato DIMACS
    todimacs(n, days, hours, file)
    print("Archivo de restricciones en formato DIMACS creado \033[92;1mexitosamente!\033[0m")

    # Ejecutar el solver
    print("\nResolviendo el problema...\n")
    # TODO: Cuando se ejecute el solver, mandar la salida a un archivo con > {file.name.replace('.json', '_result.txt')}
    os.system(f"./glucose-4.2.1/simp/glucose -model {file.name.replace('.json', '.cnf')}")


if __name__ == "__main__":
    main()
