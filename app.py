from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def transferencia():
    return render_template('index.html')

@app.route('/procesar_formulario', methods=['POST'])
def procesar_formulario():
    if request.method == 'POST':
        cuenta_origen = request.form['cuenta_origen']
        cuenta_destino = request.form['cuenta_destino']
        cuenta_monto = request.form['monto']
        
        # Puedes hacer lo que quieras con los datos, por ejemplo, imprimirlos en la consola
        print(f'Cuenta Origen: {cuenta_origen}, Cuenta destino: {cuenta_destino}')
        # También puedes redirigir a otra página o mostrar un mensaje de éxito
        return '¡Formulario enviado correctamente!'


if __name__ == '__main__':
    app.run(debug=True)