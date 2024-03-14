import json
import math
import sys
import os
from typing import List
from datetime import datetime
from optilog.solvers.sat import Glucose41
from modules.cnf_maker import *
from modules.ics_converter import *
from modules.time_converter import *

def main():
    time_start: datetime = datetime.now()
    # Obtener el archivo JSON
    file: str = sys.argv[1]
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
    t_name: str = data["tournament_name"]
    # fecha de inicio del torneo
    start_date: str = data["start_date"]
    # fecha final del torneo
    end_date: str = data["end_date"]
    # hora de inicio de los juegos en cada dia
    start_time: str = data["start_time"]
    # hora final de los juegos en cada dia
    end_time: str = data["end_time"]
    # participantes
    participants: List[str] = data["participants"]

    # obtenemos los siguientes datos
    # cantidad de participantes
    n: int = len(data["participants"])

    # el numero de participantes debe ser al menos 2, para que pueda ocurrir al menos un partido en el torneo
    if n < 2:
        print("\033[91;1mERROR:\033[0m El torneo debe tener al menos 2 participantes.")
        sys.exit(1)

    # cantidad de dias que durara el torneo
    days: int = diff_days(start_date, end_date)

    # Calcular la diferencia en horas
    hours: int = diff_hours(start_time, end_time)

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
    cnf_file: str = todimacs(n, days, hours, file)
    print("Archivo de restricciones en formato DIMACS creado \033[92;1mexitosamente!\033[0m")

    # Ejecutar el solver
    print("\nResolviendo el problema...\n")
    solver: Glucose41 = Glucose41()
    if solver.load_cnf(cnf_file) and solver.solve():
        model: List[int] = solver.model()
        if all(n <= 0 for n in model):
            print("\033[91;1mERROR:\033[0m No hay solucion para el problema.")
            sys.exit(1)
        else:
            print("\033[92;1mEl problema ha sido resuelto exitosamente!\033[0m")
            print("Las variables que son verdaderas son:")
            positivas = [i for i in model if i > 0]
            print(positivas)
    model: List[int] = solver.model()
    # Convertir las variables a formato ICS
    print("\nConvirtiendo las variables a formato ICS...")
    make_ics(data, model)

    # Calcular el tiempo que tomo resolver el problema
    time_end: datetime = datetime.now()
    time_taken: str = str(time_end - time_start)
    print(f"\nTiempo que tomo resolver el problema: \033[92;1m{time_taken}\033[0m")

    # Escribimos en el archivo times.txt el tiempo que tomo resolver el problema con el nombre del archivo
    os.system(f"echo '{file.name}\t{time_taken}' >> times.txt")


if __name__ == "__main__":
    main()
