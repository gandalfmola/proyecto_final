# Gestión de movimientos
Prototipo de aplicación web realizada con flask sin seguridad ni gestión de usuarios.
Permite registrar compras simuladas de criptomonedas de entre las siguientes
- EUR(divisa)
- BTC,      LTC,
- ETH,		USDT,
- BNB, 		XRP,
- ADA, 		SOL,
- MATIC,    DOT,

## Reglas básicas de la simulación de compra-venta
1. Se parte de infinitos euros (siempre se pueden conseguir más trabajando)
2. Sólo se puede vender una criptomoneda si se dispone de saldo de la misma. Se ha comprado anteriormente y aún no se ha vendido.

## Funcionalidad de la aplicación
Tiene tres pantallas básicas.
- Pantalla resumen con todos los movimientos realizados (sin paginación).
- Pantalla de compra-venta de criptomonedas, cada vez que realicemos una compra-venta nos llevará a la página resumen para ver como se ha añadido la nueva operación que acabmos de realizar
- Pantalla de estado de la inversión. Mostrará el dinero que representan las criptomonedas de las que aún tenemos saldo, su coste real en euros y su valor en euros al momento de realizar la consulta.

## Instalación

### Servicios externos

Esta aplicación utiliza coinAPI.io como servicio para calcular el valor actual de cada cripto. Para hacerla funcionar es necesario obtener una apikey en [su web](https://www.coinapi.io/market-data-api/pricing)

### Paso a paso

1. Replicar el fichero `.env_template` y renombrarlo a `.env`

2. Informar las siguientes claves:
    - FLASK_APP: main.py (no cambiar)
    - FLASK_DEBUG: debe ser False en entornos de producción, si vas a modificar la aplicación es más cómodo a True
    - FLASK_SECRET_KEY: una clave secreta cualquiera. Un buen sitio para generarlas es [este](https://randomkeygen.com)
    - FLASK_API_KEY: la apikey de coinApi.io obtenida más arriba

3. Ejecutar el archivo creadb.py para crear la base de datos en la que se irán volcando la operaciones de compra y tradeo



## Ejecución de la aplicación
1. Instalar todas las dependencias. Escribir
```
pip install -r requirements.txt
```

2. Lanzar la aplicación desde directorio donde esté instalada. Teclear
```
flask run
```









