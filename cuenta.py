import pymongo
from pprint import pprint
import threading


class Cuenta(): 
    def __init__(self,  titular : str , no_cuenta : int,  nip: int, saldo: float ) -> None:
        self.nip = nip
        self.saldo = saldo
        self.no_cuenta = no_cuenta
        self.titular = titular
        
    def retira(self, cantidad : float, nip_recibido : int ):
       if isinstance(nip_recibido, int) and isinstance(cantidad, (int, float)) and cantidad > 0:
            if nip_recibido == self.nip and self.saldo >= cantidad:
                self.saldo = self.saldo - cantidad
                return True 
            else:
                return False
       else : 
           return None

    def deposita(self, cantidad: float):
        if isinstance(cantidad, (float, int)) and cantidad > 0:
            self.saldo += cantidad
            return True
        else:
            return None 
        

def crea_cuenta(titular: str, nip: int, saldo : float = 0):
    # Conéctate a la base de datos
    cliente = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cliente["banco_distribuidos"]
    coleccion = db["Cuentas"]

    cantidad_documentos = coleccion.count_documents({})

    nueva_cuenta = vars(Cuenta(titular, cantidad_documentos+1, nip, saldo))
    coleccion.insert_one(nueva_cuenta)

    cliente.close()


def transfiere(cuenta_origen: int, nip_origen: int, cuenta_destino: int, saldo : float):
    cliente = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cliente["banco_distribuidos"]
    coleccion = db["Cuentas"]

    filtro = {"no_cuenta": {"$in": [cuenta_origen, cuenta_destino]}}

    resultados = coleccion.find(filtro)


    cuentas_modificadas = []

    for documento in resultados:
        cuenta = Cuenta(
            documento["titular"], documento["no_cuenta"], documento["nip"], documento["saldo"])
        # Modifica la instancia según tus necesidades
        if cuenta.no_cuenta == cuenta_origen:
            envio = cuenta.retira(saldo, nip_origen)
        elif cuenta.no_cuenta == cuenta_destino:
            recivio = cuenta.deposita(saldo)
            
      
        cuentas_modificadas.append(cuenta)

    # Actualiza la base de datos con las instancias modificadas
    if envio and recivio == True:
        for cuenta_modificada in cuentas_modificadas:
            coleccion.update_one({"no_cuenta": cuenta_modificada.no_cuenta}, {
                                "$set": {"saldo": cuenta_modificada.saldo}})
        return True
    else:
        return False

if __name__ == "__main__":
    print(transfiere(1, 123, 3, 200))
    print(transfiere(2, 457, 3, 300))






