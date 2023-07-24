import requests
from mi_aplicacion.models import Position
import sqlite3
import datetime



def my_consult(cripto, apikey):
    #apikey = "F36C75E1-23E6-4A6E-9049-9345741ED24E"
    url = f"https://rest.coinapi.io/v1/exchangerate/{cripto}/EUR?apikey={apikey}"
    response = requests.get(url)
    value = response.json()    
    print("value es", value)   
    print(response.status_code, response.text)    

    count = 0
    while response.status_code == 429 and count < 65:
        response = requests.get(url)
        value = response.json()
        count += 1

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


def conversor(moneda_from, moneda_to, cantidad, apikey):
            
    # OPCIÓN 1: UTILIZAMOS EUROS PARA COMPRAR UNA CRIPTO
            if moneda_from == "EUR" and moneda_to != "EUR" and float(cantidad) > 0:
                # Obtenemos el valor unitario en euros de la cripto seleccionada               
                probatina,cambio = my_consult(moneda_to, apikey)
                print("cambio es", cambio)

                # Con probatina controlamos el error si el status_code no es un 200
                if probatina == True:
                    #cantidad = prueba["amount"]        
                    print("cantidad es", cantidad)
                    # Calculamos la conversión a la cripto según el nº de euros que hayamos introducido en Q:
                    conv = exchange(cantidad, cambio)
                    print("conv es", conv)

                    answer = 1

                    return conv, cambio
                
                # Por aquí viene si probatina ha dado error
                else:
                    return cambio, 
            
            # OPCIÓN 2: TRADEO DE CRIPTOS
            elif moneda_from != "EUR" and moneda_to != "EUR" and float(cantidad) > 0 and moneda_from != moneda_to:
                # Obtenemos el valor unitario en euros de la primera cripto
                probatina1,value_cr1 = my_consult(moneda_from, apikey)
                # Obtenemos el valor unitario en euros de la segunda cripto
                probatina2,value_cr2 = my_consult(moneda_to, apikey)
                print("value_cr2 es", value_cr2)

                # Con probatina controlamos el error si el status_code no es un 200
                if probatina1 == True and probatina2 == True:

                    # Calculamos cuantas segundas criptos podemos comprar con la cantidad de las primeras elegidas
                    #cantidad = prueba["amount"]
                    conv = exchange(float(cantidad)*float(value_cr1),value_cr2)

                    # Comprobamos que tenemos suficiente saldo de esa cripto para hacer el tradeo
                    saldo = saldos()
                    print("saldo es", saldo[moneda_from])
                    print("cantidad es", cantidad)

                    answer = 1

                    if float(cantidad) > saldo[moneda_from]:
                        cantidad = "No tienes saldo suficiente para hacer esta compra"
                        answer = 0
                        print("answer es", answer)

                        return cantidad, answer
                    
                    else:
                        return conv, value_cr2
                
                # Por aquí viene si ha habido error en probatina1
                elif probatina1 == False:
                    answer = 0
                    #cantidad = cambio

                    return value_cr1, value_cr1
                
                # Por aquí viene si ha habido error en probatina2
                else:
                    answer = 0
                    #cantidad = cambio

                    return value_cr2, value_cr2
            
            # OPCIÓN 3: RECUPERAMOS INVERSIÓN VENDIENDO UNA CRIPTO A CAMBIO DE EUROS
            elif moneda_from != "EUR" and moneda_to == "EUR" and float(cantidad) > 0:
                # Obtenemos el valor unitario en euros de la cripto seleccionada               
                probatina, cambio = my_consult(moneda_from, apikey)
                print("cambio es", cambio)

                # Con probatina controlamos el error si el status_code no es un 200:
                if probatina == True:

                    #cantidad = prueba["amount"]        
                    print("cantidad es", cantidad)            

                    # Calculamos la conversión a la cripto según el nº de euros que hayamos introducido en Q:
                    conv = exchange_eur(cantidad, cambio)

                    # Comprobamos que tenemos suficiente saldo de esa cripto para hacer el tradeo
                    saldo = saldos()
                    print("saldo es", saldo[moneda_from])
                    print("cantidad es", cantidad)

                    answer = 1
                    
                    if float(cantidad) > saldo[moneda_from]:
                        cantidad = "No tienes saldo suficiente para hacer esta compra"
                        answer = 0
                        print("answer es", answer)

                        return cantidad, cambio
                    
                    else:
                        return conv, cambio
                
                # Por aquí viene si ha habido error en probatina
                else:
                    answer = 0                   

                    return cambio, cambio               

            
            # OPCIONES 4 Y 5: SON UN CONTROL DE ERRORES PARA CANTIDAD O MONEDAS IGUALES        
            elif moneda_from == moneda_to and float(cantidad) > 0:
                print("Por aquí pasa")
                cantidad = "Debes seleccionar dos monedas diferentes"
                resultado = ""
                
                return cantidad,resultado
                    
            elif float(cantidad) <= 0:
                cantidad = "La cantidad selecionada no puede ser menor o igual a cero"
                resultado = ""

                return cantidad, resultado



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







