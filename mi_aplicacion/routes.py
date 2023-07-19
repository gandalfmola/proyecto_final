from mi_aplicacion import app
from flask import render_template, request, redirect
from mi_aplicacion.controler import *
from mi_aplicacion.forms import MovementForm


@app.route("/")
def index():    
    print()
    print("saldos es", saldos())
    print()
     
    return render_template("index.html", resumen = show())


@app.route("/compra", methods=["GET", "POST"])
def compra():

    # Lo primeros instanciamos el formulario
    form = MovementForm()
    print("form es", form.data)
    

    # Si el método es GET entramos por aquí
    if request.method == "GET":
        return render_template("compra.html", formulario=form)
    
    #Si el método es POST entramos por este else
    else:        
        # Metemos en prueba el contenido del formulario que traemos de COMPRA.HTML
        prueba = form.data
        print("compra es ", prueba)
        # Probamos a extraer de request.form cual de los botones fué pulsado
        otra_prueba = request.form.get("Boton")        
        # Declaramos las variables para los diferentes parámetros que vamos a utilizar
        moneda_from = prueba["moneda_from"]
        print("moneda_from es", moneda_from)
        moneda_to = prueba["moneda_to"]
        print("moneda_to es", moneda_to)
        cantidad = prueba["cantidad"]        
        print("cantidad es", cantidad)
        boton_calcular = prueba["boton_calcular"]
        print("boton_calcular es", boton_calcular)
        boton_comprar = prueba["boton_comprar"]
        print("boton_comprar es", boton_comprar)

        if cantidad == "":
            cantidad = 0

        # Vamos a implantar el if para la consulta:
        if boton_calcular == True:

            # OPCIÓN 1: UTILIZAMOS EUROS PARA COMPRAR UNA CRIPTO
            if moneda_from == "EUR" and moneda_to != "EUR" and float(cantidad) > 0:
                # Obtenemos el valor unitario en euros de la cripto seleccionada               
                probatina,cambio = my_consult(moneda_to)
                print("cambio es", cambio)

                # Con probatina controlamos el error si el status_code no es un 200
                if probatina == True:
                    #cantidad = prueba["amount"]        
                    print("cantidad es", cantidad)
                    # Calculamos la conversión a la cripto según el nº de euros que hayamos introducido en Q:
                    conv = exchange(cantidad, cambio)
                    print("conv es", conv)

                    answer = 1

                    return render_template("compra.html", formulario = form, compras=cantidad, vendes=conv)
                
                # Por aquí viene si probatina ha dado error
                else:
                    answer = 0
                    cantidad = cambio

                    return render_template("compra.html", compra_option=answer, error=cantidad)
            
            # OPCIÓN 2: TRADEO DE CRIPTOS
            elif moneda_from != "EUR" and moneda_to != "EUR" and float(cantidad) > 0 and moneda_from != moneda_to:
                # Obtenemos el valor unitario en euros de la primera cripto
                probatina1,value_cr1 = my_consult(moneda_from)
                # Obtenemos el valor unitario en euros de la segunda cripto
                probatina2,value_cr2 = my_consult(moneda_to)

                # Con probatina controlamos el error si el status_code no es un 200
                if probatina1 == True and probatina2 == True:

                    # Calculamos cuantas segundas criptos podemos comprar con la cantidad de las primeras elegidas
                    cantidad = prueba["amount"]
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

                    return render_template("compra.html", respuesta = conv, amount=cantidad, campo1=moneda_from, campo2=moneda_to, cambio=value_cr1, compra_option=answer)
                
                # Por aquí viene si ha habido error en probatina
                elif probatina1 == False:
                    answer = 0
                    #cantidad = cambio

                    return render_template("compra.html", compra_option=answer, error=value_cr1)
                
                # Por aquí viene si ha habido error en probatina
                else:
                    answer = 0
                    #cantidad = cambio

                    return render_template("compra.html", compra_option=answer, error=value_cr2)
            
            # OPCIÓN 3: RECUPERAMOS INVERSIÓN VENDIENDO UNA CRIPTO A CAMBIO DE EUROS
            elif moneda_from != "EUR" and moneda_to == "EUR" and float(cantidad) > 0:
                # Obtenemos el valor unitario en euros de la cripto seleccionada               
                probatina, cambio = my_consult(prueba["campo1"])
                print("cambio es", cambio)

                # Con probatina controlamos el error si el status_code no es un 200:
                if probatina == True:

                    cantidad = prueba["amount"]        
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

                    return render_template("compra.html", respuesta = conv, amount=cantidad, campo1=moneda_from, campo2=moneda_to, cambio=cambio, compra_option = answer)
                
                else:
                    answer = 0
                    cantidad = cambio

                    return render_template("compra.html", compra_option=answer, amount=cantidad)               

            
            # OPCIONES 4 Y 5: SON UN CONTROL DE ERRORES PARA CANTIDAD O MONEDAS IGUALES        
            elif moneda_from == moneda_to and float(cantidad) > 0:
                cantidad = "Debes seleccionar dos monedas diferentes"
                answer = 0

                return render_template("compra.html", amount=cantidad, compra_option = answer)
                    
            elif float(cantidad) <= 0:
                cantidad = "La cantidad selecionada no puede ser menor o igual a cero"
                answer = 0

                return render_template("compra.html", amount=cantidad, compra_option = answer)
            
        else:            
            # Aquí montamos la opción de COMPRAR:
            # Obtenemos el valor unitario en euros de la cripto seleccionada               
            cambio = my_consult(moneda_to)
            # Calculamos la conversión a la cripto según el nº de euros que hayamos introducido en Q:
            conv = exchange(cantidad, cambio)
            print("conv es", conv)
            # Creamos el objeto con el contenido del tipo de cripto y el valor
            first_mov = create_inst(moment_calculate(),moneda_from, cantidad, moneda_to, conv, cambio)
            print(first_mov)
            # Incluimos el nuevo objeto en la base de datos
            insert_reg(first_mov)

            return redirect("/")


@app.route("/compra_realizada/<campo1>/<campo2>/<amount>/<respuesta>/<cambio>", methods=["GET", "POST"])
def compra_realizada(campo1, campo2, amount, respuesta, cambio):
    print("traemos campo1 ", campo1, "y campo2", campo2, "y amount ", amount)
    data = request.form
    print("data es", data)
    # Creamos el objeto con el contenido del tipo de cripto y el valor
    first_mov = create_inst(moment_calculate(),campo1, amount, campo2, respuesta, cambio)
    print(first_mov)
    # Incluimos el nuevo objeto en la base de datos
    insert_reg(first_mov)

    return redirect("/")


@app.route("/status")
def status():
    # Obtenemos el saldo de cada una de nuestras criptos
    mayor = saldos()
    print("mayor es", mayor)

    balance_euros = mayor["EUR"]
    print("balance_euros es", balance_euros)
    # Obtenemos al valor actual de cada una de esas criptos
    claves = list(mayor.keys())
    print(claves)

    # Vamos a intentar capturar el posible error de la API en la consulta
    
    probatina,valores = my_global_consult(claves)
    if probatina == True:       
 
        # Aplicamos al saldo de cada cripto su valor actual en euros
        mayor_lista = list(mayor.items())    

        tabla = []

        for cripto in mayor_lista:
            for valor in valores:
                if cripto[0] == valor[0]:
                    tabla.append(float(cripto[1]*float(valor[1])))
        
        # Procesamos mayor_lista para añadirle a cada elemento el valor actual(cada elemento tenía tipo de moneda y cantidad de la misma que tenemos)
        mayor_lista_listas = tupla_a_lista(mayor_lista)        

        tabla_final = []

        for element in mayor_lista_listas:
            if element[0] != "EUR":
                for valor in valores:
                    if element[0] == valor[0]:
                        element.append(float(valor[1])*float(element[1]))
                        tabla_final.append(element)
        
        # Calculamos el valor de las inversiones de tabla_final
        valor_criptos = 0
        for element in tabla_final:
            valor_criptos += element[2]    

        # Calculamos el resultado de la inversion
        res_inv = valor_criptos + balance_euros    

        return render_template("status.html", resumen = tabla_final, euros=balance_euros, valor_act = valor_criptos, resultado = res_inv)
    
    else:
        return render_template("status.html", error=valores)
    

@app.route("/prueba")
def prueba():

    return render_template("prueba.html")

















