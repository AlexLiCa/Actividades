import pymongo
from pprint import pprint



class Cuenta(): 
    def __init__(self,  titular : str , nip: int, saldo: float) -> None:
        self.nip = nip
        self.saldo = saldo
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
        


if __name__ == "__main__":

    # Conéctate a la base de datos
    cliente = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cliente["banco_distribuidos"]

    andy = Cuenta("Andrea", 123, 500)
    datos_andy = vars(andy)

    # Guarda el diccionario en la base de datos
    coleccion = db["Cuentas"]
    coleccion.insert_one(datos_andy)

    cliente.close()

    # pprint(vars(andy))

    # print(andy.retira(600, 123))
    # print(andy.retira(10, 321))
    # print(andy.retira(-10, 123))
    # print(andy.retira(10, 123))

    # pprint(vars(andy))


    # print(andy.deposita(-20))
    # print(andy.deposita(20))

    # pprint(vars(andy))
