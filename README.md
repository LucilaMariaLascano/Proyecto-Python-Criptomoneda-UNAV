# Proyecto-Python-Criptomoneda-UNAV

## PYTHON PARA ANALISIS DE DATOS: COTIZACION DE CRIPTOMONEDAS

Lucila María Lascano

Diciembre 2021


## INTRODUCCION

El objetivo de la aplicación creada es obtener a través de una API los datos necesarios
de la página web Kraken , para luego con ellos graficar la cotización de un par de
criptomonedas. El par de cotizaciones, así como el periodo de tiempo y el intervalo,
podrán ser seleccionados por el usuario a través de un menú desplegable.

Asimismo, se calcula el valor del VWAP y se grafica junto con la cotización del par
seleccionado.

## METODOLOGIA

El código de la aplicación de cotización de criptomonedas ha sido desarrollado en
Python, teniendo en cuenta las librerías necesarias para poder representar y graficar
correctamente la información correspondiente.

Para conseguir dicho objetivo, en primer lugar, se ha utilizado una API de Kraken con el
fin de leer el movimiento de los pares de criptomonedas. Al mismo tiempo, se ha
agregado el manejo de errores para aquellos casos en los cuales al conectarse a la
interfaz de programación de aplicaciones no haya ningún resultado.

Con dicha información se ha creado el dataset, sobre el cual en algunos casos fue
necesario transformar el tipo de dato. Si bien la información obtenida brindaba el valor
del VWAP, se decidió calcularlo nuevamente generando un nuevo campo llamado
VWAP_calculado, el cual fue utilizado luego en la gráfica.

Se ha ideado crear un gráfico de líneas con la opción de agregar menús desplegables
para que el usuario pudiera seleccionar el par de monedas, intervalo y fechas
correspondientes. Para ello fue necesario, crear anticipadamente los listados
predefinidos en el caso de monedas e intervalos, y un componente DatePicker
(calendario) para las fechas.

Una vez construido el dataset y generados los listados para los menús desplegables, a
partir de una función se ha procedido a graficar y actualizar conjuntamente las
cotizaciones (low y high) del par calculado, y el VWAP_calculado teniendo en cuenta los
parámetros seleccionados por el usuario.

### Inicialización del proyecto

Para inicializar el proyecto utilizamos poetry new Proyecto_Python_Cripto y poetry
init los cuales crean una estructura de proyecto por defecto para poder comenzar a
trabajar.

Las librerías han sido agregadas utilizando el comando poetry add el cual agrega las
mismas al archivo pyproject.toml.

```
python = "^3.8"
dash==2.0.
pandas==1.3.
gunicorn==20.0.
krakenex==2.1.
numpy==1.20.
```
Las mismas librerías se han incorporado al archivo requirements.txt de dónde son leídas
para ser instaladas en Heroku al momento de subir la aplicación.

Para ejecutar la aplicación en su entorno local, luego de clonarlo desde el repositorio
indicado a continuación, debe ejecutarse el comando poetry install el cual leerá las
dependencias del archivo pyproject.toml y las instalará en su ordenador.

El archivo para inicializar la aplicación es el app.py el cual debe ser ejecutado desde
PyCharm como archivo de entrada a la aplicación.

#### Repositorio

Como repositorio colaborativo de código se ha utilizado GitHub para mantener el control
de versiones del proyecto.

Se puede acceder al código clonándolo del siguiente repositorio:

https://github.com/LucilaMariaLascano/Proyecto-Python-Criptomoneda-UNAV


#### Distribución del código

A los efectos de presentar el resultado del trabajo el código ha sido distribuido en la
nube a través de Heroku, siendo la URL correspondiente la siguiente:

https://guarded-sands-06815.herokuapp.com/

### Elementos utilizados

#### Librerías

A continuación, se mencionan las librerías utilizadas:

_Datetime_
Librería estándar que proporciona clases para manipular fechas y horas.

_Dash_
Facilita la creación de dashboards y visualizaciones.

_Pandas_
Proporciona estructuras de datos rápidas, flexibles y expresivas diseñadas para que el
trabajo con datos "relacionales" o "etiquetados" sea fácil e intuitivo.

_Numpy_
Proporciona un poderoso objeto de matriz N-dimensional con capacidades útiles de
álgebra lineal.

_Krakenex_
Proporciona un contenedor conveniente para la API de Kraken.

#### API

Se utiliza la interfaz de programación de aplicaciones pública de Kraken, usando OHLC
Data.

Los parámetros de la query son los siguientes:

par requerido: string
Ejemplo: par=XBTUSD
Par de monedas de las cuales se busca la información

intervalo: integer
Default: 1
Enum: 1 5 15 30 60 240 1440 10080 21600
Ejemplo: interval=60
Intevalo de tiempo en minutos

desde: integer
Ejemplo: since=1548111600 (UNIX timestamp en segundos)
Devuelve OHLC data desde el ID brindado

#### Clases

Para cumplir con la Programación Orientada a Objetos se ha creado la clase
Criptomoneda, que contiene toda la información necesaria del par a estudiar. En ella se
pueden encontrar los siguientes atributos y métodos:

_Atributos de la Clase_

- Moneda – string – indica el par de la cotización de criptomoneda. Ej: Bitcoin/USD.
- Intervalo – integer - intervalo en el cual la API agrupa los precios mostrados.
    Ejemplo: 1 minuto, 1 día, 1 semana, etc.
- Fecha – timestamp – fecha en formato Timestamp que representa la fecha de
    inicio desde la cual se obtienen las cotizaciones. La API devuelve sólo 720
    registros desde esta fecha de inicio, con el intervalo indicado anteriormente.

_Métodos de la Clase_

- obtener_cotizaciones () – este método permite adquirir las cotizaciones de
    criptomonedas de Kraken, y crear con dicha información el dataset. El mismo no
    recibe parámetros, sino que lee los datos necesarios directamente de los
    atributos de la clase.

#### Favicon

A los efectos de personalizar e identificar la página web a construir se ha seleccionado
un dibujo de gráficos como icono de página para acompañar a la URL en el navegador.



### Construcción del dataset

El dataset se encuentra conformado por las siguientes columnas:

- Time
- Open
- High
- Low
- Close
- VWAP: VWAP que se obtiene por defecto de Kraken.
- Volume
- Count
- Date: se crea esta nueva variable gracias a la función pandas to datetime,
    convirtiendo la variable ‘Time’ que se encuentra en formato timestamp, al
    formato YYYY-MM-DD.
- VWAP_calculado: VWAP calculado y utilizado para visualizar en el gráfico
    construido.


#### Cálculo del nuevo VWAP

La información obtenida de Kraken posee un campo correspondiente al VWAP. Sin
embargo, se ha decidido crear un nuevo campo VWAP_calculado, cuyo cómputo se ha
realizado en base a la fórmula VWAP = Media ponderada * volumen.

Es decir, que se ha efectuado la sumatoria del Volumen * ((High + Low + Close) /3),
dividido la sumatoria del Volumen.

Sin embargo, para poder realizar dicha operatoria primero fue necesario convertir los
precios (Open, High, Low, Close y Volume) a valor numérico con el método
_‘apply(pd.to_numeric)’_ ya que los mismos eran de tipo Object..

### Creación del gráfico

A partir de la información obtenida en el dataset se genera un gráfico de líneas dinámico
con la ayuda de las librerías dash y plotly.

Para realizarlo y actualizar sus valores se llama a la función update_charts con los
parámetros: filtro_par_cripto, intervalos_tiempo y seleccion_fechas, cuyos valores se
obtienen de los componentes de los filtros.

En términos generales la gráfica muestra el comportamiento de la cotización de un par
de criptomonedas y del VWAP a través de un intervalo de tiempo prestablecido.

Los precios se representan con líneas, siendo ‘Low’ la línea roja, ‘High’ la línea verde y
‘VWAP’ la línea negra, correspondiéndose el eje X con las fechas y el eje Y con los
valores.

#### Filtros Gráfico

_Par de criptomonedas_

De todas las criptomonedas disponibles en Kraken, se han seleccionado los diez pares
más consultados permitiendo al usuario pueda optar entre los mismos:

- Bitcoin-USD : XXBTZUSD
- Monero-USD: XXMRZUSD
- Ripple-USD : XXRPZUSD
- Ethereum-USD: XETHZUSD
- Ethereum Classic-USD: XETCZUSD
- Bitcoin-EUR: XXBTZEUR
- Monero-EUR: XXMRZEUR
- Ripple-EUR: XXRPZEUR
- Ethereum-EUR: XETHZEUR
- Ethereum Classic-EUR: XETCZEUR


_Intervalo_

El listado de intervalos a escoger por el usuario es el siguiente:

- 1 minuto
- 5 minutos
- 15 minutos
- 30 minutos
- 1 hora
- 4 horas
- 1 día
- 7 días
- 15 días

_Fecha_

La fecha ha sido creada con un componente DatePickerSingle, con las siguientes
características:

- El mínimo de la fecha desde la cual se quiere visualizar la información se ha
    establecido en 01/01/2021 (hasta la fecha actual), con el fin de no cargar
    demasiado la página web.
- La fecha desde la cual se quiere visualizar los datos puede ser seleccionada por
    el usuario. Sin embargo, la fecha hasta la cual se pueden representar siempre
    va a ser el día de la fecha que el usuario ejecute el gráfico.
- La fecha se ha convertido a formato '%Y-%m-%d', por ejemplo: 2021- 01 - 01, para
    una mejor visualización y entendimiento del usuario.

### Manejo de errores

Con el objetivo de manejar errores de ejecución, se ha utilizado el bloque Try-Except
para aquellos casos en los cuales al conectarse a la API de Kraken no haya ningún
resultado, verificando la clave del result en el JSON obtenido de la respuesta de Kraken.

Asimismo, se ha ubicado al final un bloque Finally, que en caso de error devuelve un
objeto vacío ya que no se pudo obtener la información de la API, y despliegue en la
consola el mensaje "Ha ocurrido un error al obtener los datos de Kraken".

## RESULTADO

Como resultado se obtiene una aplicación que incluye un gráfico interactivo de líneas
que permite visualizar la cotización de un par de criptomonedas determinado (Ejemplo:
Bitcoin/USD), en un plazo determinado de tiempo y con un intervalo especifico (Ejemplo:
1 minuto, 1440 minutos).

Gracias a la interactividad que el gráfico posee el usuario puede seleccionar el par de
criptomonedas, el intervalo, y la fecha desde la cual desea visualizar la información.

