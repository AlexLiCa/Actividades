import pymongo
from pprint import pprint
import threading
import random


class Cuenta:
    def __init__(self, titular: str, no_cuenta: int, nip: int, saldo: float) -> None:
        self.nip = nip
        self.saldo = saldo
        self.no_cuenta = no_cuenta
        self.titular = titular
        self.lock_saldo = threading.Lock()

    def retira(self, cantidad: float, nip_recibido: int):
        if nip_recibido != self.nip:
            return False

        with self.lock_saldo:
            if cantidad > 0 and self.saldo >= cantidad:
                self.saldo -= cantidad
                return True
            else:
                return False

    def deposita(self, cantidad: float):
        with self.lock_saldo:
            if cantidad > 0:
                self.saldo += cantidad
                return True
            else:
                return False

    def actualiza_saldo_en_bd(self, coleccion):
        with self.lock_saldo:
            coleccion.update_one({"no_cuenta": self.no_cuenta}, {
                                 "$set": {"saldo": self.saldo}})

    def transfiere(self, cuenta_destino, monto: float, coleccion):
        if self.no_cuenta == cuenta_destino.no_cuenta:
            return False

        if self.retira(monto, self.nip):
            if cuenta_destino.deposita(monto):
                self.actualiza_saldo_en_bd(coleccion)
                cuenta_destino.actualiza_saldo_en_bd(coleccion)
                print(
                    f"{self.titular} transfirio {monto}. a {cuenta_destino.titular} \n")
                return True

        return False


def transferencia(cuenta_origen, cuenta_destino, monto, coleccion):
    return cuenta_origen.transfiere(cuenta_destino, monto, coleccion)


def crea_cuenta(titular: str, nip: int, saldo: float = 0):
    cliente = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cliente["banco_distribuidos"]
    coleccion = db["Cuentas"]

    no_cuenta = coleccion.count_documents({}) + 1
    nueva_cuenta = Cuenta(titular, no_cuenta, nip, saldo)
    coleccion.insert_one(
        {"titular": titular, "no_cuenta": no_cuenta, "nip": nip, "saldo": saldo})

    cliente.close()


if __name__ == "__main__":
    cliente = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cliente["banco_distribuidos"]
    coleccion = db["Cuentas"]
    documentos = list(coleccion.find())

    num_hilos = 3
    hilos = []

    for i in range(num_hilos):
        doc_origen = random.choice(documentos)
        doc_destino = random.choice(documentos)

        cuenta_origen = Cuenta(
            doc_origen['titular'], doc_origen['no_cuenta'], doc_origen['nip'], doc_origen['saldo'])
        cuenta_destino = Cuenta(
            doc_destino['titular'], doc_destino['no_cuenta'], doc_destino['nip'], doc_destino['saldo'])

        hilo = threading.Thread(target=transferencia, args=(
            cuenta_origen, cuenta_destino, random.randint(10, 300), coleccion))
        hilos.append(hilo)

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    cliente.close()
