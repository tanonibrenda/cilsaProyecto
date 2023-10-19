# app.py
import os
from flask import Flask, render_template, request, render_template

from flask import send_file

from app.controllers.archivo_controller import (
      
     obtener_archivos_creados, descargar_archivo,
     
   
     guardar_informacion_en_txt, guardar_informacion_en_word,
    
)


app = Flask(__name__)

@app.route("/")
def principal():
    return render_template('index.html')

@app.route("/proyecto", methods=['GET', 'POST'])
def proyecto():
    nombre_archivo = None  
    if request.method == 'POST':
        informacion = request.form.get('informacion')
        tipo_archivo = request.form.get('tipo_archivo')

        if tipo_archivo == 'bloc_notas':
            nombre_archivo = guardar_informacion_en_txt(informacion)
        elif tipo_archivo == 'word':
            nombre_archivo = guardar_informacion_en_word(informacion)

    return render_template('proyecto.html', nombre_archivo=nombre_archivo)


@app.route("/ver_informacion/<archivo>")
def ver_informacion(archivo):
    # Ruta fija para los archivos (ajusta según tu estructura de directorios)
    carpeta_archivos = os.path.join(app.root_path, 'archivos')
    
    # Obtén la ruta completa del archivo
    ruta_archivo = os.path.join(carpeta_archivos, archivo)

    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, 'rb') as file:
            informacion = file.read()

        # Imprime la ruta del archivo en la consola de Flask
        app.logger.info("Ruta del archivo: %s", ruta_archivo)

        return send_file(ruta_archivo, as_attachment=True)
    else:
        app.logger.error("¡El archivo no existe! Ruta: %s", ruta_archivo)
        return "Archivo no encontrado"
    
@app.route("/archivos_creados")
def archivos_creados():
    archivos = obtener_archivos_creados()
    # Puedes renderizar una plantilla de Flask o devolver la lista de archivos en algún formato
    return render_template('archivos_creados.html', archivos=archivos)

@app.route("/descargar_archivo/<archivo>")
def descargar(archivo):
    return descargar_archivo(archivo)


@app.route("/desafios")
def desafios():
    return render_template('desafios.html')

@app.route("/mirutadevida")
def mirutadevida():
    return render_template('mirutadevida.html')

@app.route("/contacto")
def contacto():
    return render_template('contacto.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5050)
