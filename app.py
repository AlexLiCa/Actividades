from flask import Flask, render_template, request, redirect, url_for
import pymongo
# Asegúrate de importar tu clase Cuenta desde el módulo correspondiente
from cuenta import Cuenta

app = Flask(__name__)

def obtener_coleccion():
    cliente = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cliente["banco_distribuidos"]
    return db["Cuentas"]

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/transferencia')
def transferencia():
    return render_template('transferencia.html')


@app.route('/retirar')
def retirar():
    return render_template('retirar.html')

@app.route('/depositar')
def depositar():
    return render_template('depositar.html')

@app.route('/trans', methods=['POST'])
def trans():
    try:
        titular = request.form['titular']
        no_cuenta = int(request.form['no_cuenta'])
        cantidad = float(request.form['cantidad'])
    except:
        print("No se pusieron datos validos")

    print(
        f"Titular: {titular}.\nCuenta: {no_cuenta}. \nMonto: {cantidad}"
        )
    
    return redirect(url_for('inicio'))


@app.route('/retiros', methods=['POST'])
def retiros():
    try:
        titular = request.form['titular']
        no_cuenta = int(request.form['no_cuenta'])
        cantidad = float(request.form['cantidad'])
    except:
        print("No se pusieron datos validos")

    print(
        f"Titular: {titular}. \nCuenta: {no_cuenta}.\nMonto: {cantidad}"
    )

    return redirect(url_for('inicio'))


@app.route('/depositos', methods=['POST'])
def depositos():
    try:
        titular = request.form['titular']
        no_cuenta = int(request.form['no_cuenta'])
        cantidad = float(request.form['cantidad'])
    except:
        print("No se pusieron datos validos")

    print(
        f"Titular: {titular}. \nCuenta: {no_cuenta}.  \nMonto:{cantidad}"
    )

    return redirect(url_for('inicio'))


if __name__ == '__main__':
    app.run(debug=True)
