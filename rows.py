import dash_bootstrap_components as dbc
import dash
from dash import Input, Output, State, dcc, html, dash_table
from cards import *


rowFit = html.Div([
            html.Div([
                html.Div(html.P('Select variables and data split'), className = 'head-text'),
                html.Div([
                    html.Div(cardDV, className = 'quarter'),
                    html.Div(cardIV, className = 'quarter'),
                ], id = 'top-half'),
                html.Hr(),
                html.Div([
                    html.Div(cardTransform, className = 'quarter'),
                    html.Div(cardSplit, className = 'quarter'),
                ], id = 'bottom-half'),

                html.Div([
                    html.Div(html.Button('Fit', id='btnFit', n_clicks=0, className='button-fit'), id = 'button-container'),
                ], id = 'button-lightblue'),
            ], id = 'model-page-control'),

            html.Hr(className = 'horizontal-line'),
        html.Div([
            html.Div(html.P('Results'), className = 'head-text'),
            html.Div([
                    html.Div(cardStats),
                ], className = 'table'),

            html.Div([
                html.Div(cardFit),
                ],id = 'table-margin1', className = 'table'),

            html.Div([
                html.Div(cardFitTest),
                ],id = 'table-margin2', className = 'table'),
        ], id = 'tables')

    ], id = 'model-page')


                              
rowViz = html.Div([
                html.Div([
                    html.Div([
                        html.Div(html.P('Select a view', id = 'radio-text')),

                        html.Div([
                            html.Div([
                                dbc.RadioItems(
                                id='radioViz',
                                inline=True,
                                options=[
                                {'label': 'Fit', 'value': 'modelfit'}, {'label': 'Residuals', 'value': 'residuals'}])
                                ], className = 'radio-container'),
                            html.Div(id = 'vertical-line'),
                            html.Div([
                                dbc.RadioItems(
                                id='radioTrainOrTest',
                                inline=True,
                                options=[{'label': 'Train', 'value': 'train'},
                                {'label': 'Test', 'value': 'test'}
                                ],value='train')], className = 'radio-container'),
                            ], id = 'radios')
                        ], id = 'primary-radio-container')
                    ], id = 'primary-radio'),

            html.Div(id='vmr')
       ], id = 'viz-model')



rowFig = html.Div([
                html.Div([html.Div([html.P('Select a Figure', className='main-dropdown-label'),
                dcc.Dropdown(
                id='navFig',
                options=[
                {'label': 'Correlation Matrix', 'value': 'figCorr'},
                {'label': 'Scatter Plot', 'value': 'figScatter'},
                {'label': 'Bar Chart', 'value': 'figBar'},
                {'label': 'Distribution Plot', 'value': 'figDist'},
                {'label': 'Line Plot', 'value': 'figLine'},
                {'label': 'Pie Chart', 'value': 'figPie'},
                {'label': 'Scatter Matrix', 'value': 'figMatrix'},
                {'label': 'Box Plot', 'value': 'figBox'},
                {'label': 'Histogram', 'value': 'figHist'},
                {'label': '2D Contour', 'value': 'figContour2D'},
                {'label': '2D Hist', 'value': 'fig2D'},
                {'label': '3D Scatter Plot', 'value': 'figScatter3D'},
                {'label': '3D Line Plot', 'value': 'figLine3D'},
                 {'label': 'Surface Plot', 'value': 'figSurface3D'},
                {'label': 'Mesh Grid', 'value': 'figMesh'},
                {'label': 'Descriptive Stats', 'value': 'ds'}
             ])], id = 'main-dropdown-container'),                           
        
            html.Hr(className = 'horizontal-line'),], id = 'explore-page-top-section'),

            html.Div(id='userFig')
        ], id = 'all_explore_content')


#removed dbc.container
rowHome = html.Div([html.Div(jumbotronHome)], className='Home', id = "Home_Page_Column")
