
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def principal():
    return render_template('index.html')

@app.route("/desafios")
def desafios():
    return render_template('desafios.html')

@app.route("/proyecto", methods=['GET', 'POST'])
def proyecto():
    if request.method == 'POST':
        # Obtener datos del formulario
        informacion = request.form.get('informacion')

        # Guardar información en un archivo .txt
        with open('informacion.txt', 'a') as file:
            file.write(informacion + '\n')

    return render_template('proyecto.html')

@app.route("/ver_informacion")
def ver_informacion():
    with open('informacion.txt', 'r') as file:
        informacion = file.read()

    return render_template('ver_informacion.html', informacion=informacion)

@app.route("/mirutadevida")
def mirutadevida():
    return render_template('mirutadevida.html')

@app.route("/contacto")
def contacto():
    return render_template('contacto.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

