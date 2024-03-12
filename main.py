import json
import math
import sys
from typing import List
from datetime import datetime


# enumeraremos las variables de 0 a 2*n*days*hours-1
# y lo almacenaremos en una tabla de 4 dimensiones
# cada columna corresponde al numero del participante, el tipo de juego (local o visitante), el dia y la hora
def table_variables(n, days, hours):
    variable = 0
    table = []
    for i in range(n):
        table.append([])
        for j in range(2):
            table[i].append([])
            for k in range(days):
                table[i][j].append([])
                for l in range(hours):
                    table[i][j][k].append(variable)
                    variable += 1
    return table


# obtener el numero total de clausulas para las 4 restricciones
def get_number_clauses(n, days, hours):
    c1 = (
        int(math.factorial(n) / (2 * math.factorial(n - 2)))
        * days
        * (days - 1)
        * hours
        * hours
        * 11
    )
    c2 = n * (n - 1) * 4 * days * (2 * hours - 1) + n * 2 * days * (2 * hours - 1)
    c3 = 2 * hours * n * days + hours * (hours - 1) * 2 * n * days
    c4 = 2 * hours * hours * n * (days - 1)
    return c1 + c2 + c3 + c4


# restriccion 1 a CNF
# todos los participantes deben jugar dos veces con cada uno de los otros participantes
# una como "visitantes" y la otra como "locales".
def c1(filename, table, n, days, hours):
    file = open(filename, "a")
    matched = [[False] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if x != y and not matched[x][y]:
                matched[x][y] = True
                matched[y][x] = True
                for d1 in range(days):
                    for d2 in range(days):
                        if d1 == d2:
                            continue
                        for h1 in range(hours):
                            for h2 in range(hours):
                                # primera clausula
                                p = table[x][0][d1][h1]
                                file.write(f"{p} 0\n")
                                # segunda clausula
                                q = table[x][1][d2][h2]
                                file.write(f"{q} 0\n")

                                a = table[y][0][d1][h1]
                                b = table[y][1][d2][h2]
                                c = table[y][1][d1][h1]
                                d = table[y][0][d2][h2]

                                # clausula 3 (a∨b∨c∨d)
                                file.write(f"{a} {b} {c} {d} 0\n")
                                # clausula 4 (a∨b∨c∨¬d)
                                file.write(f"{a} {b} {c} {-d} 0\n")
                                # clausula 5 (a∨b∨¬c∨d)
                                file.write(f"{a} {b} {-c} {d} 0\n")
                                # clausula 6 (a∨¬b∨c∨d)
                                file.write(f"{a} {-b} {c} {d} 0\n")
                                # clausula 7 (a∨¬b∨c∨¬d)
                                file.write(f"{a} {-b} {c} {-d} 0\n")
                                # clausula 8 (a∨¬b∨¬c∨d)
                                file.write(f"{a} {-b} {-c} {d} 0\n")
                                # clausula 9 (¬a∨b∨c∨d)
                                file.write(f"{-a} {b} {c} {d} 0\n")
                                # clausula 10 (¬a∨b∨c∨¬d)
                                file.write(f"{-a} {b} {c} {-d} 0\n")
                                # clausula 11 (¬a∨b∨¬c∨d)
                                file.write(f"{-a} {b} {-c} {d} 0\n")
    file.flush()


# restriccion 2 a CNF
# Dos juegos no pueden ocurrir al mismo tiempo
def c2(filename, table, n, days, hours):
    file = open(filename, "a")
    for a in range(n):
        for x in range(n):
            if a != x:
                for t1 in range(2):
                    for t2 in range(2):
                        for d in range(days):
                            for h in range(hours):
                                file.write(
                                    f"{-table[a][t1][d][h]} {-table[x][t2][d][h]} 0\n"
                                )
                                if h + 1 < hours:
                                    file.write(
                                        f"{-table[a][t1][d][h]} {-table[x][t2][d][h+1]} 0\n"
                                    )

    for t1 in range(2):
        for t2 in range(2):
            if t1 != t2:
                for a in range(n):
                    for d in range(days):
                        for h in range(hours):
                            file.write(
                                f"{-table[a][t1][d][h]} {-table[x][t2][d][h]} 0\n"
                            )
                            if h + 1 < hours:
                                file.write(
                                    f"{-table[a][t1][d][h]} {-table[x][t2][d][h+1]} 0\n"
                                )
    file.flush()


# restriccion 3 a CNF
# Un participante puede jugar a lo sumo una vez por dia
def c3(filename, table, n, days, hours):
    file = open(filename, "a")

    for t1 in range(2):
        for t2 in range(2):
            if t1 != t2:
                for h in range(hours):
                    for a in range(n):
                        for d in range(days):
                            file.write(
                                f"{-table[a][t1][d][h]} {-table[a][t2][d][h]} 0\n"
                            )

    for h1 in range(hours):
        for h2 in range(hours):
            if h1 != h2:
                for t in range(2):
                    for a in range(n):
                        for d in range(days):
                            file.write(
                                f"{-table[a][t][d][h1]} {-table[a][t][d][h2]} 0\n"
                            )
    file.flush()


# restriccion 4 a CNF:
# Un participante no puede jugar de "visitante" en dos dias consecutivos, ni de "local" dos dias seguidos
def c4(filename, table, n, days, hours):
    file = open(filename, "a")

    for d in range(days):
        if d + 1 < days:
            for a in range(n):
                for t in range(2):
                    for h1 in range(hours):
                        p = table[a][t][d][h1]
                        for h2 in range(hours):
                            file.write(f"{-p} {-table[a][t][d+1][h2]} 0\n")
    file.flush()


# traducir restricciones a formato dimacs
def todimacs(n, days, hours, filename):
    # restamos horas menos 1, pues el ultimo partido de un dia no puede comenzar a la hora final
    hours = hours - 1

    # numero de variables en total
    number_of_variables = 2 * n * days * hours
    # creamos la tabla de variables
    table = table_variables(n, days, hours)

    # calculamos el numero total de clausulas
    number_of_clauses = get_number_clauses(n, days, hours)
    # nombre del archivo de salida
    outputCointraints = "contraints.cnf"

    # escribimos las clausulas en el archivo de salida
    f = open(outputCointraints, "w")
    f.write(f"p cnf {number_of_variables} {number_of_clauses}\n")
    f.flush()
    c1(outputCointraints, table, n, days, hours)
    c2(outputCointraints, table, n, days, hours)
    c3(outputCointraints, table, n, days, hours)
    c4(outputCointraints, table, n, days, hours)

    return outputCointraints


def main():
    file = "data.json"

    # intentar abrir el archivo JSON
    try:
        with open(file, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"ERROR! No existe el archivo {file}.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(
            f"ERROR! Hay un problema con la forma en que formatea los datos JSON en el archivo {file}."
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
        print("ERROR! El torneo debe tener al menos 2 participantes.")
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
        days >= 2 * (n - 1) and hours >= 2 and days * (hours // 2) >= 2 * n * (n - 1)
    ):
        print(
            "ERROR! No hay suficientes dias y horas para planear las fechas de los partidos del torneo."
        )
        sys.exit(1)

    print(f" - Nombre del torneo: '{t_name}'")
    print(f" - Participantes: {', '.join(participants)}")
    print(f" - El torneo durara {days} dias")
    print(f" - Con {hours} horas por dia\n")

    # traducir las restricciones a formato DIMACS
    todimacs(n, days, hours, file)
    print("Archivo de restricciones en formato DIMACS creado exitosamente!")


if __name__ == "__main__":
    main()
