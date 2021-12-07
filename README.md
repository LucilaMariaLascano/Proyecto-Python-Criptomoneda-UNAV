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
fin de leer el movimiento de los pares de criptomonedas.

Con dicha información se ha creado el dataset, sobre el cual en algunos casos fue
necesario transformar el tipo de dato. Si bien la información obtenida brindaba el valor
del VWAP, se decidió calcularlo nuevamente generando un nuevo campo llamado
VWAP_calculado, el cual fue utilizado luego en la gráfica.

Se ha ideado crear un gráfico de líneas con la opción de agregar menús desplegables
para que el usuario pudiera seleccionar el par de monedas, intervalo y fechas
correspondientes. Para ello fue necesario, crear anticipadamente los listados
predefinidos en el caso de monedas e intervalos, y un calendario para las fechas.

Una vez construido el dataset y generados los listados para los menús desplegables, a
partir de una función se ha procedido a graficar y actualizar conjuntamente las 
cotizaciones (low y high) del par calculado, y el VWAP_calculado teniendo en cuenta los
parámetros seleccionados por el usuario.


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

Se ha creado  la clase Criptomoneda, con sus correspondientes atributos y
métodos.

_Atributos de la Clase_

- Moneda
- Intervalo
- Fecha

_Métodos de la Clase_

Se crea la función obtener_cotizaciones () que permite adquirir las cotizaciones de
criptomonedas de Kraken, y crear con dicha información el dataset.

#### Favicon

A los efectos de personalizar e identificar la página web a construir se ha seleccionado
un dibujo de gráficos como icono de página para acompañar a la URL en el navegador.



### Construcción del dataset

El dataset se encuentra conformado por las siguientes columnas:

- Time
- Open
- High
- LowClose
- VWAP: VWAP que viene por defecto de Kraken.
- Volume
- Count
- VWAP calculado: VWAP calculado y utilizado para visualizar en el gráfico
    construido.
- Date: se crea esta nueva variable gracias a la función pandas to datetime, convirtiendo la variable ‘Time’ que se encuentra
    en segundos, al formato YYYY-MM-DD.


#### Cálculo del nuevo VWAP

La información obtenida de Kraken posee un campo correspondiente al VWAP. Sin
embargo, se ha decidido crear un nuevo campo VWAP_calculado, cuyo cómputo se ha
realizado en base a la fórmula VWAP = Media ponderada * volumen.

Es decir, que se ha efectuado la sumatoria del Volumen * ((High + Low + Close) /3),
dividido la sumatoria del Volumen.

Sin embargo, para poder realizar dicha operatoria primero fue necesario convertir los
precios (Open, High, Low, Close y Volume) a valor numérico con el método
_‘_ apply(pd.to_numeric) _’_ ya que los mismos estaban creados como tipo objeto.

### Creación del gráfico

La información obtenida en el dataset se representa a través de un gráfico de líneas
dinámico generado con la ayuda de la librería dash.

Para realizarlo y actualizar sus valores se llama a la función update_charts con los
parámetros: filtro_par_cripto, intervalos_tiempo y seleccion_fechas.

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

La fecha ha sido creada con un date picker single, con las siguientes características:

- El mínimo de la fecha desde la cual se quiere visualizar la información se ha
    establecido en 01/01/2021 (hasta la fecha actual), con el fin de no cargar
    demasiado la página web.
- La fecha desde la cual se quiere visualizar los datos puede ser seleccionada por
    el usuario. Sin embargo, la fecha hasta la cual se pueden representar siempre
    va a ser el día de la fecha que el usuario ejecute el gráfico. La misma no permite
    selección por parte del usuario.
- La fecha se ha convertido a formato '%Y-%m-%d', por ejemplo: 2021- 01 - 01, para
    una mejor visualización y entendimiento del usuario.


## RESULTADO

Como resultado se obtiene una aplicación que incluye un gráfico interactivo de líneas
que permite visualizar la cotización de un par de criptomonedas determinado (Ejemplo:
Bitcoin/USD), en un plazo determinado de tiempo y con un intervalo especifico (Ejemplo:
1 minuto, 1440 minutos).

Gracias a la interactividad que el gráfico posee el usuario puede seleccionar el par de
criptomonedas, el intervalo, y la fecha desde la cual desea visualizar la información.

