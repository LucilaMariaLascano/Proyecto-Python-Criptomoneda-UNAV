from datetime import date, datetime

import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import pandas as pd
import numpy as np
import krakenex

class Criptomoneda:
    """
    Clase utilizada para criptomonedas
        :param self.moneda: par de criptomonedas seleccionado.
        :type moneda: str.
        :param self.intervalo: tipo de intervalo seleccionado.
        :type self.intervalo: int.
        :param self.fecha: fecha desde de la cual se quiere visualizar la información.
        :type self.fecha: timestamp.
    """

    # Atributos
    def __init__(self, moneda, intervalo, fecha):
        self.moneda = moneda
        self.intervalo = intervalo
        self.fecha = fecha

    def __str__(self):
        print(f'El par de criptomonedas seleccionado es {self.moneda}')

    # Métodos
    def obtener_cotizaciones(self):
        """
        Función para obtener las cotizaciones de criptomonedas de Kraken.
                :returns: pandas dataframe con la cotización del par de criptomonedas.

        """

        kraken = krakenex.API()
        crypto_data = kraken.query_public(
                                        'OHLC',
                                        {'pair': self.moneda,
                                         'interval': self.intervalo,
                                         'since': self.fecha
                                         }
                                          )

        return crypto_data['result'][self.moneda]


# Creación de diez pares de criptomonedas disponibles en Kraken
criptomonedas_disponibles = [("XXBTZUSD", "Bitcoin-USD"), ("XXMRZUSD", "Monero-USD"),
                             ("XXRPZUSD", "Ripple-USD"), ("XETHZUSD", "Ethereum-USD"),
                             ("XETCZUSD", "Ethereum Classic-USD"), ("XXBTZEUR", "Bitcoin-EUR"),
                             ("XXMRZEUR", "Monero-EUR"), ("XXRPZEUR", "Ripple-EUR"),
                             ("XETHZEUR", "Ethereum-EUR"), ("XETCZEUR", "Ethereum Classic-EUR")
                             ]

# Creación del listado de intervalos
intervalos_tiempo = [(1, "1 minuto"), (5, "5 minutos"), (15, "15 minutos"),
                     (30, "30 minutos"), (60, "1 hora"), (240, "4 horas"),
                     (1440, "1 día"), (10080, "7 días"), (21600, "15 días")
                     ]


# Creación del gráfico
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Cotización de las criptomonedas"
server = app.server

# Layout del gráfico
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="📈", className="header-emoji"),
                html.H1(
                    children="Cotización de las criptomonedas", className="header-title"
                ),
                html.P(
                    children="Gráfico de la cotización de las criptomonedas frente al "
                             "Dólar Estadounidense (USD) o al Euro (EUR) en el mercado "
                             "de las criptomonedas. "
                             "Fuente:@Kraken",
                    className="header-description"
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Criptomoneda", className="menu-title"),
                        dcc.Dropdown(
                            id="filtro-par-cripto",
                            options=[
                                {"label": nombre, "value": moneda}
                                for moneda, nombre in criptomonedas_disponibles
                            ],
                            value="XXBTZUSD",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Intervalo", className="menu-title"),
                        dcc.Dropdown(
                            id="intervalos-tiempo",
                            options=[
                                {"label": nombre, "value": intervalo}
                                for intervalo, nombre in intervalos_tiempo
                            ],
                            value="1440",
                            clearable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Fecha",
                            className="menu-title"
                            ),
                        dcc.DatePickerSingle(
                            id='seleccion-fechas',
                            min_date_allowed=date(2021, 1, 1),
                            max_date_allowed=date.today(),
                            initial_visible_month=date(2021, 1, 1),
                            date=date(2021, 1, 1)
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="grafica-precio", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    Output("grafica-precio", "figure"),
    [
        Input("filtro-par-cripto", "value"),
        Input("intervalos-tiempo", "value"),
        Input("seleccion-fechas", "date"),
    ],
)
def update_charts(filtro_par_cripto, intervalos_tiempo, seleccion_fechas):
    """DOCSTRING - Función que actualiza los valores del gráfico y lo crea.

            :param filtro_par_cripto: par de criptomonedas seleccionada.
            :type filtro_par_cripto: str.
            :param intervalos_tiempo: tipo de intervalo seleccionado.
            :type intervalos_tiempo: int.
            :param seleccion_fechas: fecha desde la cual se quiere visualizar la información.
            :type seleccion_fechas: timestamp.
            :returns: gráfico con la cotización del par de criptomonedas.

            """
    seleccion_fechas_int = int(datetime.strptime(seleccion_fechas, '%Y-%m-%d').timestamp())

    # Construcción del dataset.
    criptomoneda = Criptomoneda(filtro_par_cripto, intervalos_tiempo, seleccion_fechas_int)
    df = pd.DataFrame(data=criptomoneda.obtener_cotizaciones(),
                      columns=["Time", "Open", "High", "Low",
                               "Close", "VWAP", "Volume", "Count"]
                      )
    # Conversión de la fecha obtenida de Kraken al formato necesario.
    df["Date"] = pd.to_datetime(df.Time, unit='s')

    # Se convierten los precios a valor numérico para poder operar con ellos
    # porque vienen como objeto
    df["Open"] = df["Open"].apply(pd.to_numeric)
    df["High"] = df["High"].apply(pd.to_numeric)
    df["Low"] = df["Low"].apply(pd.to_numeric)
    df["Close"] = df["Close"].apply(pd.to_numeric)
    df["Volume"] = df["Volume"].apply(pd.to_numeric)

    # Calculo del VWAP
    df["VWAP_calculado"] = (np.cumsum(
                                        df.Volume * ((df.High + df.Low + df.Close) / 3)) / np.cumsum(df.Volume)
                            )
    price_chart_figure = {
            "data": [
                {
                    "x": df["Date"],
                    "y": df["Low"],
                    "type": "lines",
                    "name": "Low",
                    "hovertemplate": "$%{y:.2f}<extra></extra>",
                },
                {
                    "x": df["Date"],
                    "y": df["High"],
                    "type": "lines",
                    "name": "High",
                    "hovertemplate": "$%{y:.2f}<extra></extra>",
                },
                {
                    "x": df["Date"],
                    "y": df["VWAP_calculado"],
                    "type": "lines",
                    "name": "VWAP",
                    "line":{
                        "dash": 'dot',
                        "with": 6
                    },
                    "hovertemplate": "$%{y:.2f}<extra></extra>",
                },
            ],
            "layout": {
                "title": {
                    "text": "Evolución de los precios de las criptomonedas",
                    "x": 0.05,
                    "xanchor": "left",
                },
                "xaxis": {"fixedrange": True},
                "yaxis": {"tickprefix": "$", "fixedrange": True},
                "colorway": ["#ff0000", "#10a700", "#000000"],
            },
        }

    return price_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)
