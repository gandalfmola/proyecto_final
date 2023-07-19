import requests
from mi_aplicacion.models import Position
import sqlite3
import datetime



def my_consult(cripto):
    apikey = "F36C75E1-23E6-4A6E-9049-9345741ED24E"
    url = f"https://rest.coinapi.io/v1/exchangerate/{cripto}/EUR?apikey={apikey}"
    response = requests.get(url)
    value = response.json()    
    print("value es", value)   
    print(response.status_code, response.text)    

    if response.status_code == 200:

        return True,value["rate"]
    
    else:
        return False,value["error"]


def my_global_consult(list):
    url = "https://rest.coinapi.io/v1/exchangerate/EUR?apikey=F36C75E1-23E6-4A6E-9049-9345741ED24E"
    
    response = requests.get(url)
    value = response.json()
    print(response.status_code)

    if response.status_code == 200:    
        probando = value["rates"]    
        valores = []
        print("list es", list)
        

        for clave in list:

            for element in probando:
                if element["asset_id_quote"] != "EUR" and element["asset_id_quote"] == clave:
                    valor = exchange(1, element["rate"])
                    valores.append((clave, valor))                   
                                
        return True,valores
    
    else:
        return False, value["error"]


def exchange(coin1, coin2):
    return float(coin1)/float(coin2)

def exchange_eur(cantidad, cambio):
    return float(cantidad)* float(cambio)


def create_inst(moment, coin_from,q, coin_to,r, value_u):
    pos = Position(moment, coin_from,q, coin_to,r, value_u)

    return pos    


def insert_reg(mov):
    connection = sqlite3.connect("data/registro.db")
    cur = connection.cursor()

    query = """INSERT INTO registro (Fecha, Froome, Q, Too, R, PU) values(?, ?, ?, ?, ?, ?);"""

    #unidades = 1

    cur.execute(query, (mov.moment, mov.coin_from, mov.q, mov.coin_to, mov.r, mov.value_u))
    connection.commit()

def saldos():
    connection = sqlite3.connect("data/registro.db")
    cur = connection.cursor()

    criptos = ['EUR' ,'BTC', 'ETH', 'ADA', 'XRP', 'LTC']
    saldos = {}
    for cripto in criptos:
        
        query = """SELECT R FROM registro WHERE Too = (?) """
        cur.execute(query, (cripto,))
        sumatorio = cur.fetchall()
        
        if len(sumatorio) > 0:
            total = 0
            for saldo in sumatorio:
                # Ponemos posicion [0] porque el segundo elemento de la tupla está vacío
                total += saldo[0]
            saldos[cripto] = total
        else:
            saldos[cripto] = 0

    # Vamos a intentar sacar los saldos de las ventas
    for cripto in criptos:
        #print(cripto)
        query = """SELECT Q FROM registro WHERE Froome = (?) """
        cur.execute(query, (cripto,))
        sumatorio = cur.fetchall()
        #print("segundo sumatorio es", sumatorio)
        if len(sumatorio) > 0:
            for saldo in sumatorio:
                saldos[cripto] -= saldo[0]

    return saldos


def show():
    connection = sqlite3.connect("data/registro.db")
    cur = connection.cursor()
    query = """SELECT * FROM registro;"""
    cur.execute(query)
    res = cur.fetchall()    
    resumen = []
    for element in res:
        mov = Position(element[1], element[2], element[3], element[4],element[5], element[6])
        resumen.append(mov)

    #print("resumen es ", resumen)
    #print(resumen[0])

    return resumen

def view_movements():
    listado = show()    
    for mov in listado:
        print("prueba",mov)


def moment_calculate():
    prueba = datetime.datetime.now()
    fecha = datetime.datetime.strftime(prueba, "%d/%m/%Y %H:%M:%S")

    return fecha

def tupla_a_lista(elemento):
    elemento = list(elemento)
    resultado = []
    for tup in elemento:
        tup = list(tup)
        resultado.append(tup)

    return resultado







