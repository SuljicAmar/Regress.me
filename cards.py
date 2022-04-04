import dash_bootstrap_components as dbc
import dash
from dash import Input, Output, State, dcc, html, dash_table


cardDV = dbc.Card(dbc.CardBody([dbc.Label('Dependent Variable', className='mt-3',  style={'color': '#FFFDFD'}), 
                                dcc.Dropdown(id='dropDV', style={'color':'#FFFDFD', 'background-color': '#060606'})
                                ]), style={'color':'#FFFDFD', 'background-color': '#060606'})

cardIV = dbc.Card(dbc.CardBody([dbc.Label('Independent Variable(s)', className='mt-3',  style={'color': '#FFFDFD', }), 
                                dbc.Checklist(id='checkIV', inline=True, labelStyle = dict(display='inline'))
                                ]),  style={'background-color': '#060606'})

cardTransform = dbc.Card(dbc.CardBody([dbc.Label('Transformation', className='mt-3',  style={'color': '#FFFDFD'}), 
                                       dbc.RadioItems(id='radioTransform',inline=True,
                                                      options=[
                                                          {'label': 'None', 'value': 'None'},
                                                          {'label': 'Standardize', 'value': 'standardize'},
                                                          {'label': 'Min-Max', 'value': 'minmax'}
                                                          ], 
                                                      value='None')
                                       ]), 
                         style={'background-color': '#060606'})

cardStats = dbc.Card(
    dbc.CardBody(
        [
            html.Div(id='tabStats')
        ]),  style={'background-color': '#060606'})

cardFit = dbc.Card(dbc.CardBody([html.Div(id='tabFit')]),  style={'background-color': '#060606',})

cardFitTest = dbc.Card(dbc.CardBody([html.Div(id='tabFitTest')]),  style={'background-color': '#060606',})

cardDescribe = dbc.Card(dbc.CardBody([html.Div(id='tabDescribe')]),  style={'background-color': '#060606', }, className='my-5')

cardCorr = dbc.Card(dbc.CardBody(
    [
        dcc.Graph(id='figCorr',  config={'displayModeBar': False}),
        dbc.Label('Filter', className='mt-3', style={'color': '#FFFDFD'}), 
        dcc.Dropdown(
        id='filterCorr',style={'color':'#FFFDFD', 'background-color': '#060606'}),
        dbc.Label('Value', className='mt-3', style={'color': '#FFFDFD'}), 
        dcc.Dropdown(id='valueCorr',className='mt-1', style={'color':'#FFFDFD', 'background-color': '#060606'})
     ]
    ),  style={'background-color': '#060606', })
          
cardResidual = dbc.Card(dbc.CardBody([dcc.Graph(id='figResiduals',  config={'displayModeBar': False})]),  style={'background-color': '#060606'})

cardLine = dbc.Card(dbc.CardBody(
    [
        dbc.Label('X for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(
        id='userXLine',style={'color':'#FFFDFD', 'background-color': '#060606', }
        ),
        dbc.Label('Y for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(
        id='userYLine',style={'color':'#FFFDFD', 'background-color': '#060606', }
        ),
        dcc.Graph(id='figLine',  config={'displayModeBar': False}),
        dbc.Label('Filter', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(id='filterLine', style={'color':'#FFFDFD', 'background-color': '#060606', }),
        ]
    ),  style={'background-color': '#060606', }
)

cardLine3D = dbc.Card(dbc.CardBody(
    [
        dbc.Label('X for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(
        id='userXLine3D',style={'color':'#FFFDFD', 'background-color': '#060606', }
        ),
        dbc.Label('Y for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(
        id='userYLine3D',style={'color':'#FFFDFD', 'background-color': '#060606', }
        ),
        dbc.Label('Z for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(
        id='userZLine3D',style={'color':'#FFFDFD', 'background-color': '#060606', }
        ),
        dcc.Graph(id='figLine3D',  config={'displayModeBar': False}),
        dbc.Label('Filter', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(id='filterLine3D', style={'color':'#FFFDFD', 'background-color': '#060606', }),
        ]
    ),  style={'background-color': '#060606', }
)

card2D = dbc.Card(dbc.CardBody(
    [
        dbc.Label('X for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(
        id='userX2D',style={'color':'#FFFDFD', 'background-color': '#060606', }
        ),
        dbc.Label('Y for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(
        id='userY2D',style={'color':'#FFFDFD', 'background-color': '#060606', }
        ),
        dcc.Graph(id='fig2D',  config={'displayModeBar': False}),
        dbc.Label('Row Facet', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(id='filter2DRow', style={'color':'#FFFDFD', 'background-color': '#060606', }),
        dbc.Label('Column Facet', className='mt-3', style={'color': '#FFFDFD', }),
        dcc.Dropdown(id='filter2DColumn', style={'color':'#FFFDFD', 'background-color': '#060606', }),
        ]
    ),  style={'background-color': '#060606', }
)

cardScatter = dbc.Card(dbc.CardBody(
    [
        dbc.Label('X for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(
        id='userXScatter',style={'color':'#FFFDFD', 'background-color': '#060606', }
        ),
        dbc.Label('Y for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(
        id='userYScatter',style={'color':'#FFFDFD', 'background-color': '#060606', }
        ),
        dcc.Graph(id='figScatter',  config={'displayModeBar': False}),
        dbc.Label('Filter', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(id='filterScatter', style={'color':'#FFFDFD', 'background-color': '#060606', }),
        ]
    ),  style={'background-color': '#060606', }
)

cardScatter3D = dbc.Card(dbc.CardBody(
    [
        dbc.Label('X for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(
        id='userXScatter3D',style={'color':'#FFFDFD', 'background-color': '#060606', }
        ),
        dbc.Label('Y for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(
        id='userYScatter3D',style={'color':'#FFFDFD', 'background-color': '#060606', }
        ),
        dbc.Label('Z for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(
        id='userZScatter3D',style={'color':'#FFFDFD', 'background-color': '#060606', }
        ),
        dcc.Graph(id='figScatter3D',  config={'displayModeBar': False}),
        dbc.Label('Filter', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(id='filterScatter3D', style={'color':'#FFFDFD', 'background-color': '#060606', }),
        ]
    ),  style={'background-color': '#060606', }
)

cardDist = dbc.Card(dbc.CardBody(
    [
        dbc.Label('Variable for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(
        id='userXDist',style={'color':'#FFFDFD', 'background-color': '#060606', }
        ),
        dbc.Label('Filter', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(id='filterDist', style={'color':'#FFFDFD', 'background-color': '#060606'}),
        dcc.Graph(id='figDist',  config={'displayModeBar': False}),
        dbc.Checklist(id='normalize', inline=True, labelStyle = dict(display='inline'), options=[{'label': 'Normalize', 'value': 'yes'}],  style={'background-color': '#060606'})
        ]
    ),  style={'background-color': '#060606', }
)
 
cardHist = dbc.Card(dbc.CardBody(
    [
        dbc.Label('Variable for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(
        id='userXHist',style={'color':'#FFFDFD', 'background-color': '#060606', }
        ),
        dbc.Label('Filter', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(id='filterhist', style={'color':'#FFFDFD', 'background-color': '#060606', }),
        dcc.Graph(id='figHist',  config={'displayModeBar': False})        
        ]
    ),  style={'background-color': '#060606', }
)

cardBar = dbc.Card(dbc.CardBody(
    [
        dbc.Label('X for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(
        id='userXBar',style={'color':'#FFFDFD', 'background-color': '#060606', }
        ),
        dbc.Label('Y for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(
        id='userYBar',style={'color':'#FFFDFD', 'background-color': '#060606', }
        ),
        dcc.Graph(id='figBar',  config={'displayModeBar': False}),
        dbc.Label('Filter', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(id='filterBar', style={'color':'#FCFCFC', 'background-color': '#060606', }),
        ]
    ),  style={'background-color': '#060606', }
)

cardPie = dbc.Card(dbc.CardBody(
    [
        dbc.Label('Variable for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(
        id='userXPie',style={'color':'#FFFDFD', 'background-color': '#060606', }
        ),
        dbc.Label('Filter', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(id='filterPie', style={'color':'#FFFDFD', 'background-color': '#060606', }),
        dcc.Graph(id='figPie',  config={'displayModeBar': False})        
        ]
    ),  style={'background-color': '#060606', }
)

cardBox = dbc.Card(dbc.CardBody(
    [
        dbc.Label('Variable for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(
        id='userYBox',style={'color':'#FFFDFD', 'background-color': '#060606', }
        ),
        dcc.Graph(id='figBox',  config={'displayModeBar': False}),
        dbc.Label('X Variable', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(id='userXBox', style={'color':'#FFFDFD', 'background-color': '#060606', }),
        dbc.Label('Filter', className='mt-3', style={'color': '#FFFDFD', }), 
        dcc.Dropdown(id='filterBox', style={'color':'#FFFDFD', 'background-color': '#060606', }),
        ]
    ),  style={'background-color': '#060606', }
)

cardFitX = dbc.Card(dbc.CardBody(
            [dbc.Label('X for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
        dbc.RadioItems(
        id='radioIV', inline=True)]),style={'color': '#FCFCFC', 'background-color': '#060606', })

cardScatterFit = dbc.Card(dbc.CardBody([dcc.Graph(id='figFit',  config={'displayModeBar': False})]),  style={'background-color': '#060606', })

cardFitX3D = dbc.Card(dbc.CardBody(
            [dbc.Label('Var 1 for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
        dbc.RadioItems(
        id='radioIV3D', inline=True),
        dbc.Label('Var 2 for Plot', className='mt-3', style={'color': '#FFFDFD', }),
        dbc.RadioItems(
        id='radioIV3DZ', inline=True)]),style={'color': '#FCFCFC', 'background-color': '#060606', })

cardScatterFit3D = dbc.Card(dbc.CardBody([dcc.Graph(id='figFit3D',  config={'displayModeBar': False})]),  style={'background-color': '#060606', })


cardUpload = dbc.Card(
    [
        dbc.CardBody(
            [
    dcc.Upload(
        id='uploadData',
        children=html.Div([
        'Drag and Drop or ',
        html.A('Click to Files')
        ]),
        style={
        'color': '#FFFFFF',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
         },
        multiple=False
),
     dbc.Tooltip(
            '',
            target='uploadData',
            id='uploadToolTip'
        ),
            ]
        ),
    ],
      style={'background-color': '#060606'}
)

jumbotronHome = html.Div(
    dbc.Container(
        [
            html.H1('Plots & Regression', className='display-3'),
            html.P(
                'For free with no code. Upload a .csv file to get started. ',
            ),
           cardUpload
        ],
        fluid=True,
        className='py-1',
        style={'background-color': '#060606', 'color': '#FFFDFD'}
    ),
    style={'background-color': '#060606', 'color': '#FFFDFD'}
)