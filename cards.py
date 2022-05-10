import dash_bootstrap_components as dbc
import dash
from dash import Input, Output, State, dcc, html, dash_table
import base64

upload_icon = 'assets/upload2.png'
upload_icon_64 = base64.b64encode(open(upload_icon, 'rb').read()).decode('ascii')

cardDV = html.Div([
            html.P('Dependent Variable', className = 'label'), 
            dcc.Dropdown(id='dropDV')
        ],id = 'card_dv', className = 'model-card')

cardIV = html.Div([
                html.P('Independent Variable(s)', className='label'), 
                dbc.Checklist(id='checkIV', inline=True, labelStyle = dict(display='inline'))
            ],id = 'card_iv', className = 'model-card')

cardTransform = html.Div([
                    html.P('Transformation', className='label'), 
                    dbc.RadioItems(id='radioTransform',inline=True,
                                    options=[
                                        {'label': 'None', 'value': 'None'},
                                        {'label': 'Standardize', 'value': 'standardize'},
                                        {'label': 'Min-Max', 'value': 'minmax'}
                                        ], 
                                    value='None')
                ],id = 'card_transform', className = 'model-card')


cardSplit = html.Div([
                    html.P('Test Data Split', className='label'),
                    dcc.Slider(
                        min=0, 
                        max=1, 
                        step=.01, 
                        value=.20, 
                        id='testsplit',
                        tooltip={'placement': 'bottom', 'always_visible': True},
                        marks = None,
                        )
                ],id = 'card_split', className = 'model-card')

cardStats = html.Div(id='tabStats')

cardFit = html.Div(id='tabFit')

cardFitTest = html.Div(id='tabFitTest')

cardDescribe = html.Div([
                    html.Div([
                        html.Div(id='tabDescribe')
                    ], id = 'absolutely-centered')
                ], className = 'exploration-content-centered')

cardPreview = html.Div([
    html.Div([
        dbc.Label('Shuffle Dataset', className='mt-3', style={'color': '#FFFDFD'}), 
        html.Div(html.Button('Shuffle', id='btnShuffle', n_clicks=0, className='button-shuffle'), id = 'button-container'),
        ], id = 'dropdowns'),
    html.Div([
        html.Div(id='tabPreview')
        ], id = 'graph')
    ], className = 'exploration-content')

cardCorr = html.Div([
                html.Div([
                    dbc.Label('Filter', className='mt-3', style={'color': '#FFFDFD'}), 
                    dcc.Dropdown(
                    id='filterCorr'),
                    dbc.Label('Value', className='mt-3', style={'color': '#FFFDFD'}), 
                    dcc.Dropdown(id='valueCorr',className='mt-1'),
                ], id = 'dropdowns'),
                html.Div([
                    dcc.Graph(id='figCorr',  config={'displayModeBar': True}),
                ], id = 'graph')
            ], className = 'exploration-content')

cardResidual = html.Div([
                    dcc.Graph(id='figResiduals',  config={'displayModeBar': True})
                ], id = 'single-chart')

cardLine = html.Div([
                html.Div([
                    html.Div([
                        dbc.Label('X for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                        dcc.Dropdown(
                        id='userXLine'),
                        dbc.Label('Y for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                        dcc.Dropdown(
                        id='userYLine')
                    ], id = 'main-dropdowns'),

                html.Hr(className = 'sep-line'),

                    html.Div([
                        dbc.Label('Filter', className='mt-3', style={'color': '#FFFDFD', }), 
                        dcc.Dropdown(id='filterLine')
                    ], id = 'secondary-dropdowns')
                ], id = 'dropdowns'),

                html.Div([
                    dcc.Graph(id='figLine',  config={'displayModeBar': True}),
                ], id = 'graph')
           ], className = 'exploration-content')

cardLine3D = html.Div([
                html.Div([
                    html.Div([
                        dbc.Label('X for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                        dcc.Dropdown(id='userXLine3D'),
                        dbc.Label('Y for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                        dcc.Dropdown(id='userYLine3D'),
                        dbc.Label('Z for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                        dcc.Dropdown(id='userZLine3D')
                    ], id = 'main-dropdowns'),

                    html.Hr( id = 'sep-line'),

                    html.Div([
                        dbc.Label('Filter', className='mt-3', style={'color': '#FFFDFD', }), 
                        dcc.Dropdown(id='filterLine3D')
                    ], id = 'secondary-dropdowns')
                ], id = 'dropdowns'),
                html.Div([
                    dcc.Graph(id='figLine3D',  config={'displayModeBar': True}),
                ], id = 'graph')
            ], className = 'exploration-content')

card2D = html.Div([
                html.Div([
                    html.Div([
                        dbc.Label('X for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                        dcc.Dropdown(id='userX2D'),
                        dbc.Label('Y for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                        dcc.Dropdown(id='userY2D')
                    ], id = 'main-dropdowns'),

                        html.Hr( id = 'sep-line'),

                    html.Div([
                        dbc.Label('Row Facet', className='mt-3', style={'color': '#FFFDFD', }), 
                        dcc.Dropdown(id='filter2DRow'),
                        dbc.Label('Column Facet', className='mt-3', style={'color': '#FFFDFD', }),
                        dcc.Dropdown(id='filter2DColumn')
                    ], id = 'secondary-dropdowns')
                ], id = 'dropdowns'),
                html.Div([
                    dcc.Graph(id='fig2D',  config={'displayModeBar': True}),
                ], id = 'graph')
        ], className = 'exploration-content')

cardContour2D = html.Div([
                html.Div([
                    dbc.Label('X for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                    dcc.Dropdown(
                    id='userXContour2D'),
                    dbc.Label('Y for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                    dcc.Dropdown(
                    id='userYContour2D'),
                ], id = 'dropdowns'),
                html.Div([
                    dcc.Graph(id='figContour2D',  config={'displayModeBar': True}),
                ], id = 'graph')
        ], className = 'exploration-content')

cardScatter = html.Div([
                    html.Div([
                        html.Div([
                            dbc.Label('X for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                            dcc.Dropdown(
                            id='userXScatter'),
                            dbc.Label('Y for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                            dcc.Dropdown(
                            id='userYScatter')
                        ], id = 'main-dropdowns'),
                        html.Hr( id = 'sep-line'),
                        html.Div([
                            dbc.Label('Filter', className='mt-3', style={'color': '#FFFDFD', }), 
                            dcc.Dropdown(id='filterScatter'),
                            dbc.Label('Row', className='mt-3', style={'color': '#FFFDFD', }), 
                            dcc.Dropdown(id='filterScatterRow'),
                            dbc.Label('Column', className='mt-3', style={'color': '#FFFDFD', }), 
                            dcc.Dropdown(id='filterScatterCol')
                        ], id = 'secondary-dropdowns')
                    ], id = 'dropdowns'),
                    html.Div([
                        dcc.Graph(id='figScatter',  config={'displayModeBar': True}),
                    ], id = 'graph')
        ], className = 'exploration-content')

cardScatter3D = html.Div([
                    html.Div([
                        html.Div([
                            dbc.Label('X for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                            dcc.Dropdown(id='userXScatter3D'),
                            dbc.Label('Y for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                            dcc.Dropdown(id='userYScatter3D'),
                            dbc.Label('Z for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                            dcc.Dropdown(id='userZScatter3D')
                        ], id = 'main-dropdowns'),
                        html.Hr( id = 'sep-line'),
                        html.Div([
                            dbc.Label('Filter', className='mt-3', style={'color': '#FFFDFD', }), 
                            dcc.Dropdown(id='filterScatter3D')
                        ], id = 'secondary-dropdowns'),
                    ], id = 'dropdowns'),
                    html.Div([
                        dcc.Graph(id='figScatter3D',  config={'displayModeBar': True}),
                    ], id = 'graph')
                ], className = 'exploration-content')

cardSurface3D = html.Div([
                    html.Div([
                        dcc.Graph(id='figSurface3D',  config={'displayModeBar': True}),
                    ], id = 'absolutely-centered')
                ], className = 'exploration-content-centered')

cardMesh3D = html.Div([
                html.Div([
                    dbc.Label('X for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                    dcc.Dropdown(id='userXMesh3D'),
                    dbc.Label('Y for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                    dcc.Dropdown(id='userYMesh3D'),
                    dbc.Label('Z for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                    dcc.Dropdown(id='userZMesh3D'),
                ], id = 'dropdowns'),
                html.Div([
                    dcc.Graph(id='figMesh3D',  config={'displayModeBar': True}),
                ], id = 'graph')
            ], className = 'exploration-content')

cardDist = html.Div([
                html.Div([
                    html.Div([dbc.Label('Variable for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                    dcc.Dropdown(
                    id='userXDist'),
                    dbc.Label('Filter', className='mt-3', style={'color': '#FFFDFD', }), 
                    dcc.Dropdown(id='filterDist')
                    ], id = 'primary-dropdowns'),

                    html.Hr( id = 'sep-line'),

                    html.Div([
                        dbc.Checklist(id='normalize', inline=True, labelStyle = dict(display='inline'), options=[{'label': 'Normalize', 'value': 'yes'}])
                    ], id = 'secondary-dropdowns'),

                ], id = 'dropdowns'),
                
                html.Div([
                    dcc.Graph(id='figDist',  config={'displayModeBar': True}),
                ], id = 'graph')
        ], className = 'exploration-content')
 
cardHist = html.Div([
                html.Div([
                    dbc.Label('Variable for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                    dcc.Dropdown(
                    id='userXHist'),
                    dbc.Label('Filter', className='mt-3', style={'color': '#FFFDFD', }), 
                    dcc.Dropdown(id='filterhist')
                ], id = 'dropdowns'),
                html.Div([
                    dcc.Graph(id='figHist',  config={'displayModeBar': True})
                ], id = 'graph')
        ], className = 'exploration-content')

cardBar = html.Div([
            html.Div([
                html.Div([
                    dbc.Label('X for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                    dcc.Dropdown(
                    id='userXBar'
                    ),
                    dbc.Label('Y for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                    dcc.Dropdown(
                    id='userYBar'
                    ),
                ], id = 'main-dropdowns'),
                html.Hr( id = 'sep-line'),
                html.Div([dbc.Label('Filter', className='mt-3', style={'color': '#FFFDFD', }), 
                    dcc.Dropdown(id='filterBar'),
                ], id = 'secondary-dropdowns'),
            ], id = 'dropdowns'),
            html.Div([
                dcc.Graph(id='figBar',  config={'displayModeBar': True}),
            ], id = 'graph')
            ], className = 'exploration-content')


cardMatrix = html.Div([
                html.Div([
                    html.Div([
                        dbc.Label('Variables for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                        dcc.Checklist(
                        id='radioMatrix')
                    ], id = 'main-dropdowns'),
                    html.Hr( id = 'sep-line'),
                    html.Div([
                        dbc.Label('Filter', className='mt-3', style={'color': '#FFFDFD', }), 
                        dcc.Dropdown(id='filterMatrix')
                    ], id = 'secondary-dropdowns')
                ], id = 'dropdowns'),
                html.Div([
                    dcc.Graph(id='figMatrix',  config={'displayModeBar': True}),
                ], id = 'graph')
            ], className = 'exploration-content')

cardPie = html.Div([
            html.Div([
                dbc.Label('Variable for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                dcc.Dropdown(
                id='userXPie'),
                dbc.Label('Filter', className='mt-3', style={'color': '#FFFDFD', }), 
                dcc.Dropdown(id='filterPie')
            ], id = 'dropdowns'),

            html.Div([
                dcc.Graph(id='figPie',  config={'displayModeBar': True})
            ], id = 'graph')
        ], className = 'exploration-content')

cardBox = html.Div([
                html.Div([
                    html.Div([
                        dbc.Label('Variable for Plot', className='mt-3', style={'color': '#FFFDFD', }), 
                        dcc.Dropdown(
                        id='userYBox',style={'color':'#FFFDFD', 'background-color': '#060606', }
                        )
                    ], id = 'main-dropdowns'),
                    html.Hr( id = 'sep-line'),
                    html.Div([
                        dbc.Label('X Variable', className='mt-3', style={'color': '#FFFDFD', }), 
                        dcc.Dropdown(id='userXBox', style={'color':'#FFFDFD', 'background-color': '#060606', }),
                        dbc.Label('Filter', className='mt-3', style={'color': '#FFFDFD', }), 
                        dcc.Dropdown(id='filterBox', style={'color':'#FFFDFD', 'background-color': '#060606', })
                    ], id = 'secondary-dropdowns')
                ], id = 'dropdowns'),
                html.Div([
                    dcc.Graph(id='figBox',  config={'displayModeBar': True}),
                ], id = 'graph')
        ], className = 'exploration-content')

cardFitX = html.Div([
                html.P('X for Plot',), 
                dbc.RadioItems(
                id='radioIV')
            ])

cardScatterFit = html.Div([
                    dcc.Graph(id='figFit',  config={'displayModeBar': True})
                ], className = 'graph-parent')

cardFitX3D = html.Div([
                html.P('Var 1 for Plot'), 
                dbc.RadioItems(id='radioIV3D'),
                html.Hr(className = 'sep-line'),
                html.P('Var 2 for Plot'),
                dbc.RadioItems(id='radioIV3DZ')
            ])

cardScatterFit3D = html.Div([
                    dcc.Graph(id='figFit3D',  config={'displayModeBar': True})
                    ], className = 'graph-parent')


cardUpload = html.Div([
                dcc.Upload(
                    id='uploadData',
                    children=html.Div([
                    html.Img(id = 'Upload_Icon', src = 'data:image/png;base64,{}'.format(upload_icon_64)),
                    html.P(['Drag and Drop or ',html.A('Click to Upload a .CSV', id = 'Upload_Link')], id = 'Upload_Text'),
                    # html.A('Click to Files', id = 'Upload_Link')
                    ], id = 'upload_section_content'),
                    multiple=False
                    ),
                dbc.Tooltip(
                        '',
                        target='uploadData',
                        id='uploadToolTip'
                    ),
            ])




jumbotronHome = html.Div([
            html.H1('Welcome to regress.me', className='display-3', id = 'home_header'),
            html.P([
                'regress.me was designed to provide easy, efficient, and effective exploratory analysis for already cleaned datasets.', html.Br(),
                'You can visualize your data using a number of different graphs and fit regression models with no code.', html.Br(), 
                'Upload a .csv file (~50MB Max) to get started.'], id = 'home_text'
            ),
           cardUpload
    ],id = "home_page")