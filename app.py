# app.py

#1era parte importar bibliotecas y frameworks, luego ser instalados

#se importa csv para poder leer este tipo de archivo 
import csv

#se importa panda para mejor gestion de la información 
import pandas as pd

#de flask se importa flask para manejo de archivo, y render_template para poder mostrar en la pagina web

from flask import Flask, render_template

#cache es para el almacenamiento temporal de información, por ejemplo como cuando se cuenta la cantidad total de votantes
from flask_caching import Cache

#crea una instancia de la clase Flask que representa una aplicación web. Esta instancia, usualmente llamada app, se utiliza para configurar y ejecutar tu aplicación Flask. Puedes definir rutas, vistas, configuraciones y otros aspectos de tu aplicación utilizando esta instancia.
app = Flask(__name__)

#en esta linea usando cache se usa para que la información manipulada no realice un almacenamiento real, sino uno transito. El real en este proyecto se guarda en el archivo gonzalez.txt
cache = Cache(app, config={'CACHE_TYPE': 'null'})

#utilizar la biblioteca Pandas para leer un archivo CSV (Comma-Separated Values) llamado 'votos.csv' y cargar sus datos en un objeto DataFrame.
df = pd.read_csv('votos.csv')

# Función para cargar los datos desde el archivo CSV
def cargar_datos(archivo):
    try:
        # Intenta abrir el archivo CSV
        with open(archivo, newline='', encoding='utf-8') as csvfile:
             # Utiliza DictReader de csv para leer el archivo CSV y crear un diccionario para cada fila
            reader = csv.DictReader(csvfile)
            # Convierte el lector a una lista de diccionarios y devuelve esa lista
            return list(reader)
    except FileNotFoundError:
        # Captura una excepción si el archivo no se encuentra
        print(f"Error: El archivo {archivo} no se encuentra.")
        #Y retorna una lista vacia
        return []
    except Exception as e:
        # Captura cualquier otra excepción y muestra un mensaje de error
        print(f"Error al cargar los datos: {e}")
         #Y retorna una lista vacia
        return []

#función para calcular los votos totales. Primera parte del punto 1 del planteo
def calcular_votos_totales(datos):
    # Crear un diccionario para almacenar el recuento total de votos por partido
    votos_totales = {}
    
    # Iterar sobre cada persona en los datos
    for persona in datos:
        
        # Obtener el partido de la persona o establecer 'Sin Partido' si no hay información
        partido = persona.get('Partido', 'Sin Partido')
        
        # Actualizar el recuento de votos para el partido en el diccionario
        votos_totales[partido] = votos_totales.get(partido, 0) + 1
        
     # Imprimir el recuento total de votos por partido
    print("Votos totales por partido:", votos_totales)  
    
    # Devolver el diccionario con el recuento total de votos
    return votos_totales

# Funcion para calcular votos por partido
def calcular_votos_por_partido():
     # Inicializa un diccionario para almacenar el recuento de votos por partido
    votos_por_partido = {}

    # Itera sobre cada fila en el DataFrame df
    for _, fila in df.iterrows():
        # Obtiene el valor de la columna 'Voto' para la fila actual
        partido = fila['Voto']
        
        # Verifica si el partido ya está en el diccionario votos_por_partido
        if partido in votos_por_partido:
            # Si se incrementa el recuento de votos para ese partido
            votos_por_partido[partido] += 1
        else:
             # Si no, agrega el partido al diccionario con un recuento inicial de 1
            votos_por_partido[partido] = 1
     # Devuelve el diccionario con el recuento total de votos por partido
    return votos_por_partido

# Función para filtrar personas por DNI y nombre. Punto 2 
def filtrar_personas(datos, dni_limite, nombre):
     # Utiliza una lista  para filtrar las personas que cumplen con las condiciones datos, dni y nombre
    return [persona for persona in datos if int(persona['DNI']) > dni_limite and persona['Nombre'] == nombre]

# Función para guardar en un archivo de texto personas con apellido "Gonzalez". Punto 3
def guardar_gonzalez(datos):
    # Abre el archivo 'gonzalez.txt' en modo de escritura ('w') con codificación utf-8
    with open('gonzalez.txt', 'w', encoding='utf-8') as file:
        # Itera sobre cada persona en los datos
        for persona in datos:
             # Verifica si el apellido de la persona es 'Gonzalez'
            if persona['Apellido'] == 'Gonzalez':
                 # Escribe el nombre y apellido en el archivo, seguido de un salto de línea
                file.write(f"{persona['Nombre']} {persona['Apellido']}\n")

#se usa para almacenar temporalmente los resultados de una función y evitar tener que calcular esos resultados nuevamente si se llaman con los mismos parámetros. 
@cache.cached(timeout=0, key_prefix='index')

#usando Flask se renderiza una pagina web, en este caso la pagina index.html
@app.route("/")
def principal():
     cache.clear()
     return render_template('index.html')



#decorador de ruta que indica que la función, y ejecuta la funcion proyecto cuando se abre la pagina proyecto.html
@app.route("/proyecto")
#Define la función proyecto, que manejará las solicitudes a la ruta "/proyecto".
def proyecto():
    # Tarea 1: Calcular y mostrar la cantidad de votos totales por partido
    #
    # Cargar los datos desde el archivo CSV (votos.csv)
    #Se está calculando la cantidad de votos totales por partido y almacenando el resultado en votos_por_partido.
    # Calcular votos por partido utilizando la nueva función
    votos_por_partido = calcular_votos_por_partido()

    # Tarea 2: Mostrar personas con DNI mayor a 40,000,000 y nombre "Juan", Se están filtrando personas con DNI mayor a 40,000,000 y nombre "Juan" utilizando la función filtrar_personas(). El resultado se almacena en personas_juan.
    personas_juan = filtrar_personas(datos_votos, 40000000, 'Juan')

    # Tarea 3: Guardar en un archivo de texto las personas con apellido "Gonzalez". Se están filtrando personas con apellido "Gonzalez" utilizando una lista de comprensión y la condición persona['Apellido'] == 'Gonzalez'. Luego, se llama a la función guardar_gonzalez() para guardar estas personas en un archivo de texto.
    personas_gonzalez = [persona for persona in datos_votos if persona['Apellido'] == 'Gonzalez']
    guardar_gonzalez(personas_gonzalez)

    # Devolver la respuesta utilizando render_template. Devuelve el resultado renderizado utilizando la plantilla 'proyecto.html'. Los resultados de las tareas se pasan como variables a la plantilla para que puedan ser mostrados dinámicamente en la interfaz de usuario.
    return render_template('proyecto.html',
                           total_votos=len(datos_votos),
                           votos_por_partido=votos_por_partido,
                           personas_juan=personas_juan,
                           personas_gonzalez=personas_gonzalez)

# Rutas a páginas accesorias
@app.route("/integrantes")
def integrantes():
    return render_template('integrantes.html')

@app.route("/contacto")
def contacto():
    return render_template('contacto.html')

#el script se ejecuta directamente y no es importado
if __name__ == "__main__":
    
    # Cargar los datos desde el archivo CSV al iniciar la aplicación
    archivo_csv = 'votos.csv'
    
    #llama cargar_datos y para eso usa archivo csv
    datos_votos = cargar_datos(archivo_csv)
    
    #cache es para el almacenamiento temporal de información, por ejemplo como cuando se cuenta la cantidad total de votantes
    from flask_caching import Cache

#asocia Flask con app
    cache = Cache(app, config={'CACHE_TYPE': 'null'})

# inicia el servidor de desarrollo de Flask con la función run. Con debug que es para depurar, y configura el host y el puerto
    app.run(debug=True, host='0.0.0.0', port=5050)
