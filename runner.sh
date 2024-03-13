# !/bin/bash

# Script que ejecuta la conversión de JSON a ICS usando el formato CNF como punto intermedio.
# El script recibe un archivo JSON como argumento y genera un archivo ICS con el mismo nombre.

# Uso: ./runner.sh <archivo JSON>
# Ejemplo: ./runner.sh test.json

# Verifica que la cantidad de argumentos sea la correcta.
if [ $# -ne 1 ]; then
    echo -e "\033[91;1mError:\033[0m Cantidad de argumentos incorrecta."
    echo -e "\033[93;1mUso:\033[0m ./runner.sh <archivo JSON>"
    exit 1
fi

# Verifica que el archivo JSON exista.
if [ ! -f $1 ]; then
    echo -e "\033[91;1mError:\033[0m El archivo $1 no existe."
    exit 1
fi

# Verifica que el archivo JSON tenga extensión .json.
if [[ $1 != *.json ]]; then
    echo -e "\033[91;1mError:\033[0m El archivo $1 no tiene extensión .json."
    exit 1
fi

# Verificamos si las librerias de requirements.txt estan instaladas
printf "\033[93;1mVerificando librerías...\033[0m\n"
# Declaramos un contador para la barra de progreso
N=0
LIBS=$(wc -l < requirements.txt)
while read -r line; do
    PACKAGE=$(echo $line | cut -d'=' -f1)
    if ! pip show -q $PACKAGE; then
        echo -e "\033[93;1mInstalando librería:\033[0m $PACKAGE"
        pip install $PACKAGE
    fi
    N=$((N+1))
    # Barra de progreso
    # La barra de progreso tiene el formato: [=====    ] 50%
    printf "\r["
    for ((i=0; i < $((N*10/LIBS)); i++)); do printf "\033[93;1m=\033[0m"; done
    for ((i=$N; i < $((LIBS/10)); i++)); do printf " "; done
    printf "] %d%%" $((N*100/LIBS))
done < requirements.txt
printf "\n\n"

# Revisamos si el solver esta compilado. En caso de que no lo este, 
# hacemos make en la carpeta glucose-4.2.1/simp
if [ ! -f glucose-4.2.1/simp/glucose ]; then
    printf "\033[93;1mCompilando solver...\033[0m\n"
    make -C glucose-4.2.1/simp
    printf "\033[92;1mCompletado!\033[0m\n"
fi

# Ejecutar la conversión de JSON a ICS.
echo -e "\033[93;1mConvirtiendo JSON a ICS...\033[0m"
python3 main.py $1