from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def principal():
    return render_template('index.html')

@app.route("/desafios")
def desafios():
    return render_template('desafios.html')

@app.route("/proyecto")
def proyecto():
    return render_template('proyecto.html')

@app.route("/mirutadevida")
def mirutadevida():
    return render_template('mirutadevida.html')

@app.route("/contacto")
def contacto():
    return render_template('contacto.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

