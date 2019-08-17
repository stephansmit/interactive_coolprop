# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.plotly as py

from distribution import *
from point import *
from line import *
from surface import *
from fluid import *



camera = dict(
    up=dict(x=0, y=0, z=1),
    center=dict(x=-0.45, y=0, z=0),
    eye=dict(x=1.5, y=-2, z=0.5)
)
layout = go.Layout(
	margin=dict(
                    r=10, l=10,
                    b=10, t=10),
        scene = dict(
            camera=camera,
            xaxis = dict(title = 'Specific Volume [m^3/kg]',type='log'),
            yaxis = dict(title = 'Temperature [K]'),
            zaxis = dict(title = 'Pressure [Pa]',type='log'),
       ),
        legend= dict(
            x = 0
       ),
)



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



database = dict()
fluids = ['Water']
for name in fluids:
    fluid = Fluid(name)
    database['Water']=fluid.getData(go)
print("created the figure")
fig = go.FigureWidget(data=[database['Water']['surface']['S']]+ database['Water']['phase'],layout=layout)
def check_variable(fig):
    if "Entropy" in fig.data[0].colorbar.title.text:
        return "S"
    elif "Enthalpy" in fig.data[0].colorbar.title.text:
        return "H"
    elif "Vapour" in fig.data[0].colorbar.title.text:
        return "Q"
    elif "Compressibility" in fig.data[0].colorbar.title.text:
        return "Z"
    elif "Pressure" in fig.data[0].colorbar.title.text:
        return "P"
    else:
        raise NotImplementedError

def getCamera(fig):
    return fig.layout.scene.camera


def setCamera2(fig):
    fig.layout.scene.camera = getCamera(fig)
    return fig


def setCamera(fig, position):
    if position == 'Default':
        fig.layout.scene.camera.up=dict(x=0, y=0, z=1)
        fig.layout.scene.camera.center=dict(x=-0.45, y=0, z=0)
        fig.layout.scene.camera.eye=dict(x=1.5, y=-2, z=0.5)
    elif position == "PV":
        fig.layout.scene.camera.eye = dict(x=0, y=-1.5, z=0)
        fig.layout.scene.camera.up=dict(x=0, y=0, z=1)
        fig.layout.scene.camera.center=dict(x=-0, y=0, z=0)
    elif position == "TV":
        fig.layout.scene.camera.eye = dict(x=0, y=0, z=1.5)
        fig.layout.scene.camera.up=dict(x=0, y=1, z=0)
        fig.layout.scene.camera.center=dict(x=0, y=0, z=0)

    elif position == "PT":
        fig.layout.scene.camera.eye = dict(x=1.5, y=0, z=0)
        fig.layout.scene.camera.up=dict(x=0, y=0, z=-1)
        fig.layout.scene.camera.center=dict(x=-0, y=0, z=0)
    else:
        raise NotImplementedError
    return fig


def getName(fig):
    return  fig.layout.title.text.split(" ")[-1]
        
fig = go.FigureWidget(data=[database['Water']['surface']['S']]+ database['Water']['phase'],layout=layout)


def set_contours(contours):
    if "P" in contours:
        fig.data[0].contours.z.show=True
    else:
        fig.data[0].contours.z.show=False
    if "T" in contours:
        fig.data[0].contours.y.show=True
    else:
        fig.data[0].contours.y.show=False
    return fig

def set_perspective(fig, perspective):
    fig = setCamera2(fig)
    fig.layout.scene.camera.projection.type= perspective
    return fig

def change_fluid(name, variable):
    if name not in database.keys():
        fluid = Fluid(name)
        database[name]=fluid.getData(go)
    with fig.batch_update():
        for j, element in enumerate(fig.data[0]):
            fig.data[0][element]=database[name]['surface'][variable][element]
        for i,d in enumerate(fig.data[1:]):
            for j, element in enumerate(d):
                fig.data[i+1][element]=database[name]['phase'][i][element]
    return fig        

def getFig():
    return fig


app.layout = html.Div(children=[
    html.H1(children='Interactive p-v-T diagram',
            style={
            'textAlign': 'center'
            }),


    html.Div([
        dcc.Graph(
            id='example-graph',
            figure = fig)
        ], style={"width":"70%","display":"block", "margin-left": "auto", "margin-right": "auto", "class":"center"}),
    
    html.Div([
        html.Label('Fluid'),
        dcc.Dropdown(
            id='my-dropdown',
            options=[
                {"label":"CO2", "value":"CO2"},
                {"label":"Water", "value":"Water"},
                {"label":"Toluene", "value":"Toluene"},
                {"label":"Methane", "value":"Methane"},
                {"label":"Benzene", "value":"Benzene"},
                {"label":"m-Xylene", "value":"m-Xylene"},
                {"label":"Xenon", "value":"Xenon"},
                {"label":"Nitrogen", "value":"Nitrogen"},
                {"label":"Helium", "value":"Helium"},
                {"label":"Hydrogen", "value":"Hydrogen"},
                {"label":"Ammonia", "value":"Ammonia"},
                {"label":"Ethane", "value":"Ethane"},
                {"label":"Krypton", "value":"Krypton"},
                {"label":"Pentane", "value":"Pentane"},
                {"label":"Octane", "value":"Octane"},
                {"label":"Decane", "value":"Decane"},

            ],
            value='Water'
        ),
        html.Label('Variable'),
        dcc.Dropdown(
            id='my-dropdown2',
            options=[
                {'label': 'Entropy', 'value': 'S'},
                {'label': 'Vapour Fraction', 'value': 'Q'},
                {'label': 'Enthalpy', 'value': 'H'},
                {'label': 'Compressibility', 'value': 'Z'},
                {'label': 'Pressure', 'value': 'P'},                
            ],
            value='S'
            ),
        html.Div([

            html.Div([
            html.Label('Camera Position'),
            dcc.RadioItems(
                 id='my-radio2',
                 options=[
                     {'label': 'Default', 'value': 'Default'},
                     {'label': 'P-T', 'value': 'PT'},
                     {'label': 'P-V', 'value': 'PV'},
                     {'label': 'T-V', 'value': 'TV'},

                 ],
                 value="Default"
                 )],style={'width': '31%', 'display': 'inline-block','vertical-align': 'top'}),
            html.Div([
                html.Label('Perspective'),
                dcc.RadioItems(
                 id='my-radio',
                 options=[
                     {'label': 'Perspective', 'value': 'perspective'},
                     {'label': 'Orthograpic', 'value': 'orthographic'},
                 ],
                 value='perspective'
                 )],style={'width': '31%', 'display': 'inline-block', "vertical-align":'top'}),
            html.Div([
                html.Label('Contours'),
                dcc.Checklist(
                 id='checkbox',
                 options=[
                     {'label': 'Temperature', 'value': 'T'},
                     {'label': 'Pressure', 'value': 'P'},
                 ],
                 values=['T']
                 )],style={'width': '31%', 'display': 'inline-block', "vertical-align":'top'}),

        ])
       ], style={'width': '40%',"display":"block", "margin-left": "auto", "margin-right": "auto", "class":"center"}),

    ], style={'marginBottom': 10, 'marginTop': 10, "marginLeft":10, "marginRight":10, "textAlign":'center'})
@app.callback(
    dash.dependencies.Output('example-graph', 'figure'),
    [dash.dependencies.Input('my-dropdown', 'value'),
    dash.dependencies.Input('my-dropdown2', 'value'),
    dash.dependencies.Input('my-radio', 'value'),
    dash.dependencies.Input('my-radio2', 'value'),
    dash.dependencies.Input('checkbox', 'values')])
def change_figure(name, variable, perspective, position,contours):
    ctx = dash.callback_context
    fig = getFig()
    
    if (ctx.triggered[0]['prop_id'] == "my-dropdown.value") or (ctx.triggered[0]['prop_id'] == "my-dropdown2.value"):
       fig = change_fluid(name,variable)
    
    if ctx.triggered[0]['prop_id'] == 'checkbox.values':
        fig = set_contours(contours)
    
    if ctx.triggered[0]['prop_id'] == 'my-radio.value':
        fig = set_perspective(fig, perspective)
    
    if ctx.triggered[0]['prop_id'] == 'my-radio2.value':
        fig = setCamera(fig,position)
    return fig




if __name__ == '__main__':
    app.run_server(debug=True)



