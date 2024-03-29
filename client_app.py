from flask import Flask, request
from dash import Input, Output, State, dcc, html, dash_table
import dash
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import base64
import io
import numpy as np
import dash_bootstrap_components as dbc
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from models import OLS
from transformations import Standardize, MinMax
from dash_bootstrap_templates import load_figure_template
from sklearn.model_selection import train_test_split
from rows import *
import requests
from datetime import datetime
import statsmodels.api as sm
from sklearn.metrics import accuracy_score, precision_score, recall_score
import math


flask_app = Flask(__name__)
flask_app.debug = False
app = dash.Dash(__name__, server=flask_app, suppress_callback_exceptions=True, title='Regress.me',  url_base_pathname='/', external_stylesheets=[
        dbc.themes.CYBORG,
        'https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100;0,600;1,300&display=swap'
    ])
load_figure_template('cyborg')

app.layout = html.Div(children=
                      [
                          dcc.Store(id='userData'),
                          dcc.Store(id='userYhat'),
                          dcc.Store(id='userTestResidual'),
                          dcc.Store(id='userTestPred'),
                          dcc.Store(id='userTestX'),
                          dcc.Store(id='userCoefficients'),
                          dbc.Row(
                              [
                                  
                                      html.Div(
                                          dbc.Tabs(
                                              [
                                                  dbc.Tab(rowHome, tab_id='tabHome', label='Home', tab_style={'margin': 'auto'}, active_label_style={'background-color': '#2a9fd6'}),
                                                  dbc.Tab(rowFig, id='tabFigs', tab_id='tabFigsTab', label='Explore Data', tab_style={'margin': 'auto'},active_label_style={'background-color': '#2a9fd6'}, disabled=True),
                                                  dbc.Tab(rowFit, id='tabModel', label='Model', disabled=True,active_label_style={'background-color': '#2a9fd6'}, tab_style={'margin': 'auto'}),
                                                  dbc.Tab(rowViz, id='tabViz', label='Vizualize Model', disabled=True,active_label_style={'background-color': '#2a9fd6'}, tab_style={'margin': 'auto'}),
                                                  ], id='tabs', style={}, className='d-flex justify-content-center'),
                                          )
                                  ]
                              ),
                          ]
                      )



def parse_data(contents, filename):
    if contents and filename:
        try:
            content_type, content_string = contents.split(",")
            decoded = base64.b64decode(content_string)
            try:
                if 'csv' in filename:
                    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
                return df
            except Exception as e:
                return uploadError
        except Exception as exception:
            return uploadError
    else:
        raise PreventUpdate



@app.callback([Output('userData', 'data'),
               Output('tabFigs', 'disabled'),
               Output('tabModel', 'disabled'),
               Output('uploadData', 'disabled'),
               Output('uploadToolTip', 'children'),
               Output('tabs', 'active_tab'),
               Output('userDataChoiceError', 'children'),
               Output('dropDatasets', 'disabled')],
              [Input('uploadData', 'contents'),
               Input('uploadData', 'filename'),               
               Input('dropDatasets', 'value')], prevent_intial_call=True)
def updateData(contents, filename, dataset):
    try:
        else:
            if dataset:
                df = pd.read_csv('sample_datasets/{}.csv'.format(dataset))
        if isinstance(df, pd.DataFrame):
            return [df.dropna().to_json(date_format='iso', orient='split'), False, False, True, 'Refresh to upload a new dataset', 'tabFigsTab', html.Div(html.P('')), True]
        else:
            return [pd.DataFrame({'x':[1]}).to_json(date_format='iso', orient='split'), True, True, True, 'Refresh to try again', 'tabHome', df, True]
    except Exception as exception:
        raise PreventUpdate


        

@app.callback(Output('dropDV', 'options'),
              Input('userData', 'data'))
def updateDropDV(df2):
    if df2:
        try:
            df = pd.read_json(df2, orient='split')
            return [{'label': str(i), 'value': str(i)} for i in df._get_numeric_data().columns]
        except Exception as exception:
            return exception
    else:
        raise PreventUpdate

@app.callback([Output('radioIV', 'options'),
               Output('radioIV', 'value')],
              [State('userData', 'data'),
               State('dropDV', 'value'),
               State('checkIV', 'value'),
               Input('btnFit', 'n_clicks')
               ])
def updateRadioIV(df2, y, x, btn):
    if btn:
        try:
            df = pd.read_json(df2, orient='split')
            numeric_col = df.drop(columns = [y])[x]._get_numeric_data().columns
            temp = [{'label': str(i), 'value': str(i)} for i in numeric_col]
            temp.insert(0, {'label': 'None', 'value': 'none'})
            return temp, numeric_col[0]
        except Exception as exception:
            return exception
    else:
        raise PreventUpdate

@app.callback([Output('radioIV3D', 'options'),
               Output('radioIV3D', 'value'),
               Output('radioIV3DZ', 'options'),
               Output('radioIV3DZ', 'value')],
              [State('userData', 'data'),
               State('dropDV', 'value'),
               State('checkIV', 'value'),
               Input('btnFit', 'n_clicks')
               ])
def updateRadioIV3D(df2, y, x, btn):
    if btn:
        try:
            df = pd.read_json(df2, orient='split')
            numeric_col = df.drop(columns = [y])[x]._get_numeric_data().columns
            temp = [{'label': str(i), 'value': str(i)} for i in numeric_col]
            return temp, numeric_col[0], temp, numeric_col[1]
        except Exception as exception:
            return exception
    else:
        raise PreventUpdate


@app.callback([Output('filterDist', 'options'),
               Output('userXDist', 'options'),
               Output('userXDist', 'value')],
              [State('userData', 'data'),
               Input('navFig', 'value')
               ])
def updateDistOptions(df2, value):
    if value == 'figDist':
        df = pd.read_json(df2, orient='split')
        numeric_col = df._get_numeric_data().columns
        temp = []
        temp2 = []
        for i in numeric_col:
            temp.append({'label': str(i), 'value': str(i)})
        for i in df.columns:
            if i not in numeric_col:
                temp2.append({'label': str(i), 'value': str(i)})
        return temp2, temp, numeric_col[0]
    else:
        raise PreventUpdate

@app.callback([Output('filterBar', 'options'),
               Output('userXBar', 'options'),
               Output('userXBar', 'value'),
               Output('userYBar', 'options'),
               Output('userYBar', 'value')],
              [State('userData', 'data'),
               Input('navFig', 'value')
               ])
def updateBarOptions(df2, value):
    if value == 'figBar':
        df = pd.read_json(df2, orient='split')
        numeric_col = df._get_numeric_data().columns
        temp = []
        temp2 = []
        temp3 = [{'label': str(i), 'value': str(i)} for i in df.columns]
        for i in df.columns:
            if i not in numeric_col:
                temp2.append({'label': str(i), 'value': str(i)})
            else:
                temp.append({'label': str(i), 'value': str(i)})
            if is_datetime(df[i]):
                temp.append({'label': str(i), 'value': str(i)})                
        return temp3, temp3, df.columns[0], temp3, df.columns[0]
    else:
        raise PreventUpdate

@app.callback([Output('radioMatrix', 'options'),
               Output('radioMatrix', 'value'),
               Output('filterMatrix', 'options')],
              [State('userData', 'data'),
               Input('navFig', 'value')
               ])
def updateFilterMatrix(df2, value):
    if value == 'figMatrix':
        try:
            df = pd.read_json(df2, orient='split')
            numeric_col = df._get_numeric_data().columns
            temp = [{'label': str(i), 'value': str(i)} for i in numeric_col]
            temp2 = [{'label': str(i), 'value': str(i)} for i in df.columns if i not in numeric_col]
            return [temp, [numeric_col[0]], temp2] 
        except Exception as exception:
            return exception
    else:
        raise PreventUpdate


@app.callback([Output('filterhist', 'options'),
               Output('userXHist', 'options'),
               Output('userXHist', 'value')],
              [State('userData', 'data'),
               Input('navFig', 'value')
               ])
def updateHistOptions(df2, value):
    if value == 'figHist':
        df = pd.read_json(df2, orient='split')
        numeric_col = df._get_numeric_data().columns
        temp = []
        temp2 = []
        for i in df.columns:
            if i not in numeric_col:
                temp2.append({'label': str(i), 'value': str(i)})
            if is_datetime(df[i]):
                temp.append({'label': str(i), 'value': str(i)})    
        for i in numeric_col:
            temp.append({'label': str(i), 'value': str(i)})
        return temp2, temp, numeric_col[0]
    else:
        raise PreventUpdate

@app.callback([Output('filterPie', 'options'),
               Output('filterPie', 'value'),
               Output('userXPie', 'options'),
               Output('userXPie', 'value')],
              [State('userData', 'data'),
               Input('navFig', 'value')
               ])
def updatePieOptions(df2, value):
    if value == 'figPie':
        df = pd.read_json(df2, orient='split')
        numeric_col = df._get_numeric_data().columns
        temp = []
        temp2 = []
        for i in df.columns:
            if i not in numeric_col:
                temp2.append({'label': str(i), 'value': str(i)})
                rtrn = i
                if is_datetime(df[i]):
                    temp.append({'label': str(i), 'value': str(i)})    
        for i in numeric_col:
            temp.append({'label': str(i), 'value': str(i)})
        return temp2, rtrn, temp, numeric_col[0]
    else:
        raise PreventUpdate

@app.callback(Output('figBox', 'figure'),
              [State('userData', 'data'),
               Input('userYBox', 'value'),
               Input('userXBox', 'value'),
               Input('filterBox', 'value')
               ])
def updateBox(df2, y, x, filters):
    df = pd.read_json(df2, orient='split')
    fig = go.Figure()    
    if y:
        if x:
            if filters in df.columns:
                fig = px.box(df, x=x, y=y, color=filters)
            else:
                fig = px.box(df, x=x, y=y)
        else:
            fig = px.box(df, y=y)
    fig.layout.xaxis.fixedrange = False
    fig.layout.yaxis.fixedrange = False
    fig.update_layout(
                xaxis_title=x,
                paper_bgcolor='#060606',
                template='cyborg',
                plot_bgcolor='#060606',
                hoverlabel=dict(bgcolor='white', font_color='black', font_size=18),
                font_family = 'Montserrat, sans-serif',
                font_color='#FCFCFC',
                title_font_family='Arial, Helvetica, sans-serif',
                title_font_color='#FCFCFC',
                legend_title_font_color='#FFFDFD',
                hovermode='closest'
                ) 
    return fig

@app.callback(Output('figMatrix', 'figure'),
              [State('userData', 'data'),
               Input('radioMatrix', 'value'),
               Input('filterMatrix', 'value')
               ])
def updateMatrix(df2, x, filters):
    df = pd.read_json(df2, orient='split')
    fig = go.Figure()    
    if x:
        if filters:
            fig = px.scatter_matrix(df,dimensions=x,color=filters)
        else:
            fig = px.scatter_matrix(df,dimensions=x)
    fig.layout.xaxis.fixedrange = False
    fig.layout.yaxis.fixedrange = False
    fig.update_layout(
                paper_bgcolor='#060606',
                template='cyborg',
                plot_bgcolor='#060606',
                hoverlabel=dict(bgcolor='white', font_color='black', font_size=18),
                font_family = 'Montserrat, sans-serif',
                font_color='#FCFCFC',
                legend_title_font_color='#FFFDFD',
                ) 
    return fig

@app.callback([Output('filterBox', 'options'),
               Output('userXBox', 'options'),
               Output('userYBox', 'options'),
               Output('userYBox', 'value'),],
              [State('userData', 'data'),
               Input('navFig', 'value')
               ])
def updateBoxOptions(df2, x):
    if x:
        df = pd.read_json(df2, orient='split')
        numeric_col = df._get_numeric_data().columns
        temp = []
        temp2 = []
        for i in df.columns:
            if i not in numeric_col:
                temp2.append({'label': str(i), 'value': str(i)})
            if is_datetime(df[i]):
                temp.append({'label': str(i), 'value': str(i)}) 
                temp2.append({'label': str(i), 'value': str(i)}) 
        for i in numeric_col:
            temp.append({'label': str(i), 'value': str(i)})       
        return [temp2, temp2, temp, numeric_col[0]]
    else:
        raise PreventUpdate
                   
@app.callback(Output('valueCorr', 'options'),
              [State('userData', 'data'),
               Input('filterCorr', 'value')], prevent_initial_call=True)
def updateCorrValue(df2, value):
    if value:
        df = pd.read_json(df2, orient='split')
        temp = [{'label': str(i), 'value': str(i)} for i in df[value].unique().tolist()]     
        return temp
    else:
        raise PreventUpdate


@app.callback(Output('filterCorr', 'options'),
              [State('userData', 'data'),
               Input('navFig', 'value')])
def updateCorrOptions(df2, x):
    if x == 'figCorr':
        df = pd.read_json(df2, orient='split')
        numeric_col = df._get_numeric_data().columns
        temp2 = []
        for i in df.columns:
            if i not in numeric_col:
                temp2.append({'label': str(i), 'value': str(i)})
        return temp2
    else:
        raise PreventUpdate

@app.callback([Output('userXScatter', 'options'),
               Output('userXScatter', 'value'),
               Output('userYScatter', 'options'),
               Output('userYScatter', 'value'),
               Output('filterScatter', 'options'),
               Output('filterScatterRow', 'options'),
               Output('filterScatterCol', 'options')],
              [State('userData', 'data'),
               Input('navFig', 'value')
               ])
def updateScatterChoice(df2, x):
    if x == 'figScatter':
        df = pd.read_json(df2, orient='split')
        numeric_col = df._get_numeric_data().columns
        temp = []
        temp2 = []
        for i in df.columns:
            if i not in numeric_col:
                temp2.append({'label': str(i), 'value': str(i)})
            temp.append({'label': str(i), 'value': str(i)})    
        return [temp, str(numeric_col[0]), temp, str(numeric_col[0]), temp, temp2, temp2]
    else:
        raise PreventUpdate

@app.callback([Output('userXScatter3D', 'options'),
               Output('userXScatter3D', 'value'),
               Output('userYScatter3D', 'options'),
               Output('userYScatter3D', 'value'),
               Output('userZScatter3D', 'options'),
               Output('userZScatter3D', 'value'),
               Output('filterScatter3D', 'options')],
              [State('userData', 'data'),
               Input('navFig', 'value')
               ])
def updateScatterChoice3D(df2, x):
    if x == 'figScatter3D':
        df = pd.read_json(df2, orient='split')
        numeric_col = df._get_numeric_data().columns
        temp = []
        temp2 = []
        for i in df.columns:
            if i not in numeric_col:
                temp2.append({'label': str(i), 'value': str(i)})
            if is_datetime(df[i]):
                temp.append({'label': str(i), 'value': str(i)})    
        for i in numeric_col:
            temp.append({'label': str(i), 'value': str(i)})
        return [temp, str(numeric_col[0]), temp, str(numeric_col[0]), temp, str(numeric_col[0]), temp2]
    else:
        raise PreventUpdate


@app.callback([Output('userXMesh3D', 'options'),
               Output('userXMesh3D', 'value'),
               Output('userYMesh3D', 'options'),
               Output('userYMesh3D', 'value'),
               Output('userZMesh3D', 'options'),
               Output('userZMesh3D', 'value')],
              [State('userData', 'data'),
               Input('navFig', 'value')
               ])
def updateMeshChoice3D(df2, x):
    if x == 'figMesh':
        df = pd.read_json(df2, orient='split')
        numeric_col = df._get_numeric_data().columns
        temp = []
        temp2 = []
        for i in df.columns:
            if i not in numeric_col:
                temp2.append({'label': str(i), 'value': str(i)})
            if is_datetime(df[i]):
                temp.append({'label': str(i), 'value': str(i)})    
        for i in numeric_col:
            temp.append({'label': str(i), 'value': str(i)})
        return [temp, str(numeric_col[0]), temp, str(numeric_col[1]), temp, str(numeric_col[2])]
    else:
        raise PreventUpdate


@app.callback([Output('userXLine', 'options'),
               Output('userXLine', 'value'),
               Output('userYLine', 'options'),
               Output('userYLine', 'value'),
               Output('filterLine', 'options')],
              [State('userData', 'data'),
               Input('navFig', 'value')
               ])
def updateLineChoice(df2, x):
    if x == 'figLine':
        df = pd.read_json(df2, orient='split')
        numeric_col = df._get_numeric_data().columns
        temp = []
        temp2 = []
        for i in df.columns:
            if i not in numeric_col:
                temp2.append({'label': str(i), 'value': str(i)})
            if is_datetime(df[i]):
                temp.append({'label': str(i), 'value': str(i)})    
        for i in numeric_col:
            temp.append({'label': str(i), 'value': str(i)})
        return [temp, str(numeric_col[0]), temp, str(numeric_col[0]), temp2]
    else:
        raise PreventUpdate

@app.callback([Output('userXLine3D', 'options'),
               Output('userXLine3D', 'value'),
               Output('userYLine3D', 'options'),
               Output('userYLine3D', 'value'),
               Output('userZLine3D', 'options'),
               Output('userZLine3D', 'value'),
               Output('filterLine3D', 'options')],
              [State('userData', 'data'),
               Input('navFig', 'value')
               ])
def updateLineChoice(df2, x):
    if x == 'figLine3D':
        df = pd.read_json(df2, orient='split')
        numeric_col = df._get_numeric_data().columns
        temp = []
        temp2 = []
        for i in df.columns:
            if i not in numeric_col:
                temp2.append({'label': str(i), 'value': str(i)})
            if is_datetime(df[i]):
                temp.append({'label': str(i), 'value': str(i)})    
        for i in numeric_col:
            temp.append({'label': str(i), 'value': str(i)})
        return [temp, str(numeric_col[0]), temp, str(numeric_col[0]), temp, str(numeric_col[0]), temp2]
    else:
        raise PreventUpdate

@app.callback([Output('userX2D', 'options'),
               Output('userX2D', 'value'),
               Output('userY2D', 'options'),
               Output('userY2D', 'value'),
               Output('filter2DRow', 'options'),
               Output('filter2DColumn', 'options')],
              [State('userData', 'data'),
               Input('navFig', 'value')
               ])
def update2DOptions(df2, x):
    if x == 'fig2D':
        df = pd.read_json(df2, orient='split')
        numeric_col = df._get_numeric_data().columns
        temp = []
        temp2 = []
        for i in df.columns:
            if i not in numeric_col:
                temp2.append({'label': str(i), 'value': str(i)})
            if is_datetime(df[i]):
                temp.append({'label': str(i), 'value': str(i)})    
        for i in numeric_col:
            temp.append({'label': str(i), 'value': str(i)})
        return [temp, str(numeric_col[0]), temp, str(numeric_col[0]), temp2, temp2]
    else:
        raise PreventUpdate

@app.callback([Output('userXContour2D', 'options'),
               Output('userXContour2D', 'value'),
               Output('userYContour2D', 'options'),
               Output('userYContour2D', 'value')],
              [State('userData', 'data'),
               Input('navFig', 'value')
               ])
def updateContour2DOptions(df2, x):
    if x == 'figContour2D':
        df = pd.read_json(df2, orient='split')
        numeric_col = df._get_numeric_data().columns
        temp = []
        temp2 = []
        for i in df.columns:
            if i not in numeric_col:
                temp2.append({'label': str(i), 'value': str(i)})
            if is_datetime(df[i]):
                temp.append({'label': str(i), 'value': str(i)})    
        for i in numeric_col:
            temp.append({'label': str(i), 'value': str(i)})
        return [temp, str(numeric_col[0]), temp, str(numeric_col[0])]
    else:
        raise PreventUpdate

@app.callback(Output('figDist', 'figure'),
              [State('userData', 'data'),
               Input('userXDist', 'value'),
               Input('filterDist', 'value'),
               Input('normalize', 'value')
               ])
def updateDist(df2, x, filters, norm):
    df = pd.read_json(df2, orient='split')
    fig = go.Figure()
    if filters in df.columns:
        if norm == ['yes']:
            fig =  ff.create_distplot([df.loc[df[filters] == i][x].values for i in pd.unique(df[filters])], [i for i in pd.unique(df[filters])], show_hist=False, show_rug=False, curve_type='normal')
        else:
            fig =  ff.create_distplot([df.loc[df[filters] == i][x].values for i in pd.unique(df[filters])], [i for i in pd.unique(df[filters])], show_hist=False, show_rug=False)
    else:
        if norm == ['yes']:
            fig = ff.create_distplot([df[x].values], [x], show_hist=False, show_rug=False, curve_type='normal')
        else:
            fig = ff.create_distplot([df[x].values], [x], show_hist=False, show_rug=False)
    fig.layout.hovermode = False
    fig.layout.xaxis.fixedrange = False
    fig.layout.yaxis.fixedrange = False
    fig.update_yaxes(automargin=True)
    fig.update_xaxes(automargin=True)
    fig.update_layout(
                yaxis_visible = False,
                xaxis_title=x,
                template='cyborg',
                paper_bgcolor='#060606',
                plot_bgcolor='#060606',
                font_family = 'Montserrat, sans-serif',
                font_color='#FCFCFC',
                legend_title_font_color='#FFFDFD',
                autosize=True
                ) 
    return fig

@app.callback(Output('fig2D', 'figure'),
              [State('userData', 'data'),
               Input('userX2D', 'value'),
               Input('userY2D', 'value'),
               Input('filter2DRow', 'value'),
               Input('filter2DColumn', 'value')
               ])
def update2D(df2, x, y, r, c):
    df = pd.read_json(df2, orient='split')
    if r in df.columns or c in df.columns:   
        fig =  px.density_heatmap(df, x=x, y=y, facet_row=r, facet_col=c)
    else:
        fig = px.density_heatmap(df, x=x, y=y)
    fig.layout.xaxis.fixedrange = False
    fig.layout.yaxis.fixedrange = False
    fig.update_yaxes(automargin=True)
    fig.update_xaxes(automargin=True)
    fig.update_layout(
                yaxis_visible = False,
                xaxis_title=x,
                autosize=True,
                template='cyborg',
                paper_bgcolor='#060606',
                plot_bgcolor='#060606',
                hoverlabel=dict(bgcolor='white', font_color='black', font_size=18),
                font_family = 'Montserrat, sans-serif',
                font_color='#FCFCFC',
                title_font_family='Arial, Helvetica, sans-serif',
                title_font_color='#FCFCFC',
                legend_title_font_color='#FFFDFD',
                hovermode='closest'
                ) 
    return fig

@app.callback(Output('figContour2D', 'figure'),
              [State('userData', 'data'),
               Input('userXContour2D', 'value'),
               Input('userYContour2D', 'value')
               ])
def updateContour2D(df2, x, y):
    df = pd.read_json(df2, orient='split')
    fig = go.Figure(go.Histogram2dContour(x = df[x],y = df[y],
                    hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>' + 'Count' + ': %{z}'))
    fig.layout.xaxis.fixedrange = False
    fig.layout.yaxis.fixedrange = False
    fig.update_yaxes(automargin=True)
    fig.update_xaxes(automargin=True)
    fig.update_layout(
                yaxis_visible = False,
                xaxis_title=x,
                autosize=True,
                template='cyborg',
                paper_bgcolor='#060606',
                plot_bgcolor='#060606',
                hoverlabel=dict(bgcolor='white', font_color='black', font_size=18),
                font_family = 'Montserrat, sans-serif',
                font_color='#FCFCFC',
                title_font_family='Arial, Helvetica, sans-serif',
                title_font_color='#FCFCFC',
                legend_title_font_color='#FFFDFD',
                hovermode='closest'
                ) 
    return fig

@app.callback(Output('figBar', 'figure'),
              [State('userData', 'data'),
               Input('userXBar', 'value'),
               Input('userYBar', 'value'),
               Input('filterBar', 'value')
               ])
def updateBar(df2, x, y, filters):
    df = pd.read_json(df2, orient='split')
    if filters in df.columns:   
        fig =  px.bar(df, x=x, y=y, color=filters)
    else:
        fig = px.bar(df, x=x, y=y)
    fig.layout.xaxis.fixedrange = False
    fig.layout.yaxis.fixedrange = False
    fig.update_yaxes(automargin=True)
    fig.update_xaxes(automargin=True)
    fig.update_layout(
                xaxis_title=x,
                paper_bgcolor='#060606',
                plot_bgcolor='#060606',
                autosize=True,
                template='cyborg',
                hoverlabel=dict(bgcolor='white', font_color='black', font_size=18),
                font_family = 'Montserrat, sans-serif',
                font_color='#FCFCFC',
                title_font_family='Arial, Helvetica, sans-serif',
                title_font_color='#FCFCFC',
                legend_title_font_color='#FFFDFD'
                ) 
    return fig


@app.callback(Output('figPie', 'figure'),
              [State('userData', 'data'),
               Input('userXPie', 'value'),
               Input('filterPie', 'value')
               ])
def updatePie(df2, x, filters):
    if x:
        df = pd.read_json(df2, orient='split')
        fig = px.pie(df, values=x, names=filters)
        fig.update_yaxes(automargin=True)
        fig.update_xaxes(automargin=True)
        fig.layout.xaxis.fixedrange = False
        fig.layout.yaxis.fixedrange = False
        fig.update_layout(
                    xaxis_title=x,
                    paper_bgcolor='#060606',
                    autosize=True,
                    template='cyborg',
                    plot_bgcolor='#060606',
                    hoverlabel=dict(bgcolor='white', font_color='black', font_size=18),
                    font_family = 'Montserrat, sans-serif',
                    font_color='#FCFCFC',
                    legend_title_font_color='#FFFDFD',
                    hovermode='closest'
                    ) 
        fig.update_traces(textfont_size=15, marker=dict(line=dict(color='#000000', width=2)))
        return fig
    else:
        raise PreventUpdate

@app.callback(Output('figHist', 'figure'),
              [State('userData', 'data'),
               Input('userXHist', 'value'),
               Input('filterhist', 'value')
               ])
def updateHist(df2, x, filters):
    df = pd.read_json(df2, orient='split')
    fig = go.Figure()
    if filters in df.columns:   
        fig =  px.histogram(df, x, color=filters)
    else:
        fig =  px.histogram(df, x)
    fig.update_yaxes(automargin=True)
    fig.update_xaxes(automargin=True)
    fig.layout.xaxis.fixedrange = False
    fig.layout.yaxis.fixedrange = False
    fig.update_layout(
                xaxis_title=x,
                paper_bgcolor='#060606',
                autosize=True,
                template='cyborg',
                hoverlabel=dict(bgcolor='white', font_color='black', font_size=18),
                plot_bgcolor='#060606',
                font_family = 'Montserrat, sans-serif',
                font_color='#FCFCFC',
                legend_title_font_color='#FFFDFD'
                ) 
    return fig


@app.callback(Output('figScatter', 'figure'),
              [State('userData', 'data'),
               Input('userXScatter', 'value'),
               Input('userYScatter', 'value'),
               Input('filterScatter', 'value'),
               Input('filterScatterRow', 'value'),
               Input('filterScatterCol', 'value')])
def updateScatter(df2, x, y, filters, row, col):
    df = pd.read_json(df2, orient='split')
    fig = go.Figure()
    if filters in df.columns:
        if row:           
            if col:
                fig = px.scatter(df.sort_values(by=x), x=x, y=y, color=filters, facet_row=row, facet_col=col)
            else:
                fig = px.scatter(df.sort_values(by=x), x=x, y=y, color=filters, facet_row=row)
        else:
            fig = px.scatter(df.sort_values(by=x), x=x, y=y, color=filters)
    else:
        if row:
            if col:
                fig = px.scatter(df.sort_values(by=x), x=x, y=y, facet_row=row, facet_col=col)
            else:
                fig = px.scatter(df.sort_values(by=x), x=x, y=y, facet_row=row)
        else:
            if col:
                fig = px.scatter(df.sort_values(by=x), x=x, y=y, facet_col=col)
            else:
                fig = px.scatter(df.sort_values(by=x), x=x, y=y)
    fig.update_yaxes(automargin=True)
    fig.update_xaxes(automargin=True)
    fig.layout.xaxis.fixedrange = False
    fig.layout.yaxis.fixedrange = False
    fig.update_layout(
                xaxis_title=x,
                hoverlabel=dict(bgcolor='white', font_color='black', font_size=18),
                yaxis_title=y,
                autosize=True,
                template='cyborg',
                paper_bgcolor='#060606',
                plot_bgcolor='#060606',
                font_family = 'Montserrat, sans-serif',
                font_color='#FCFCFC',
                legend_title_font_color='#FFFDFD',
                hovermode='closest'
                ) 
    return fig

@app.callback(Output('figScatter3D', 'figure'),
              [State('userData', 'data'),
               Input('userXScatter3D', 'value'),
               Input('userYScatter3D', 'value'),
               Input('userZScatter3D', 'value'),
               Input('filterScatter3D', 'value')])
def updateScatter3D(df2, x, y, z, filters):
    df = pd.read_json(df2, orient='split')
    fig = go.Figure()
    if filters in df.columns:
        for i in df[filters].unique():
            fig.add_scatter3d(x=df.loc[df[filters] == i].sort_values(by=x)[x].values, y=df.loc[df[filters] == i].sort_values(by=x)[y].values, z=df.loc[df[filters] == i].sort_values(by=x)[z].values,
                                        mode='markers',
                                        name=i, 
                                        marker=dict(size=5),
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>' + str(z) + ': %{z}')
    else:
        fig.add_trace(go.Scatter3d(x=df.sort_values(by=x)[x].values, y=df.sort_values(by=x)[y].values, z=df.sort_values(by=x)[z].values,
                                    mode='markers',
                                    marker=dict(size=5),
                                    hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>' + str(z) + ': %{z}'))
    fig.update_yaxes(automargin=True)
    fig.update_xaxes(automargin=True)
    fig.layout.xaxis.fixedrange = False
    fig.layout.yaxis.fixedrange = False
    fig.update_layout(
                hoverlabel=dict(bgcolor='white', font_color='black', font_size=18),
                scene=dict(xaxis_title=x,yaxis_title=y,zaxis_title=z),
                template='cyborg',
                autosize=True,
                paper_bgcolor='#060606',
                plot_bgcolor='#060606',
                font_family = 'Montserrat, sans-serif',
                font_color='#FCFCFC',
                legend_title_font_color='#FFFDFD',
                hovermode='closest'
                ) 
    return fig

@app.callback(Output('figSurface3D', 'figure'),
              [State('userData', 'data'),
               Input('navFig', 'value')])
def updateSurface3D(df2, x):
    if x == 'figSurface3D':
        df = pd.read_json(df2, orient='split')
        fig = go.Figure(go.Surface(z=df._get_numeric_data()))
        fig.update_yaxes(automargin=True)
        fig.update_xaxes(automargin=True)
        fig.layout.xaxis.fixedrange = False
        fig.layout.yaxis.fixedrange = False
        fig.update_traces(contours_z=dict(show=True, usecolormap=True,
                                  highlightcolor="limegreen", project_z=True))
        fig.update_layout(
                    hoverlabel=dict(bgcolor='white', font_color='black', font_size=18),
                    template='cyborg',
                    scene=dict(xaxis_title='',yaxis_title='',zaxis_title=''),
                    autosize=True,
                    hovermode=False,
                    paper_bgcolor='#060606',
                    scene_camera_eye=dict(x=1.87, y=0.88, z=-0.64),
                    plot_bgcolor='#060606',
                    font_family = 'Montserrat, sans-serif',
                    font_color='#FCFCFC',
                    legend_title_font_color='#FFFDFD',
                    ) 
        return fig
    else:
        raise PreventUpdate

@app.callback(Output('figMesh3D', 'figure'),
              [State('userData', 'data'),
               Input('userXMesh3D', 'value'),
               Input('userYMesh3D', 'value'),
               Input('userZMesh3D', 'value')])
def updateMesh3D(df2, x, y, z):
    df = pd.read_json(df2, orient='split')
    fig = go.Figure()
    fig.add_trace(go.Mesh3d(x=df[x], y=df[y], z=df[z], opacity=.5,
                 hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>' + str(z) + ': %{z}'))
    fig.update_yaxes(automargin=True)
    fig.update_xaxes(automargin=True)
    fig.layout.xaxis.fixedrange = False
    fig.layout.yaxis.fixedrange = False
    fig.update_layout(
                hoverlabel=dict(bgcolor='white', font_color='black', font_size=18),
                scene=dict(xaxis_title=x,yaxis_title=y,zaxis_title=z),
                template='cyborg',
                autosize=True,
                paper_bgcolor='#060606',
                plot_bgcolor='#060606',
                font_family = 'Montserrat, sans-serif',
                font_color='#FCFCFC',
                legend_title_font_color='#FFFDFD',
                hovermode='closest'
                ) 
    return fig

@app.callback(Output('figLine', 'figure'),
              [State('userData', 'data'),
               Input('userXLine', 'value'),
               Input('userYLine', 'value'),
               Input('filterLine', 'value')
               ])
def updateLine(df2, x, y, filters):
    df = pd.read_json(df2, orient='split')
    fig = go.Figure()
    if filters in df.columns:
        for i in df[filters].unique():
            fig.add_trace(go.Scattergl(x=df.loc[df[filters] == i].sort_values(by=x)[x].values, y=df.loc[df[filters] == i].sort_values(by=x)[y].values,
                                mode='lines',
                                hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>',
                                name=i))
    else:
        fig.add_trace(go.Scattergl(x=df.sort_values(by=x)[x].values, y=df.sort_values(by=x)[y].values,
                                mode='lines',
                                hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>',
                                name=x))

    fig.update_yaxes(automargin=True)
    fig.update_xaxes(automargin=True)
    fig.layout.xaxis.fixedrange = False
    fig.layout.yaxis.fixedrange = False
    fig.update_layout(
                xaxis_title=x,
                yaxis_title=y,
                autosize=True,
                hoverlabel=dict(bgcolor='white', font_color='black', font_size=18),
                paper_bgcolor='#060606',
                plot_bgcolor='#060606',
                font_family = 'Montserrat, sans-serif',
                font_color='#FCFCFC',
                template='cyborg',
                title_font_family='Arial, Helvetica, sans-serif',
                title_font_color='#FCFCFC',
                legend_title_font_color='#FFFDFD',
                hovermode='closest'
                ) 
    return fig

@app.callback(Output('figLine3D', 'figure'),
              [State('userData', 'data'),
               Input('userXLine3D', 'value'),
               Input('userYLine3D', 'value'),
               Input('userZLine3D', 'value'),
               Input('filterLine3D', 'value')
               ])
def updateLine3D(df2, x, y, z, filters):
    df = pd.read_json(df2, orient='split')
    fig = go.Figure()
    if filters in df.columns:
        for i in df[filters].unique():
            fig.add_scatter3d(x=df.loc[df[filters] == i].sort_values(by=x)[x].values, y=df.loc[df[filters] == i].sort_values(by=x)[y].values, z=df.loc[df[filters] == i].sort_values(by=x)[z].values,
                                        mode='lines',
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>' + str(z) + ': %{z}',
                                        name=i)
    else:
        fig.add_trace(go.Scatter3d(x=df.sort_values(by=x)[x].values, y=df.sort_values(by=x)[y].values, z=df.sort_values(by=x)[z].values,
                                    hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>' + str(z) + ': %{z}',
                                    mode='lines'))
    fig.update_yaxes(automargin=True)
    fig.update_xaxes(automargin=True)
    fig.layout.xaxis.fixedrange = False
    fig.layout.yaxis.fixedrange = False
    fig.update_layout(
                scene=dict(xaxis_title=x,yaxis_title=y,zaxis_title=z),
                hoverlabel=dict(bgcolor='white', font_color='black', font_size=18),
                paper_bgcolor='#060606',
                plot_bgcolor='#060606',
                autosize=True,
                font_family = 'Montserrat, sans-serif',
                font_color='#FCFCFC',
                template='cyborg',
                title_font_family='Arial, Helvetica, sans-serif',
                title_font_color='#FCFCFC',
                legend_title_font_color='#FFFDFD',
                hovermode='closest'
                ) 
    return fig

@app.callback(Output('figFit', 'figure'),
              [State('userYhat', 'data'),             
              Input('radioIV', 'value'),
              State('dropDV', 'value'),
              State('radioTransform', 'value'),
              Input('btnFit', 'n_clicks'),
              Input('radioTrainOrTest', 'value'),
              Input('userTestX', 'data')
               ], prevent_initial_call=True)
def updateFitFigure(df2, x, y, transformation, btn, TrainOrTest, xtest):
    fig = go.Figure()
    if btn:  
        if x:
            if str(TrainOrTest) == 'train':
                df = pd.read_json(df2)
            elif str(TrainOrTest) == 'test':
                df = pd.read_json(xtest)
            if sorted(df[y].unique()) == [0, 1]:
                if transformation == 'standardize':
                    if 'none' in x:
                        fig.add_trace(go.Scattergl(x=[i for i in range(df.shape[0])], y=df[y].values,
                                        mode='markers',
                                        name='True',
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))
                        fig.add_trace(go.Scattergl(x=[i for i in range(df.shape[0])], y=df['userYhat'].values,
                                        mode='markers',
                                        name='Pred Probability',
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))
                    else:
                        fig.add_trace(go.Scattergl(x=Standardize(df.sort_values(by=x)[x].values), y=df.sort_values(by=x)[y].values,
                                        mode='markers',
                                        name=x,
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))
                        fig.add_trace(go.Scattergl(x=Standardize(df.sort_values(by=x)[x].values), y=df.sort_values(by=x)['userYhat'].values,
                                        mode='markers',
                                        name='Pred Probability',
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))
                elif transformation == 'minmax':
                    if 'none' in x:
                        fig.add_trace(go.Scattergl(x=[i for i in range(df.shape[0])], y=df[y].values,
                                        mode='markers',
                                        name='True',
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))
                        fig.add_trace(go.Scattergl(x=[i for i in range(df.shape[0])], y=df['userYhat'].values,
                                        mode='markers',
                                        name='Pred Probability',
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))
                    else:
                        fig.add_trace(go.Scattergl(x=MinMax(df.sort_values(by=x)[x].values), y=df.sort_values(by=x)[y].values,
                                        mode='markers',
                                        name=x,
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))
                        fig.add_trace(go.Scattergl(x=MinMax(df.sort_values(by=x)[x].values), y=df.sort_values(by=x)['userYhat'].values,
                                        mode='markers',
                                        name='Pred Probability',
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))   
                else:
                    if 'none' in x:
                        fig.add_trace(go.Scattergl(x=[i for i in range(df.shape[0])], y=df[y].values,
                                        mode='markers',
                                        name='True',
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))
                        fig.add_trace(go.Scattergl(x=[i for i in range(df.shape[0])], y=df['userYhat'].values,
                                        mode='markers',
                                        name='Pred Probability',
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))
                    else:
                        fig.add_trace(go.Scattergl(x=df[x], y=df[y],
                                        mode='markers',
                                        name=x,
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))
                        fig.add_trace(go.Scattergl(x=df.sort_values(by=x)[x], y=df.sort_values(by=x)['userYhat'],
                                        mode='markers',
                                        name='Pred Probability',
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))
            else:
                if transformation == 'standardize':
                    if 'none' in x:
                        fig.add_trace(go.Scattergl(x=[i for i in range(df.shape[0])], y=df[y].values,
                                        mode='lines',
                                        name='True',
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))
                        fig.add_trace(go.Scattergl(x=[i for i in range(df.shape[0])], y=df['userYhat'].values,
                                        mode='lines',
                                        name='Pred',
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))
                    else:
                        fig.add_trace(go.Scattergl(x=Standardize(df.sort_values(by=x)[x].values), y=df.sort_values(by=x)[y].values,
                                        mode='markers',
                                        name=x,
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))
                        fig.add_trace(go.Scattergl(x=Standardize(df.sort_values(by=x)[x].values), y=df.sort_values(by=x)['userYhat'].values,
                                        mode='lines',
                                        name='OLS Best Fit',
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))
                elif transformation == 'minmax':
                    if 'none' in x:
                        fig.add_trace(go.Scattergl(x=[i for i in range(df.shape[0])], y=df[y].values,
                                        mode='lines',
                                        name='True',
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))
                        fig.add_trace(go.Scattergl(x=[i for i in range(df.shape[0])], y=df['userYhat'].values,
                                        mode='lines',
                                        name='Pred',
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))
                    else:
                        fig.add_trace(go.Scattergl(x=MinMax(df.sort_values(by=x)[x].values), y=df.sort_values(by=x)[y].values,
                                        mode='markers',
                                        name=x,
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))
                        fig.add_trace(go.Scattergl(x=MinMax(df.sort_values(by=x)[x].values), y=df.sort_values(by=x)['userYhat'].values,
                                        mode='lines',
                                        name='OLS Best Fit',
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))   
                else:
                    if 'none' in x:
                        fig.add_trace(go.Scattergl(x=[i for i in range(df.shape[0])], y=df[y].values,
                                        mode='lines',
                                        name='True',
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))
                        fig.add_trace(go.Scattergl(x=[i for i in range(df.shape[0])], y=df['userYhat'].values,
                                        mode='lines',
                                        name='Pred',
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))
                    else:
                        fig.add_trace(go.Scattergl(x=df[x], y=df[y],
                                        mode='markers',
                                        name=x,
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))
                        fig.add_trace(go.Scattergl(x=df.sort_values(by=x)[x], y=df.sort_values(by=x)['userYhat'],
                                        mode='lines',
                                        name='OLS Best Fit',
                                        hovertemplate = str(x) + ': %{x}<br>' +  str(y) + ': %{y}<br>'))
            fig.layout.xaxis.fixedrange = False
            fig.update_yaxes(automargin=True)
            fig.update_xaxes(automargin=True)
            fig.layout.yaxis.fixedrange = False
            fig.update_layout(
                    xaxis_title=x,
                    yaxis_title=y,
                    hoverlabel=dict(bgcolor='white', font_color='black', font_size=18),
                    paper_bgcolor='#060606',
                    plot_bgcolor='#060606',
                    template='cyborg',
                    autosize=True,
                    font_family = 'Montserrat, sans-serif',
                    font_color='#FCFCFC',
                    title_font_family='Arial, Helvetica, sans-serif',
                    title_font_color='#FCFCFC',
                    legend_title_font_color='#FFFDFD',
                    hovermode='closest'
                    )           
            return fig
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(Output('figFit3D', 'figure'),
              [State('userYhat', 'data'),             
              Input('radioIV3D', 'value'),
              Input('radioIV3DZ', 'value'),
              State('dropDV', 'value'),
              State('radioTransform', 'value'),
              Input('btnFit', 'n_clicks'),
              Input('radioTrainOrTest', 'value'),
              Input('userTestX', 'data'),
              Input('userCoefficients', 'data'),
               ], prevent_initial_call=True)
def updateFitFigure3D(df2, x, z, y, transformation, btn, TrainOrTest, xtest, coef):
    fig = go.Figure()
    if btn:  
        if x:
            if str(TrainOrTest) == 'train':
                df = pd.read_json(df2)
            elif str(TrainOrTest) == 'test':
                df = pd.read_json(xtest)
            betas = pd.read_json(coef)
            if transformation == 'standardize':
                if sorted(df[y].unique()) == [0, 1]:
                    fig.add_trace(go.Scatter3d(x=Standardize(df.sort_values(by=x)[x].values), y=Standardize(df.sort_values(by=x)[z].values), z=df.sort_values(by=x)[y].values,
                                    mode='markers',
                                    marker=dict(size=5),
                                    name='Sample',
                                    hovertemplate = str(y) + ': %{z}<br>' + str(x) + ': %{x}<br>' + str(z) + ': %{y}<br>'))
                    fig.add_trace(go.Scatter3d(x=Standardize(df.sort_values(by=x)[x].values), y=Standardize(df.sort_values(by=x)[z].values), z=df.sort_values(by=x)['userYhat'].values,
                                    mode='markers',
                                    name='Pred Probability',
                                    hovertemplate = str(y) + ': %{z}<br>' + str(x) + ': %{x}<br>' + str(z) + ': %{y}<br>'))
                else:
                    fig.add_trace(go.Scatter3d(x=Standardize(df.sort_values(by=x)[x].values), y=Standardize(df.sort_values(by=x)[z].values), z=df.sort_values(by=x)[y].values,
                                    mode='markers',
                                    marker=dict(size=5),
                                    name='Sample',
                                    hovertemplate = str(y) + ': %{z}<br>' + str(x) + ': %{x}<br>' + str(z) + ': %{y}<br>'))
                    fig.add_trace(go.Scatter3d(x=Standardize(df.sort_values(by=x)[x].values), y=Standardize(df.sort_values(by=x)[z].values), z=df.sort_values(by=x)['userYhat'].values,
                                    mode='lines',
                                    name='Model Fit',
                                    hovertemplate = str(y) + ': %{z}<br>' + str(x) + ': %{x}<br>' + str(z) + ': %{y}<br>'))
            elif transformation == 'minmax':
              if sorted(df[y].unique()) == [0, 1]:
                    fig.add_trace(go.Scatter3d(x=MinMax(df.sort_values(by=x)[x].values), y=MinMax(df.sort_values(by=x)[z].values), z=df.sort_values(by=x)[y].values,
                                        mode='markers',
                                        marker=dict(size=5),
                                        name='Sample',
                                        hovertemplate = str(y) + ': %{z}<br>' + str(x) + ': %{x}<br>' + str(z) + ': %{y}<br>'))
                    fig.add_trace(go.Scatter3d(x=MinMax(df.sort_values(by=x)[x].values), y=MinMax(df.sort_values(by=x)[z].values), z=df.sort_values(by=x)['userYhat'].values,
                                        mode='markers',
                                        name='Pred Probability',
                                        hovertemplate = str(y) + ': %{z}<br>' + str(x) + ': %{x}<br>' + str(z) + ': %{y}<br>')) 
              else:
                    fig.add_trace(go.Scatter3d(x=MinMax(df.sort_values(by=x)[x].values), y=MinMax(df.sort_values(by=x)[z].values), z=df.sort_values(by=x)[y].values,
                                        mode='markers',
                                        marker=dict(size=5),
                                        name='Sample',
                                        hovertemplate = str(y) + ': %{z}<br>' + str(x) + ': %{x}<br>' + str(z) + ': %{y}<br>'))
                    fig.add_trace(go.Scatter3d(x=MinMax(df.sort_values(by=x)[x].values), y=MinMax(df.sort_values(by=x)[z].values), z=df.sort_values(by=x)['userYhat'].values,
                                        mode='lines',
                                        name='Model Fit',
                                        hovertemplate = str(y) + ': %{z}<br>' + str(x) + ': %{x}<br>' + str(z) + ': %{y}<br>'))                
            else:
                if sorted(df[y].unique()) == [0, 1]:
                    fig.add_trace(go.Scatter3d(x=df[x], y=df[z], z=df[y].values,
                                        mode='markers',
                                        marker=dict(size=5),
                                        name='Sample',
                                        hovertemplate = str(y) + ': %{z}<br>' + str(x) + ': %{x}<br>' + str(z) + ': %{y}<br>'))
                    fig.add_trace(go.Scatter3d(x=df.sort_values(by=x)[x], y=df.sort_values(by=x)[z], z=df.sort_values(by=x)['userYhat'].values,
                                        mode='markers',
                                        name='Pred Probability',
                                        hovertemplate = str(y) + ': %{z}<br>' + str(x) + ': %{x}<br>' + str(z) + ': %{y}<br>'))
                else:
                    fig.add_trace(go.Scatter3d(x=df[x], y=df[z], z=df[y].values,
                                        mode='markers',
                                        marker=dict(size=5),
                                        name='Sample',
                                        hovertemplate = str(y) + ': %{z}<br>' + str(x) + ': %{x}<br>' + str(z) + ': %{y}<br>'))
                    fig.add_trace(go.Scatter3d(x=df.sort_values(by=x)[x], y=df.sort_values(by=x)[z], z=df.sort_values(by=x)['userYhat'].values,
                                        mode='lines',
                                        name='Model Fit',
                                        hovertemplate = str(y) + ': %{z}<br>' + str(x) + ': %{x}<br>' + str(z) + ': %{y}<br>'))
            fig.layout.xaxis.fixedrange = False
            fig.update_yaxes(automargin=True)
            fig.update_xaxes(automargin=True)
            fig.layout.yaxis.fixedrange = False
            fig.update_layout(
                    scene=dict(xaxis_title=x,yaxis_title=z,zaxis_title=y),
                    hoverlabel=dict(bgcolor='white', font_color='black', font_size=18),
                    paper_bgcolor='#060606',
                    plot_bgcolor='#060606',
                    template='cyborg',
                    autosize=True,
                    font_family = 'Montserrat, sans-serif',
                    font_color='#FCFCFC',
                    title_font_family='Arial, Helvetica, sans-serif',
                    title_font_color='#FCFCFC',
                    legend_title_font_color='#FFFDFD',
                    hovermode='closest')
            return fig
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(Output('figResiduals', 'figure'),
              [Input('userYhat', 'data'),
               Input('userTestResidual', 'data'),
               Input('radioTrainOrTest', 'value'),
               State('dropDV', 'value'),
               Input('userTestX', 'data'),
               ])
def updateResiduals(df2, residuals, TrainOrTest, y, test):
    if not df2:
        raise PreventUpdate
    else:
        df = pd.read_json(df2)
        test_df = pd.read_json(test)
        fig = go.Figure()
        if TrainOrTest == 'train':
            fig.add_trace(go.Scattergl(x=df['userYhat'], y=df['residuals'],
                                mode='markers',
                                name='Residuals',
                                hovertemplate = 'Predicted: ' + str(y) + ': %{x}<br>' + 'Residual: ' + '%{y}<br>'))
        elif TrainOrTest == 'test':
            fig.add_trace(go.Scattergl(x=test_df['userYhat'], y=residuals,
                                mode='markers',
                                name='Residuals',
                                hovertemplate = 'Predicted: ' + str(y) + ': %{x}<br>' + 'Residual: ' + '%{y}<br>'))
        fig.update_layout(
            scene=dict(xaxis_title='Predicted Values', yaxis_title='Residuals'),
            paper_bgcolor='#060606',
            plot_bgcolor='#060606',
            font_family = 'Montserrat, sans-serif',
            font_color='#FCFCFC',
            title_font_family='Arial, Helvetica, sans-serif',
            title_font_color='#FCFCFC',
            hoverlabel=dict(bgcolor='white', font_color='black', font_size=18),
            legend_title_font_color='#FFFDFD',
            template= 'cyborg'
            )
        fig.update_yaxes(automargin=True)
        fig.update_xaxes(automargin=True)
        fig.layout.xaxis.fixedrange = False
        fig.layout.yaxis.fixedrange = False
        return fig


@app.callback(Output('figCorr', 'figure'),
              [State('userData', 'data'),
               Input('navFig', 'value'),
               Input('filterCorr', 'value'),
               Input('valueCorr', 'value')
               ])
def updateCorr(df2, nav, group, value):
    if nav == 'figCorr':
        if df2 and group and value:
            df = pd.read_json(df2, orient='split')
            corr = df.loc[df[group] == value].corr()
            fig = go.Figure()
            fig.add_trace(go.Heatmap(z=corr.values,
                    x=corr.index.values,
                    y=corr.columns.values,
                    hovertemplate = '%{x} - %{y}<br>' + "Correlation" + ': %{z}'))
        else:
            corr = pd.read_json(df2, orient='split').corr()
            fig = go.Figure()
            fig.add_trace(go.Heatmap(z=corr.values,
                    x=corr.index.values,
                    y=corr.columns.values,
                    hovertemplate = '%{x} - %{y}<br>' + "Correlation" + ': %{z}'))
        fig.update_layout(
            paper_bgcolor='#060606',
            autosize=True,
            hoverlabel=dict(bgcolor='white',
            font_color='black', font_size=18),
            font_family = 'Montserrat, sans-serif',
            font_color='#FCFCFC')
        fig.update_yaxes(automargin=True)
        fig.update_xaxes(automargin=True)
        fig.layout.xaxis.fixedrange = False
        fig.layout.yaxis.fixedrange = False 
        return fig
    else:
        raise PreventUpdate

@app.callback(Output('checkIV', 'options'),
              [Input('userData', 'data')], prevent_initial_call=True)
def updateCheckIV(df):
    return [{'label': str(i), 'value': str(i)} for i in pd.read_json(df, orient='split')._get_numeric_data().columns]

@app.callback(Output('tabDescribe', 'children'),
              [Input('userData', 'data')
               ])
def updateDescribe(df):
    if df:
        return dbc.Table.from_dataframe(pd.read_json(df, orient='split').describe().reset_index().rename(columns={'index':'stat'}), striped=True, bordered=True, responsive=True)
    else:
        raise PreventUpdate


@app.callback(Output('tabPreview', 'children'),
              [Input('userData', 'data'),
               Input('btnShuffle', 'n_clicks')
               ])
def updateShuffle(df, btn):
    if df:
        if df and not btn:
            return dbc.Table.from_dataframe(pd.read_json(df, orient='split').head(10), striped=True, bordered=True, responsive=True, style={'borderRadius': '15px','overflow': 'hidden'})
        else:
            return dbc.Table.from_dataframe(pd.read_json(df, orient='split').sample(frac=1).head(10), striped=True, bordered=True, responsive=True, style={'borderRadius': '15px','overflow': 'hidden'})
    else:
        raise PreventUpdate

@app.callback(Output('vmr', 'children'),
              [Input('radioViz', 'value'),
               State('checkIV', 'value'),
               Input('btnFit', 'n_clicks')], prevent_initial_call=True)
def updateViewModelResults(val, x, btn):
    if btn or val:
        if val == 'residuals':
            try:
                return [dbc.Row(
                    [
                        dbc.Col(html.Div(cardResidual), width=12),
                    ], justify="center", align="center"
                )]
            except Exception as exception:
                return exception 
        elif val == 'modelfit':
            try:
                if len(x) > 1:
                    return [
                            html.Div([
                                html.Div(cardFitX, className = 'viz-model-radio'),
                                html.Div(cardScatterFit, className = 'viz-model-chart'), 
                            ], className = 'chart-and-radio'),
                            html.Hr(), 
                            html.Div([
                                html.Div(cardFitX3D, className = 'viz-model-radio'), 
                                html.Div(cardScatterFit3D, className = 'viz-model-chart')
                            ], className = 'chart-and-radio')
                            ]
                else:
                    return [
                            html.Div([
                                html.Div(cardFitX, className = 'viz-model-radio'),
                                html.Div(cardScatterFit, className = 'viz-model-chart'), 
                            ], className = 'chart-and-radio')
                            ]
            except Exception as exception:
                return exception
    else:
        raise PreventUpdate


@app.callback([Output('user_upload_section_content', 'style'),
               Output('upload_section_content', 'style')],
              [Input('radioChooseDataOption', 'value')])
def updateDataSelection(val):
    if val == 'sampDataset':
        return [{'display': 'flex'}, {'display': 'none'}]
    elif val == 'userUploadDataset':
        return [{'display': 'none'}, {'display': 'flex'}]
    else:
        raise PreventUpdate

    
@app.callback(Output('userFig', 'children'),
              [Input('navFig', 'value')
               ])
def updateUserChoice(val):
    if val == 'figScatter':
        return cardScatter
    elif val == 'figScatter3D':
        return cardScatter3D
    elif val == 'figSurface3D':
        return cardSurface3D
    elif val == 'fig2D':
        return card2D
    elif val == 'figMatrix':
        return cardMatrix
    elif val == 'figContour2D':
        return cardContour2D
    elif val == 'figMesh':
        return cardMesh3D
    elif val == 'figLine':
        return cardLine
    elif val == 'figLine3D':
        return cardLine3D
    elif val == 'figCorr':
        return cardCorr
    elif val == 'ds':
        return cardDescribe
    elif val == 'figDist':
        return cardDist
    elif val == 'figHist':
        return cardHist
    elif val == 'figBar':
        return cardBar
    elif val == 'figPie':
        return cardPie
    elif val == 'figBox':
        return cardBox
    elif val == 'dataPreview':
        return cardPreview


@app.callback([Output('tabStats', 'children'),
               Output('userYhat', 'data'),
               Output('tabFit', 'children'),
               Output('dropDV', 'disabled'),
               Output('tabViz', 'disabled'),
               Output('tabFitTest', 'children'),
               Output('userTestResidual', 'data'),
               Output('userTestPred', 'data'),
               Output('userTestX', 'data'),
               Output('userCoefficients', 'data'),
               Output('radioViz', 'options'),
               Output('radioTrainOrTest', 'options')
               ],
              [
               State('userData', 'data'),
               State('dropDV', 'value'),
               State('checkIV', 'value'),
               State('radioTransform', 'value'),
               Input('btnFit', 'n_clicks'),
               State('testsplit', 'value'),
               State('radioIntercept', 'value')
               ], prevent_initial_call=True)
def run(df2, y, x, transformation, btn, prcnt, intercept):
    if btn:
        tempdf = pd.read_json(df2, orient='split').dropna()._get_numeric_data()
        if sorted(tempdf[y].unique()) == [0, 1]:
            if 'yes' in intercept:        
                x.insert(0, 'Intercept')
            if transformation == 'standardize':
                df = Standardize(tempdf, True)
                if 'yes' in intercept:
                    df['Intercept'] = [1 for i in range(tempdf.shape[0])]
                if float(prcnt) > 0:
                    X_train, X_test, y_train, y_test = train_test_split(df[x], df[y], test_size=float(prcnt), random_state=42)
                    model = sm.Logit(y_train, X_train).fit()
                    df = X_train.copy()
                    df[y] = y_train
                    test = model.predict(X_test)
                    test_class =  np.array([1 if i > .5 else 0 for i in test])
                    X_test[y] = y_test
                    X_test['userYhat'] = test
                    train_pred = model.predict(X_train)
                    train_temp =  np.array([1 if i > .5 else 0 for i in train_pred])
                    df['userYhat'] = train_pred
                else:
                    model = sm.Logit(df[y], df[x]).fit()
                    test = model.predict(df[x])
                    test_class =  np.array([1 if i > .5 else 0 for i in test])
                    X_test = df[x].head(1)
                    df['userYhat'] = test
            elif transformation == 'minmax':
                df = MinMax(tempdf, True)
                if 'yes' in intercept:
                    df['Intercept'] = [1 for i in range(tempdf.shape[0])]
                if float(prcnt) > 0:
                    X_train, X_test, y_train, y_test = train_test_split(df[x], df[y], test_size=float(prcnt), random_state=42)
                    model = sm.Logit(y_train, X_train).fit()
                    df = X_train.copy()
                    df[y] = y_train
                    test = model.predict(X_test)
                    test_class =  np.array([1 if i > .5 else 0 for i in test])
                    X_test[y] = y_test
                    X_test['userYhat'] = test
                    train_pred = model.predict(X_train)
                    train_temp =  np.array([1 if i > .5 else 0 for i in train_pred])
                    df['userYhat'] = train_pred
                else:
                    model = sm.Logit(df[y], df[x]).fit()
                    test= model.predict(df[x])
                    test_class =  np.array([1 if i > .5 else 0 for i in test])
                    X_test = df[x].head(1)
                    df['userYhat'] = test
            else:
                df = tempdf.copy()
                if 'yes' in intercept:
                    df['Intercept'] = [1 for i in range(tempdf.shape[0])]
                if float(prcnt) > 0:
                    X_train, X_test, y_train, y_test = train_test_split(df[x], df[y], test_size=float(prcnt), random_state=42)
                    model = sm.Logit(y_train, X_train).fit()
                    df = X_train.copy()
                    df[y] = y_train
                    test = model.predict(X_test)
                    test_class =  np.array([1 if i > .5 else 0 for i in test])
                    X_test[y] = y_test
                    X_test['userYhat'] = test
                    train_pred = model.predict(X_train)
                    train_temp =  np.array([1 if i > .5 else 0 for i in train_pred])
                    df['userYhat'] = train_pred
                else:
                    model = sm.Logit(df[y], df[x]).fit()          
                    test = model.predict(df[x])
                    test_class =  np.array([1 if i > .5 else 0 for i in test])
                    X_test = df[x].head(1)
                    df['userYhat'] = test
            if float(prcnt) > 0:
                ac = round(accuracy_score(y_test, test_class), 2)
                pc = round(precision_score(y_test, test_class), 2)
                rc = round(recall_score(y_test, test_class), 2)
            else:
                ac = 0
                pc = 0
                rc = 0
            
            tst_df = pd.DataFrame({'Accuracy': [ac], 'Precision': [pc], 'Recall': [rc]})
            fit1_df = pd.read_html(model.summary().tables[1].as_html(), header=0, index_col=0)[0].reset_index().rename({'index': 'Variable'})
            tabfit1 = dash_table.DataTable(id='table_data1',export_format='csv', data=fit1_df.to_dict('records'), columns= [{'name': i, 'id': i} for i in fit1_df.columns], style_cell={'padding': '5px'}, style_header={
            'backgroundColor': '#090909',
            'color': '#FCFCFC',
            'border': '1px solid black',
            'fontWeight': 'bold',
            'font_family': 'Arial, Helvetica, sans-serif'
                },
                style_data={
                'backgroundColor': '#191a1b',
                'color': '#ffffff',
                'border': '1px solid black',
                'font_family': 'Arial, Helvetica, sans-serif'
                },
                style_data_conditional=[
                        {
            'if': {'state': 'selected'},
            'backgroundColor': 'inherit !important',
            'border': 'inherit !important',
                        }
                    ]
                )
            fit2_df = pd.read_html(model.summary().tables[0].as_html(), header=0, index_col=0)[0].reset_index()
            tabfit2 = dash_table.DataTable(id='table_data3',export_format='csv', data=fit2_df.to_dict('records'), columns= [{'name': i, 'id': i} for i in fit2_df.columns], style_cell={'padding': '5px'}, style_header={
            'backgroundColor': '#090909',
            'color': '#FCFCFC',
            'border': '1px solid black',
            'fontWeight': 'bold',
            'font_family': 'Arial, Helvetica, sans-serif'
                },
                style_data={
                'backgroundColor': '#191a1b',
                'color': '#ffffff',
                'border': '1px solid black',
                'font_family': 'Arial, Helvetica, sans-serif'
                },
                style_data_conditional=[
                        {
            'if': {'state': 'selected'},
            'backgroundColor': 'inherit !important',
            'border': 'inherit !important',
                        }
                    ]
                )
            tabscores = dash_table.DataTable(id='table_data2',export_format='csv', data=tst_df.to_dict('records'), columns= [{'name': i, 'id': i} for i in tst_df.columns], style_cell={'padding': '5px'}, style_header={
            'backgroundColor': '#090909',
            'color': '#FCFCFC',
            'border': '1px solid black',
            'fontWeight': 'bold',
            'font_family': 'Arial, Helvetica, sans-serif'
                },
                style_data={
                'backgroundColor': '#191a1b',
                'color': '#ffffff',
                'border': '1px solid black',
                'font_family': 'Arial, Helvetica, sans-serif'
                },
                style_data_conditional=[
                        {
            'if': {'state': 'selected'},
            'backgroundColor': 'inherit !important',
            'border': 'inherit !important',
                        }
                    ]
                )
            if float(prcnt) > 0:
                radioTrainOrTest = [{'label': 'Train', 'value': 'train'}, {'label': 'Test', 'value': 'test'}]
            else:
                radioTrainOrTest = [{'label': 'Train', 'value': 'train'}] 
            return [tabfit1, df.to_json(), tabfit2, False, False, tabscores, pd.DataFrame({'x': [0]}).to_json(), test, X_test.to_json(), pd.read_html(model.summary().tables[1].as_html(), header=0, index_col=0)[0].to_json(), [{'label': 'Fit', 'value': 'modelfit'}], radioTrainOrTest]
        else:          
            ols = OLS()
            dct = pd.DataFrame()
            dct2 = pd.DataFrame()
            if transformation == 'standardize':
                df = Standardize(tempdf, True)
                if float(prcnt) > 0:
                    X_train, X_test, y_train, y_test = train_test_split(df[x], df[y], test_size=float(prcnt), random_state=42)
                    if 'yes' in intercept:
                        ols.fit(X_train.values, y_train.to_numpy(), True)
                    else:
                        ols.fit(X_train.values, y_train.to_numpy(), False)
                    df = X_train.copy()
                    df[y] = y_train
                    test = ols.test(X_test.values, y_test.to_numpy())
                    X_test[y] = y_test
                    X_test['userYhat'] = test[5]
                else:
                    if 'yes' in intercept:
                        ols.fit(df[x].values, df[y].to_numpy(), True)
                    else:
                        ols.fit(df[x].values, df[y].to_numpy(), False)                   
                    test = ols.test(df[x].head(1).values, df[y].head(1).to_numpy())
                    X_test = df[x].head(1)
            elif transformation == 'minmax':
                df = MinMax(tempdf, True)
                if float(prcnt) > 0:
                    X_train, X_test, y_train, y_test = train_test_split(df[x], df[y], test_size=float(prcnt), random_state=42)
                    if 'yes' in intercept:
                        ols.fit(X_train.values, y_train.to_numpy(), True)
                    else:
                        ols.fit(X_train.values, y_train.to_numpy(), False)
                    df = X_train.copy()
                    df[y] = y_train
                    test = ols.test(X_test.values, y_test.to_numpy())
                    X_test[y] = y_test
                    X_test['userYhat'] = test[5]
                else:
                    if 'yes' in intercept:
                        ols.fit(df[x].values, df[y].to_numpy(), True)
                    else:
                        ols.fit(df[x].values, df[y].to_numpy(), False) 
                    test = ols.test(df[x].head(1).values, df[y].head(1).to_numpy())
                    X_test = df[x].head(1)
            else:
                df = tempdf.copy()
                if float(prcnt) > 0:
                    X_train, X_test, y_train, y_test = train_test_split(df[x], df[y], test_size=float(prcnt), random_state=42)
                    if 'yes' in intercept:
                        ols.fit(X_train.values, y_train.to_numpy(), True)
                    else:
                        ols.fit(X_train.values, y_train.to_numpy(), False)
                    df = X_train.copy()
                    df[y] = y_train
                    test = ols.test(X_test.values, y_test.to_numpy())
                    X_test[y] = y_test
                    X_test['userYhat'] = test[5]
                else:
                    if 'yes' in intercept:
                        ols.fit(df[x].values, df[y].to_numpy(), True)
                    else:
                        ols.fit(df[x].values, df[y].to_numpy(), False) 
                    test = ols.test(df[x].head(1).values, df[y].head(1).to_numpy())
                    X_test = df[x].head(1)
            if 'yes' in intercept:
                dct['intercept'] = [str(round(ols.beta[0], 3))]
                dct2['intercept'] = [str(ols.beta[0])]
                cnt = 1
            else:
                cnt = 0
            for i in df.drop(columns=[y])[x]._get_numeric_data().columns:
                dct[str(i)] = [str(round(ols.beta[cnt], 3))]    
                dct2[str(i)] = [str(ols.beta[cnt])]    
                cnt += 1   
            df['userYhat'] = ols.yhat
            df['residuals'] = ols.residuals
            stats = pd.DataFrame()
            stats_test = pd.DataFrame()
            stats['Train R2'] = [str(round(ols.r2, 2))]

            if float(prcnt) == 0:
                stats_test['Test R2'] = 0.0
                stats_test['Test Adj R2'] = 0.0
                stats_test['Test RMSE'] = 0.0
                stats_test['Test MAPE'] = 0.0
                stats_test['Test Durbin Watson'] = 0.0
            else:
                stats_test['Test R2'] = [str(round(test[1], 2))]
                stats_test['Test Adj R2'] = [str(round(test[2], 2))] 
                stats_test['Test RMSE'] = [str(round(math.sqrt(test[3]), 4))]
                stats_test['Test MAPE'] = [str(round(test[6], 2))] 
                stats_test['Test Durbin Watson'] = [str(round(test[4], 2))]         
            stats['Train Adj R2'] = [str(round(ols.adj_r2,2))]
            stats['Train RMSE'] = [str(round(math.sqrt(ols.mse),4))]
            stats['Train MAPE'] = [str(round(ols.mape,2))]
            stats['Train Durbin Watson'] = [str(round(ols.dw,2))]
            return_df = dct.T.reset_index().rename(columns={0:'Coeffecient', 'index':'Variables'})
            return_df['Standard Error'] = [round(i, 3) for i in ols.se]
            return_df['T'] = [round(i, 3) for i in ols.t]
            return_df['P value'] = [round(i, 5) for i in ols.p]
            tabfit = dash_table.DataTable(id='table_data1',export_format='csv', data=return_df.to_dict('records'), columns= [{'name': i, 'id': i} for i in return_df.columns], style_cell={'padding': '5px'}, style_header={
            'backgroundColor': '#090909',
            'color': '#FCFCFC',
            'border': '1px solid black',
            'fontWeight': 'bold',
            'font_family': 'Arial, Helvetica, sans-serif'
                },
                style_data={
                'backgroundColor': '#191a1b',
                'color': '#ffffff',
                'border': '1px solid black',
                'font_family': 'Arial, Helvetica, sans-serif'
                },
                style_data_conditional=[
                        {
            'if': {'state': 'selected'},
            'backgroundColor': 'inherit !important',
            'border': 'inherit !important',
                        }
                    ]
                )
            tabstats = dash_table.DataTable(id='table_data2',export_format='csv', data=stats.to_dict('records'), columns= [{'name': i, 'id': i} for i in stats.columns], style_cell={'padding': '5px'}, style_header={
            'backgroundColor': '#090909',
            'color': '#FCFCFC',
            'border': '1px solid black',
            'fontWeight': 'bold',
            'font_family': 'Arial, Helvetica, sans-serif'
                },
                style_data={
                'backgroundColor': '#191a1b',
                'color': '#ffffff',
                'border': '1px solid black',
                'font_family': 'Arial, Helvetica, sans-serif'
                },
                style_data_conditional=[
                {
            'if': {'state': 'selected'},
            'backgroundColor': 'inherit !important',
            'border': 'inherit !important',
                }
                    ]
                )
            testtab = dash_table.DataTable(id='table_data3',export_format='csv', data=stats_test.to_dict('records'), columns= [{'name': i, 'id': i} for i in stats_test.columns], style_cell={'padding': '5px'}, style_header={
            'backgroundColor': '#090909',
            'color': '#FCFCFC',
            'border': '1px solid black',
            'fontWeight': 'bold',
            'font_family': 'Arial, Helvetica, sans-serif'
                },
                style_data={
                'backgroundColor': '#191a1b',
                'color': '#ffffff',
                'border': '1px solid black',
                'font_family': 'Arial, Helvetica, sans-serif'
                },
                style_data_conditional=[
                {
            'if': {'state': 'selected'},
            'backgroundColor': 'inherit !important',
            'border': 'inherit !important',
                }
                    ]
                )
            if float(prcnt) > 0:
                radioTrainOrTest = [{'label': 'Train', 'value': 'train'}, {'label': 'Test', 'value': 'test'}]
            else:
                radioTrainOrTest = [{'label': 'Train', 'value': 'train'}] 
            return [tabfit, df.to_json(), tabstats, False, False, testtab, test[0], test[5], X_test.to_json(), dct2.to_json(), [{'label': 'Fit', 'value': 'modelfit'}, {'label': 'Residuals', 'value': 'residuals'}], radioTrainOrTest]
    else:
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=False,dev_tools_ui=False,dev_tools_props_check=False)
    #app.run_server(debug=True)   


