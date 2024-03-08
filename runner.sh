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
while read -r line; do
    PACKAGE=$(echo $line | cut -d'=' -f1)
    if ! pip show -q $PACKAGE; then
        echo -e "\033[93;1mInstalando librería:\033[0m $PACKAGE"
        pip install $PACKAGE
    fi
done < requirements.txt

# TODO: Ejecutar la conversión de JSON a ICS.
echo -e "\033[93;1mConvirtiendo JSON a ICS...\033[0m"