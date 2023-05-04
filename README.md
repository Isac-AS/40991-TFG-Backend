-[Introducción](#Introducción)

-[Setup](#Setup)

-[Ejecución](#Ejecución)

# 1. Introducción
Este respositorio se corresponde con la aplicación Python-Flask empleada para la gestión y lógica el sistema de gestión de registros 
médicos procesados con inteligencia artifical.

# 2. Setup
## 2.1. Instalar haciendo uso del fichero docker-compose.yml
Es un requisito necesario en indispensable tener instalado docker. La instalación a través de este método no requiere el clonado del repositorio.
Es suficiente con copiar el fichero "docker-compose.yml", situarlo en un directorio conveniente y ejecutar el comando:
~~~
docker compose up
~~~

## 2.2. Instalación manual
La instalación manual es completada ejecutando el comando:

~~~
git clone https://github.com/Isac-AS/40991-TFG-Backend.git
~~~

# 3. Ejecución
Existen tres modos de ejecución disponible haciendo uso de los ficheros ".bash" visibles en el directorio. En consecuencia, es necesario estar
en un entorno Linux o sobre un intérprete bash. Asegúrese que los ficheros tienen permisos de ejecución.

La ejecución se realiza con cualquiera de los siguientes comandos:
~~~
./bootstrap_prod.bash
./bootstrap.bash
./run_tests.bash
~~~

## 3.1 Modo producción
El modo producción ejecuta la aplicación Flask de tal manera que si se realizan cambios en los ficheros, no se reinicia el servidor.

## 3.2 Modo desarrollo
El modo desarrollo reinicia el servidor al realizar cambios en los ficheros bajo el directorio `./src/`. Esto es conveniente para realizar
cambios sin tener que reiniciar la aplicación manualmente.

## 3.3 Ejecución de tests
La ejecución de los tests no es interactiva. Se procede a ejecutar los tests, según la configuación establecida.