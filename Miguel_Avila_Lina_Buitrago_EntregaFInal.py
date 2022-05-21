from click import style
from dash import Dash, dcc, html, Input, Output, dash_table
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import plotly.express as px

df = pd.read_excel(
    'C:\\Users\\Miguel Avila\\Desktop\\dash\\data\\arboles.xlsx')


pivote = df.pivot('Month', 'Day of Year', 'Avg Temp (C)')

no_date = df.drop(["Month", "Date", "Unnamed: 0",
                  "Year", "Day", "Day of Year"], axis=1)



fig =  px.line(df, x='Day', y='Avg Temp (C)', color='Month', symbol="Month")

pivote2 = df.pivot('Month', 'Day', 'Avg Temp (C)')

pivote33 = df[['Avg Rel Hum (%)', 'Avg Sol Rad (w/m^2)', 'Avg Wind (mph)', 'Avg Barom (mb)', 'Precip (in)',
 'Avg Temp (C)']]

#fig_2 = px.histogram(pivote33,histnorm='probability')

fig_2 = make_subplots(rows=2, cols=3)

HUMEDAD = go.Histogram(x=df["Avg Rel Hum (%)"].values,histnorm='percent')
RADIACIÓN_SOLAR = go.Histogram(y=df['Day'].values,x=df['Avg Sol Rad (w/m^2)'].values,histnorm='percent')
VELOCIDAD_VIENTO= go.Histogram(x=df['Avg Wind (mph)'].values)
PRESIÓN_ADMO = go.Histogram(x=df['Avg Barom (mb)'].values)
PRECIPITACIÓN = go.Histogram(x=df['Precip (in)'].values)
TEMPERATURA = go.Histogram(x=df['Avg Temp (C)'].values)
fig_2.append_trace(HUMEDAD, 1, 1)
fig_2.append_trace(RADIACIÓN_SOLAR, 1, 2)
fig_2.append_trace(VELOCIDAD_VIENTO, 1, 3)
fig_2.append_trace(PRESIÓN_ADMO, 2, 1)
fig_2.append_trace(PRECIPITACIÓN, 2, 2)
fig_2.append_trace(TEMPERATURA, 2, 3)

fig_3 = px.scatter(df,
                x="Month",
                y="Avg Rel Hum (%)",color="Avg Rel Hum (%)", marginal_y="histogram")

fig_4 = px.scatter_matrix(no_date, width=1400, height=1000)


fig_5 = px.bar(df, x='Day', y='Month',color='Avg Temp (C)',color_continuous_scale='RdBu_r')

app = Dash(__name__)


app.layout = html.Div(children=[
    html.Div(children=[
        html.H1(children=' Dash Reserva Hopkins Memorial Forest ')
        

    ], style={'textAlign': 'center'}),



    html.Div(children=[
        html.H1(children='Comportamiento de la temperatura en cada mes'),
        html.P(children=" insight Se logra apreciar el comportamiento de cada mes respecto a la temperatura, se puede identificar el dia y el mes exacto en el que se midio "),
        html.P(children=" la temperatura, ademas se puede despejar del grafico las series de meses si se quiere apreciar con menos meses "),
        html.P(children=" y se puede hacer zoom recortado retangularmente o en columna, ademas desplazar los ejes "),
        dcc.Graph(id='Temperaturas', figure=fig)

    ], style={'textAlign': 'center'}),

    html.Div(children=[
        html.H1(children='Histogramas de cada variable de interes'),
         html.P(children=" HUMEDAD, RADIACIÓN_SOLAR, VELOCIDAD_VIENTO"),
         html.P(children="PRESIÓN_ADMO, PRECIPITACIÓN, TEMPERATURA"),
         html.P(children="insight Se aprecian el comportamiento de las variables de interes por medio de histogramas individuales, ademas se puede hacer zoom y mover los ejes respectivamente"),
         

        dcc.Graph(id='Histograma', figure=fig_2)
    ], style={'textAlign': 'center'}),

    html.Div(children=[
        html.H1(children='Comportamiento de la Humedad en todo el año por meses'),
        html.P(children=" insight Especiamente se aprecia unicamente el comportamiento de la Humedad relativa a traves del año.   "),
        html.P(children=" se puede interactuar de la misma forma que los anteriores graficos"),
        dcc.Graph(id='HUMEDAD  ', figure=fig_3)
    ], style={'textAlign': 'center'}),

    html.Div(children=[
        html.H1(children='Matrix de dispersión'),
        html.P(children=" insight la facilidad para apreciar los comportamientos de las relaciones entre variables,ademas con zoom se puede apreciar mas de cerca   "),
        html.P(children=" insight 2. especialmente este grafico tiene una ventaja excepcional en cuanto a los recortes y movimientos de los ejes"),
         html.P(children=" insight 2. ya que al subselecionar una sección se desvanecen las observaciones que no estan dentro de este rango selecionando en las demas casillas"),
        dcc.Graph(id='Scatter matrix', figure=fig_4)
    ], style={'textAlign': 'center'}),

    html.Div(children=[
        html.H1(children='Mapa de calor de la temperatura a traves del año '),
        html.P(children=" insight especialmente se puede identificar con el cursor el dia especifico del año con su respectiva temperatura  "),
        html.P(children="de igual manera se pude interactuar, subselecionar de forma rectangular,recortar  en columna y mover los ejes"),
        dcc.Graph(id='heatmap', figure=fig_5)
    ], style={'textAlign': 'center'}),


    html.Div(children=[
        html.H1(children='Comportamiento de la Radiación Solar por meses',style={'textAlign':'center'}),
        html.P(children=" insight permite ver las agrupaciones de cada mes y se puede hacer facilmente comparaciones entre meses   "),
        html.P(children="de igual manera se pude interactuar, subselecionar de forma rectangular,recortar  en columna y mover los ejes"),
        
        dcc.Graph(id='graph-with-slider'),
        dcc.Slider(
            df['Year'].min(),
            df['Day'].max(),
            step=None,
            value=df['Year'].min(),
            marks={str(year): str(year) for year in df['Year'].unique()},
            id='year-slider'
        )
    ],style={'textAlign':'center'}),











],style={"backgroundColor":"black","color":"white","fontFamily":"arial"}

)


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df.Year == selected_year]

    fig = px.scatter(filtered_df, x="Day of Year", y="Avg Sol Rad (w/m^2)",
                     size="Day of Year", color="Month", hover_name="Month",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)