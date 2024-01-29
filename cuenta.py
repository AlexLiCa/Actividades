import pymongo
from pprint import pprint
import threading
import random

class Cuenta(): 
    def __init__(self,  titular : str , no_cuenta : int,  nip: int, saldo: float ) -> None:
        self.nip = nip
        self.saldo = saldo
        self.no_cuenta = no_cuenta
        self.titular = titular
        self.lock_saldo = threading.Lock()
        
    def retira(self, cantidad : float, nip_recibido : int ):
       with self.lock_saldo:
        if isinstance(nip_recibido, int) and isinstance(cantidad, (int, float)) and cantidad > 0:
                if nip_recibido == self.nip and self.saldo >= cantidad:
                    self.saldo = self.saldo - cantidad
                    return True 
                else:
                    return False
        else : 
            return None

    def deposita(self, cantidad: float):
        with self.lock_saldo:
            if isinstance(cantidad, (float, int)) and cantidad > 0:
                self.saldo += cantidad
                return True
            else:
                return None 
    
    def transfiere(self, cuenta_destino: 'Cuenta', monto : float, coleccion ):
        if self.saldo >= monto:
            self.saldo -= monto
            cuenta_destino.deposita(monto)
            #Actualizamos la cuenta original
            coleccion.update_one({"no_cuenta": self.no_cuenta}, {
                                            "$set": {"saldo": self.saldo}})
            #Actualizamos la cuenta a la que depositamos
            coleccion.update_one({"no_cuenta": cuenta_destino.no_cuenta}, {
                                "$set": {"saldo": cuenta_destino.saldo}})
            
            print(f"{self.titular} transfirio {monto}. Saldo: {self.saldo} \n")
            return True
        else:
            print(f"{self.titular} no pudo transferir {monto}. \n")
            return False


def transferencia(cuenta_origen: "Cuenta", cuenta_destino:  "Cuenta", monto: float, coleccion):
    return cuenta_origen.transfiere(cuenta_destino, monto, coleccion)

def crea_cuenta(titular: str, nip: int, saldo : float = 0):
    # Conéctate a la base de datos
    cliente = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cliente["banco_distribuidos"]
    coleccion = db["Cuentas"]

    cantidad_documentos = coleccion.count_documents({})

    nueva_cuenta = vars(Cuenta(titular, cantidad_documentos+1, nip, saldo))
    coleccion.insert_one(nueva_cuenta)

    cliente.close()



if __name__ == "__main__":
    cliente = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cliente["banco_distribuidos"]
    coleccion = db["Cuentas"]
    documentos = list(coleccion.find())

    num_hilos = 20
    hilos = []

    for i in range(num_hilos):
            # Seleccionar un documento aleatorio
        documento_aleatorio = random.choice(documentos)

        # Crear una instancia de la clase Cuenta con los datos del documento
        cuenta_origen = Cuenta(
            titular=documento_aleatorio['titular'],
            no_cuenta=documento_aleatorio['no_cuenta'],
            nip=documento_aleatorio['nip'],
            saldo=documento_aleatorio['saldo']
        )

        documento_aleatorio = random.choice(documentos)

        # Crear una instancia de la clase Cuenta con los datos del documento
        cuenta_destino = Cuenta(
            titular=documento_aleatorio['titular'],
            no_cuenta=documento_aleatorio['no_cuenta'],
            nip=documento_aleatorio['nip'],
            saldo=documento_aleatorio['saldo']
        )

        hilo = threading.Thread(
            target=transferencia, args=(cuenta_origen, cuenta_destino, random.randint(10,500), coleccion))
        
        
        hilos.append(hilo)

        # Iniciar cada hilo
    for hilo in hilos:
        hilo.start()

    # Esperar a que cada hilo termine
    for hilo in hilos:
        hilo.join()

    cliente.close()









