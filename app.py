from flask import Flask

# importar plantillas 
from flask import render_template

#creación de aplicación
app=Flask(__name__)

# Acceder a Index.html
@app.route('/')
def inicio():
    return render_template('sitio/index.html')

@app.route('/templates/sitio/desafios.html')

if __name__ == '__main__':
    app.run(debug=True)

