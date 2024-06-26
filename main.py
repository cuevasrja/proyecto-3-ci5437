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
    solved: bool = True
    total_time_start: datetime = datetime.now()
    print("\n👋 \033[92;1m¡Bienvenido al Planificador de Torneos!\033[0m\n")

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
        solved = False

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
        solved = False

    print(f" - Nombre del torneo: \033[92;1m'{t_name}'\033[0m")
    print(f" - Participantes: \033[92;1m{', '.join(participants)}\033[0m")
    print(f" - El torneo durara \033[92;1m{days}\033[0m dias")
    print(f" - Con \033[92;1m{hours}\033[0m horas por dia")
    print(f" - Se van a jugar \033[92;1m{n * (n - 1)}\033[0m partidos en total\n")

    time_start: datetime = datetime.now()
    # traducir las restricciones a formato DIMACS
    cnf_file: str 
    if solved:
        cnf_file = todimacs(n, days, hours, file)
    print("Archivo de restricciones en formato DIMACS creado \033[92;1mexitosamente!\033[0m")

    # imprimir tiempo en que toma en traducir las restricciones a formato DIMACS
    time_end: datetime = datetime.now()
    time_taken_1: str = str(time_end - time_start)
    print(f"\n⌛ Tiempo que tomo en convertir las restricciones en formato DIMACS: \033[92;1m{time_taken_1}\033[0m")

    # Ejecutar el solver
    print("\n\033[1;33mResolviendo el problema...\033[0m\n")
    time_start: datetime = datetime.now()
    solver: Glucose41 = Glucose41()
    if solved:
        solver.load_cnf(cnf_file)

    if solved and solver.solve():
        model: List[int] = solver.model()
        if all(n <= 0 for n in model):
            print("\033[91;1mERROR:\033[0m No hay solucion para el problema.")
            solved = False
    else:
        print("\033[91;1mERROR:\033[0m No se pudo resolver el problema.")
        solved = False
    if solved:
        print("\033[92;1mEl problema ha sido resuelto exitosamente!\033[0m")
    # Calcular el tiempo que tomo resolver el problema SAT
    time_end: datetime = datetime.now()
    time_taken_2: str = str(time_end - time_start)

    print(f"\n⌛ Tiempo que tomo Glucose en resolver el problema: \033[92;1m{time_taken_2}\033[0m")
    model: List[int]
    if solved:
        model = solver.model()
        # Convertir las variables a formato ICS
        print("\n\033[1;33mConvirtiendo las variables a formato ICS...\033[0m\n")
        make_ics(data, model)

    time_end: datetime = datetime.now()
    total_time: str = str(time_end - total_time_start)
    print(f"\n⌛ Tiempo total que toma en resolver el problema: \033[92;1m{total_time}\033[0m\n")

    result: str = "SAT" if solved else "UNSAT"
    # Escribimos en el archivo times.txt el tiempo que tomo resolver el problema con el nombre del archivo
    os.system(f"echo '{file.name}\t{time_taken_1}\t{time_taken_2}\t{total_time}\t{result}' >> times.txt")

    return


if __name__ == "__main__":
    main()
