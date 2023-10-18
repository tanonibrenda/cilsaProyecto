# app.py
import os
from flask import Flask, render_template, request, render_template

from app.controllers.archivo_controller import (
    guardar_informacion, obtener_archivos_creados, 
    guardar_informacion_en_txt, guardar_informacion_en_word, 
    descargar_archivo
)


app = Flask(__name__)

@app.route("/")
def principal():
    return render_template('index.html')

@app.route("/proyecto", methods=['GET', 'POST'])
def proyecto():
    nombre_archivo = None  
    if request.method == 'POST':
        # Obtener datos del formulario
        informacion = request.form.get('informacion')
        tipo_archivo = request.form.get('tipo_archivo')

        if tipo_archivo == 'bloc_notas':
            # Guardar información en un archivo de texto (.txt)
            nombre_archivo = guardar_informacion_en_txt(informacion)
        elif tipo_archivo == 'word':
            # Guardar información en un archivo Word (.docx)
            nombre_archivo = guardar_informacion_en_word(informacion)

    return render_template('proyecto.html', nombre_archivo=nombre_archivo)


@app.route("/ver_informacion/<archivo>")
def ver_informacion(archivo):
    # Obtén la ruta completa del archivo
    ruta_archivo = os.path.join(app.root_path, archivo)

    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, 'r') as file:
            informacion = file.read()
        return render_template('ver_informacion.html', informacion=informacion)
    else:
        return "Archivo no encontrado"
    
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
