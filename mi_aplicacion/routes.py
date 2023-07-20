from mi_aplicacion import app
from flask import render_template, request, redirect, flash
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
    
    # Si el método es POST entramos por este else
    else:        
        # Metemos en prueba el contenido del formulario que traemos de COMPRA.HTML
        prueba = form.data
        print("prueba es ", prueba)
        # Probamos a extraer de request.form cual de los botones fué pulsado
        otra_prueba = request.form.get("Boton")        
        # Declaramos las variables para los diferentes parámetros que vamos a utilizar
        #moneda_from = prueba["moneda_from"]
        #print("moneda_from es", moneda_from)
        #moneda_to = prueba["moneda_to"]
        #print("moneda_to es", moneda_to)
        #cantidad = prueba["cantidad"]        
        #print("cantidad es", cantidad)
        boton_calcular = prueba["boton_calcular"]
        print("boton_calcular es", boton_calcular)
        boton_comprar = prueba["boton_comprar"]
        print("boton_comprar es", boton_comprar)
        # Probamos a meterle info al hidden
        #form.hid1.data = moneda_from
        #form.hid2.data = moneda_to
        #form.hid3.data = cantidad
        #print("prueba con cambio es", prueba)


        # Por aquí viene la opción CALCULAR:
        if boton_calcular == True:

            # Vamos a probar a fijar aquí los campos hidden
            moneda_from = prueba["moneda_from"]
            moneda_to = prueba["moneda_to"]
            cantidad = prueba["cantidad"]
            form.hid1.data = moneda_from
            form.hid2.data = moneda_to
            form.hid3.data = cantidad

            # Obtenemos la cantidad a comprar de moneda_from
            resultado = conversor(moneda_from, moneda_to, cantidad)
            print("resultado de calcular es", resultado)
            print(type(resultado))

            # Si da error lo mostramos por pantalla
            if type(resultado[0]) == str:
                return render_template("compra.html", formulario=form, vendes = "",compras=resultado)

            # Si va bien devolvemos el cálculo y habilitamos botón comprar
            else:                
                return render_template("compra.html", formulario=form, vendes = cantidad,compras=resultado, moneda_from=moneda_from, moneda_to=moneda_to)           
                
        
        # Aquí montamos la opción de COMPRAR:    
        else:
            # Intentamos proteger de los cambios en último momento
            #prueba = form.data
            print("prueba ya en COMPRAR es ", prueba)
            moneda_from = prueba["moneda_from"]
            moneda_to = prueba["moneda_to"]
            cantidad = prueba["cantidad"]

            if moneda_from != form.hid1.data or moneda_to != form.hid2.data or str(cantidad) != form.hid3.data:
                print("SIN CAMBIOS CABRON")
                flash("SIN CAMBIOS CABRON")
                return render_template("compra.html", formulario=form, moneda_from=moneda_from, moneda_to=moneda_to)

            else:
                        
                # primero obtenemos el cálculo de moneda_from y el cambio unitario 
                print("datos antes de comprar", prueba)           
                resultado,cambio = conversor(moneda_from, moneda_to, cantidad)
                print("resultado de comprar es", resultado)
                
                # Si da error lo mostramos por pantalla
                if type(resultado) != float:
                    return render_template("compra.html", formulario = form, compras=resultado, vendes="")
                
                elif type(cambio) != float:
                    return render_template("compra.html", formulario = form, compras=cambio, vendes="")

                # Si va todo bien insertamos la compra en la base de datos
                else:                             
                    # Creamos el objeto con el contenido del tipo de cripto y el valor
                    first_mov = create_inst(moment_calculate(),moneda_from, cantidad, moneda_to, resultado, cambio)
                    print(first_mov)
                    # Incluimos el nuevo objeto en la base de datos
                    insert_reg(first_mov)

                    return redirect("/")            


@app.route("/status")
def status():
    # Obtenemos el saldo de cada una de nuestras criptos
    mayor = saldos()    
    # Obtenemos la cantidad de euros enganchados
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

        print("tabla final es", tabla_final)

        return render_template("status.html", resumen = tabla_final, euros=balance_euros, valor_act = valor_criptos, resultado = res_inv)
    
    else:
        return render_template("status.html", error=valores)
    

@app.route("/prueba")
def prueba():

    return render_template("prueba.html")

















