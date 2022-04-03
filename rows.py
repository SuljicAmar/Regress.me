import dash_bootstrap_components as dbc
import dash
from dash import Input, Output, State, dcc, html, dash_table
from cards import *


rowFit = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(cardDV), width = 5),
                dbc.Col(html.Div(cardIV), width = 7)
            ], justify='center', align='center'
        ),

        dbc.Row(
            [
                dbc.Col(html.Div(cardTransform), width = 5),                
                dbc.Col(html.Div([dbc.Label('Test Data Split', className='mt-3',  style={'color': '#FFFDFD', }),
                        dcc.Slider(min=0, max=1, step=.01, value=.20, id='testsplit',tooltip={'placement': 'bottom', 'always_visible': True})]), width = 5),        
            ], justify='center', align='center'
        ),

        dbc.Row([
            dbc.Col(html.Div(dbc.Button('Fit', id='btnFit', n_clicks=0, size='sm', style={'width': '75%', }), className='mt-5'), width = 5)
            ], justify='center', align='center'),

        html.Hr(),

        dbc.Row(
            [
                dbc.Col(html.Div(cardStats), width = 10),
            ], justify='center', align='center', className='mt-2'
        ),

        dbc.Row(
            [
               dbc.Col(html.Div(cardFit), width = 7)  
            ], justify='center', align='center'
        ),

        dbc.Row(
            [
               dbc.Col(html.Div(cardFitTest), width = 7)  
            ], justify='center', align='center'
        ),

    ]
)


                              
rowViz = dbc.Container(
    [
       dbc.Row(
            [
             dbc.Col(html.Div([
                dbc.RadioItems(
                id='radioViz',
                inline=True,
                options=[
                {'label': 'Fit', 'value': 'modelfit'}, {'label': 'Residuals', 'value': 'residuals'}], style={'background-color': '#060606', 'color':'#FFFDFD', })
                ],
                ), width=5),

             dbc.Col(html.Div([
                dbc.RadioItems(
                id='radioTrainOrTest',
                inline=True,
                options=[{'label': 'Train', 'value': 'train'},
                {'label': 'Test', 'value': 'test'}
                ],value='train')]),  style={'background-color': '#060606', }, width=5),
            ], 
            justify='center', align='center', className='mt-5'),

       dbc.Row(html.Div(id='vmr'), justify='center', align='center')
       ]
    )



rowFig = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col([dbc.Label('Select a Figure', className='mt-5 mb-3', style={'color': '#FFFDFD', }),
                dcc.Dropdown(
                id='navFig',
                options=[
                {'label': 'Correlation Matrix', 'value': 'figCorr'},
                {'label': 'Scatter Plot', 'value': 'figScatter'},
                {'label': 'Line Plot', 'value': 'figLine'},
                {'label': '2D Hist', 'value': 'fig2D'},
                {'label': 'Box Plot', 'value': 'figBox'},
                {'label': 'Distribution Plot', 'value': 'figDist'},
                {'label': 'Bar Chart', 'value': 'figBar'},
                {'label': 'Histogram', 'value': 'figHist'},
                {'label': 'Pie Chart', 'value': 'figPie'},
                {'label': 'Descriptive Stats', 'value': 'ds'}
             ], style={'background-color': '#060606', 'color':'#FFFDFD', })], width=5),                           
    ], justify='center', align='center'),
        
        html.Hr(className='mt-5'),
        
        dbc.Row(
            [
                dbc.Col(id='userFig', width=12)], justify='center', align='center')     
            ]
)               

rowHome = dbc.Container([dbc.Row([dbc.Col(html.Div(jumbotronHome), width=12),], className='d-flex justify-content-center mt-5'), ],)
