# !/bin/bash

# Script que ejecuta la conversión de JSON a ICS usando el formato CNF como punto intermedio.
# El script recibe un archivo JSON como argumento y genera un archivo ICS con el mismo nombre.

# Uso: ./runner.sh <archivo JSON>
# Ejemplo: ./runner.sh test.json

# Verifica que la cantidad de argumentos sea la correcta. (Mayor o igual a 1) $# < 1
if [ $# -lt 1 ]; then
    echo -e "\033[91;1mError:\033[0m Cantidad de argumentos incorrecta."
    echo -e "\033[93;1mUso:\033[0m ./runner.sh <archivo JSON> <archivo JSON> ... <archivo JSON>"
    exit 1
fi

FILES=$@

# Verifica que cada archivo exista.
for FILE in $FILES; do
    if [ ! -f $FILE ]; then
        echo -e "\033[91;1mError:\033[0m El archivo $FILE no existe."
        exit 1
    fi
done

# Verifica que los archivos sean de tipo JSON.
for FILE in $FILES; do
    if [[ $FILE != *.json ]]; then
        echo -e "\033[91;1mError:\033[0m El archivo $FILE no es de tipo JSON."
        exit 1
    fi
done

FILE_TIME="times.txt"
# Verificamos si el archivo de tiempos no existe, si no existe, lo creamos.
if [ ! -f $FILE_TIME ]; then
    echo -e "Archivo\t Convertir a DIMCAS\t Resolver SAT\tTiempo Total\tSatisfacible" > $FILE_TIME
fi

# Verificamos si las librerias de requirements.txt estan instaladas
printf "\033[93;1mVerificando librerías...\033[0m\n"
# Declaramos un contador para la barra de progreso
N=0
LIBS=$(wc -l < requirements.txt)
while read -r line; do
    # Obtenemos el nombre de la librería. El formato es: <nombre>==<versión>
    PACKAGE=$(echo $line | cut -d'=' -f1)
    if ! pip3 show $PACKAGE > /dev/null 2>&1; then
        printf "\033[93;1mInstalando:\033[0m $PACKAGE\n"
        pip3 install $line > /dev/null 2>&1
    fi
    N=$((N+1))
    # Barra de progreso
    # La barra de progreso tiene el formato: [=====    ] 50%
    printf "["
    for ((i=0; i < $((N*10/LIBS)); i++)); do printf "\033[92;1m=\033[0m"; done
    for ((i=$N; i < $((LIBS/10)); i++)); do printf " "; done
    printf "] %d%%\r" $((N*100/LIBS))
done < requirements.txt
echo -e "\n"

# Ejecutar la conversión de JSON a ICS para cada archivo.
echo -e "\033[93;1mConvirtiendo JSON a ICS...\033[0m"
# Si solo es un archivo, no se imprime el nombre del archivo
if [ $# -eq 1 ]; then
    printf "\033[93;1mConvirtiendo:\033[0m $FILES\n"
    python3 main.py $FILES
else
    N_FILES=$#
    N=0
    for FILE in $FILES; do
        printf "["
        for ((i=0; i < $((N*10/N_FILES)); i++)); do printf "\033[92;1m=\033[0m"; done
        printf "\033[92;1m>\033[0m"
        printf "] %d%%\r" $((N*100/N_FILES))
        python3 main.py $FILE
        # Eliminamos el archivo .cnf
	    rm -f $(echo $FILE | sed 's/.json/.cnf/')
        N=$((N+1))
    done
    printf "["
    for ((i=0; i < $((N*10/N_FILES)); i++)); do printf "\033[92;1m=\033[0m"; done
    printf "] %d%%\r" $((N*100/N_FILES))
    echo -e "\n"
fi
echo -e "El tiempo de ejecución de cada archivo se encuentra en el archivo \033[93;1m$FILE_TIME\033[0m."
