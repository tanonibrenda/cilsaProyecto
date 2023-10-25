# app.py
import os
import csv
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

# Función para cargar los datos desde el archivo CSV
def cargar_datos(archivo):
    with open(archivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)
    



# Función para calcular la cantidad de votos totales por partido
def calcular_votos_totales(datos):
    votos_totales = {}

    for persona in datos:
        partido = persona.get('Partido', 'Sin Partido')
        votos_totales[partido] = votos_totales.get(partido, 0) + 1

    return votos_totales

#Funcion para calcular votos por partido
def calcular_votos_por_partido(datos):
    votos_por_partido = {'partido1': [], 'partido2': [], 'partido3': []}

    for persona in datos:
        partido = persona.get('Partido')
        if partido in votos_por_partido:
            votos_por_partido[partido].append(persona)

    return votos_por_partido

# Función para filtrar personas por DNI y nombre
def filtrar_personas(datos, dni_limite, nombre):
    return [persona for persona in datos if int(persona['DNI']) > dni_limite and persona['Nombre'] == nombre]

# Función para guardar en un archivo de texto personas con apellido "Gonzalez"
def guardar_gonzalez(datos):
    with open('gonzalez.txt', 'w', encoding='utf-8') as file:
        for persona in datos:
            if persona['Apellido'] == 'Gonzalez':
                file.write(f"{persona['Nombre']} {persona['Apellido']}\n")

@app.route("/")
def principal():
    return render_template('index.html')

@app.route("/proyecto")
def proyecto():
    # Tarea 1: Calcular y mostrar la cantidad de votos totales por partido
    # Cargar los datos desde el archivo CSV (votos.csv)
    archivo_csv = 'votos.csv'
    datos_votos = cargar_datos(archivo_csv)

    # Calcular la cantidad de votos totales por partido
    votos_totales = calcular_votos_totales(datos_votos)

    # Imprimir en la consola para verificar
    print("Votos totales por partido:", votos_totales)
    
    #Calcular votos por partido
    votos_por_partido = calcular_votos_por_partido(datos_votos)
    print("Votos por Partido: ", votos_por_partido)
    
    
    
    # Tarea 2: Mostrar personas con DNI mayor a 40,000,000 y nombre "Juan"
    personas_juan = filtrar_personas(datos_votos, 40000000, 'Juan')

    # Tarea 3: Guardar en un archivo de texto las personas con apellido "Gonzalez"
    personas_gonzalez = [persona for persona in datos_votos if persona['Apellido'] == 'Gonzalez']
    guardar_gonzalez(personas_gonzalez)

   

    return render_template('proyecto.html', 
                           total_votos=len(datos_votos),
                           votos_totales=votos_totales,
                           votos_por_partido=votos_por_partido, 
                           personas_juan=personas_juan, 
                           personas_gonzalez=personas_gonzalez,
                           )

# Rutas a páginas accesorias
@app.route("/integrantes")
def integrantes():
    return render_template('integrantes.html')

@app.route("/contacto")
def contacto():
    return render_template('contacto.html')

if __name__ == "__main__":
    # Cargar los datos desde el archivo CSV al iniciar la aplicación
    archivo_csv = 'votos.csv'
    datos_votos = cargar_datos(archivo_csv)
    
    app.run(debug=True, host='0.0.0.0', port=5050)
