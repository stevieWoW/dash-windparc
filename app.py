import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import *
import dash_daq as daq
import configparser
import numpy as np
import datetime
import logging
import DashPerformance 
import pandas as pd
import plotly.express as px

##################################################
#initialize the log file
logging.basicConfig(format = '%(asctime)s ' + "[%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s", filename='/var/log/Windparc/Windparc.log', level = logging.DEBUG)


##################################################
#Declare Variables

#load Data
Windmill = pd.read_csv('assets/windmills.csv',sep=';')[1:]
Weather = pd.read_csv('assets/weather.csv',sep=';')
Income = pd.read_csv('assets/windincomes.csv',sep=';')
Perf = pd.read_csv('assets/windperf.csv',sep=';')
Location = pd.read_csv('assets/windlocation.csv',sep=';')


month_name=["Januar","February","March","April","May","June","July","August","September","October","November","December"]

app = dash.Dash(__name__, meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])




##################################################
# some design patterns
design = {
    'colors' : {
        'background': 'rgb(30,30,30)',
        'text': 'rgb(127, 219, 255)',
        'BarPlan':'rgb(54,81,215)',
		'BarIs':'rgb(107,124,209)',
        'BarMedian':'rgb(255,0,127)',
        'BarInvest':'rgb(0,128,255)',
        'BarIncome':'rgb(255,255,102)',
        'BarTax':'rgb(255,153,153)',
        'BarWin':'rgb(0,153,0)',
        'BarLose':'rgb(153,0,0)',
        'PieType':['gold', 'mediumturquoise', 'darkorange']
    },

    'body' : {
        'backgroundColor': 'rgb(17,17,17)',
        'margin': '0px',
        'height': '1000px',
        'position' : 'relative'
    }
    
}

##################################################
#include the map
location = pd.read_csv("assets/WindparcLocation.csv")
figlocation = px.scatter_mapbox(location, lat="lat", lon="lon", hover_name="City", hover_data=["Location", "Number"],
                        color_discrete_sequence=["fuchsia"], zoom=11, height=500,color="Number", size="Number",
                        color_continuous_scale=px.colors.diverging.BrBG,size_max=20)
figlocation.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "openstreetmap.org",
            "source": [
                "https://c.tile.openstreetmap.org/{z}/{x}/{y}.png"
            ]
        }
      ])

figlocation.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


##################################################
app.layout = html.Div(style=design['body'],children=[
##################################################
# Header
    html.Div(id='header', children=[
        html.Div(id='logo',children=[
            html.Img(src='assets/windmill.png',className='windmill-1')
        ]),
        html.H1(
            children='WindParc - Dashboard - Development',
            style={
                'textAlign': 'center',
                'color': 'rgb(255,255,255)'
            }
        ),
        html.Div(children=' Lorup ', style={
            'textAlign': 'center',
            'color': 'rgb(180,180,180)'
        }),
    ]),
    
    
    html.Hr(),

# Header end
##################################################
##################################################
# sidemenu
    html.Div(id='sidemenu',className='sidenav',children=[
        html.H2('Settings',style={'color':'rgb(161, 159, 153)','margin':'2%'}),
        
        html.Hr(style={'border-color':'rgb(17,17,17)'}),
        html.H6('Aggregation',style={'color':'rgb(161, 159, 153)','margin':'2%'}),
        dcc.RadioItems(
            id='aggregation',
            options=[
                {'label': 'year', 'value': 'YEAR'},
                {'label': 'month', 'value': 'MONTH'},
                {'label': 'windmill', 'value': 'WINDMILL_ID'}
            ],
            value='MONTH',
            labelStyle={'display': 'inline-block'}
        ) ,
        html.Hr(style={'border-color':'rgb(40,40,40)','margin-left':'30px','margin-right':'30px'}),
        dcc.Dropdown(
            id='location',
            options=[{'label':label,'value':value} for label, value in zip(Location['LOCATION'], Location['ID'])],
            value='1',
            style={
                'width':'260px',
                'backgroundColor':'black',
                'color':'white',
                'margin':'2%'
                },
            clearable=False
        ),
##################################################
##################################################
# slideryear        
        html.Div(id='slideryear', className="col-10", children=[
            dcc.Checklist(
                id='check_box_year',
                options=[
                    {'label': 'year', 'value': 'true'},
                ],
                value = ['true']
            ),
            dcc.RangeSlider(
            id='range_slider_year',
            className='col-8',
            allowCross=False,
            value=[int( datetime.datetime.now().year) - 1 ,int(datetime.datetime.now().year)],
            step=1,
            min=2017,
            marks={i + 1: '{}'.format(i + 1) for i in range(2016,int(datetime.datetime.now().year),1)},
            max=int(datetime.datetime.now().year),
            #persistence=True,
            #persistence_type='session',
            updatemode='mouseup',
        )
        ]),
##################################################
##################################################
# slidermonth
        html.Div(id='slidermonth', className="col-10", children=[
            dcc.Checklist(
                id='check_box_month',
                options=[
                    {'label': 'month', 'value': 'true'},
                ],
            ),
            dcc.RangeSlider(
            id='range_slider_month',
            className='col-8',
            allowCross=False,
            value=[3,5],
            step=1,
            min=1,
            marks={i + 1: '{}'.format(i + 1) for i in range(12)},
            max=12,
            #persistence=True,
            #persistence_type='session',
            updatemode='mouseup',
        )
        ]),
##################################################
##################################################
# windmill
        html.Hr(style={'border-color':'rgb(40,40,40)','margin-left':'30px','margin-right':'30px'}),
        dcc.Dropdown(id='windmill',
        multi=True,
        #value=None,
        style={
            'width':'260px',
            'backgroundColor':'black',
            'color':'white',
            'margin':'2%',
            'float':'left'
            },
        clearable=False
        ),
        
        html.Button(id='button',style={'float':'left', 'display':'block','margin':'2%'},children='select')
    ]),
# Sidemenu end
##################################################
html.H1('Graphs',id='h1graph',style={'color':'rgb(161, 159, 153)'}),
html.Hr(id='graphhr',style={'border-color':'rgb(17,17,17)'}),
##################################################
# container for graphs
    html.Div(id='graphcontainer', children=[
# ##################################################
#graph one | Performance Bar
    html.Div(className='placeholdergraph col-10 bradius-4',children=[
        dcc.Checklist(id='median',
            options=[
                {'label': 'median', 'value': 'median'}
            ],
            value=[],
            style={'position':'absolute','z-index':'9999'}
        ),
        dcc.Graph(id='performance_bar',figure={
            'layout' :{
                'paper_bgcolor': design['colors']['background'],
                'plot_bgcolor': design['colors']['background'],
            }
        })  
    ]),
# end graph one
# ##################################################
# ##################################################
# graph two Invest
    html.Div(id='invest-div',className='placeholdergraph col-5 bradius-4',children=[
        dcc.Checklist(id='total_invest',
            options=[
                {'label': 'total', 'value': 'total'}
            ],
            value=[],
            style={'position':'absolute','z-index':'9999'}
        ),
        dcc.Graph(
            id='Invest',figure={
                'layout': {
                    'plot_bgcolor': design['colors']['background'],
                    'paper_bgcolor': design['colors']['background'],
                    'font': {
                        'color': design['colors']['text']
                        }
                }
            }

        )
    ]),
# end graph two
# ##################################################
# ##################################################
# graph three Windspeed
    html.Div(className='placeholdergraph col-5 bradius-4',children=[
        dcc.Checklist(id='windspeed_year',
        options=[
            {'label': 'per year', 'value': 'windspeedyear'}
        ],
        value=[],
        style={'position':'absolute','z-index':'9999'}
        ),
        dcc.Graph(
            id='Windspeed',
            figure={
                'layout': {
                    'plot_bgcolor': design['colors']['background'],
                    'paper_bgcolor': design['colors']['background'],
                    'font': {
                        'color': design['colors']['text']
                        }
                }
            }

        )
    ]),
# end graph three
# ##################################################
# ##################################################
# graph four | Performance Gauge
    html.Div(className='placeholdergraph col-4 bradius-4',children=[
        daq.Gauge(
            id='performance_gauge',
            showCurrentValue=True,
            units="%",
            color={"gradient":True,"ranges":{"red":[0,60],"yellow":[60,80],"green":[80,100]}},
            label='Performance',
            max=100,
            min=0
        )
    ]),
# # end graph four
# ##################################################
# ##################################################
# graph five | Windmill Number
    html.Div(className='placeholdergraph col-6 bradius-4',id="Windmill",children=[
        dcc.Graph(
            id='windmill_number',
            figure={
                'layout': {
                    'plot_bgcolor': design['colors']['background'],
                    'paper_bgcolor': design['colors']['background'],
                    'font': {
                        'color': design['colors']['text']
                        }
                }
            }
        )
    ]),
# end graph five
# ##################################################
# ##################################################
# graph six | Location
    html.Div(className='placeholdergraph col-10 bradius-4',children=[
        dcc.Graph(
            id='Location',
            figure=figlocation
        )
    ]),
# end graph six
    ])# Close GraphContainer
])# Close app.layout

##################################################
#start with callbacks

@app.callback(
    [
        Output('performance_gauge','value'),
        Output('performance_bar','figure'),
        Output('windmill_number','figure')
    ],
    [
        Input('button','n_clicks'),
        Input('median','value')
    ],
    [
        State('aggregation','value'),
        State('location','value'),
        State('check_box_year','value'),
        State('check_box_month','value'),
        State('range_slider_year','value'),
        State('range_slider_month','value'),
        State('windmill','value')
     ]
)
def UpdatePerformance(n_clicks,median,aggregation,location,check_box_year,check_box_month,range_slider_year,range_slider_month,windmill):
    '''Function to update the Performance Graph that shows PLAN/IS Values
    These values depends on the input of the Settings on the left side
    You can show the PLAN/IS of a single windmill, a parc or combined
    this function also affects Performance Gauge and Windmill Pie Chart'''

    #log some information
    logging.debug(f'Year: {check_box_year},{range_slider_year}')
    logging.debug(f'Month: {check_box_month},{range_slider_month}')
    logging.debug(f'Aggregation: {aggregation}')
    logging.debug(f'Location {location}')
    logging.debug(f'windmill: {windmill}')
    logging.debug(f'Median : {median}')

    # get the last maintained year 
    last_year = Perf.loc[Perf['ISPERFORMANCE'] == 0]['YEAR'].unique()

    #set hover header in performance_barchart
    if aggregation == "MONTH":
        if check_box_month:
            header=month_name[range_slider_month[0] - 1:range_slider_month[1]]
        else:
            header=month_name
    elif aggregation == "WINDMILL_ID":
        header=Windmill['WINDMILL']
        pass
    elif aggregation == "YEAR":
        h=[*range(range_slider_year[0],range_slider_year[1] + 1)]
        header=["YEAR"] * len(h)
        del h


    # transmit windmills if a location was picked
    if str(location) != '1' and not windmill:
        windmill = Windmill.loc[Windmill['LOCATION'] == location]
        windmill = windmill['WINDMILL_ID'].to_list()

    # create an Instance of DashPerformance
    dp = DashPerformance.DashPerformance(Perf,Windmill)

    # prepare dataframes
    if check_box_year and check_box_month:
        data = dp.check_box_year_month(
            range_slider_year,range_slider_month,windmill,aggregation
            )

    elif check_box_year and not check_box_month:
        data = dp.check_box_year(
            range_slider_year,range_slider_month,windmill,aggregation
            )
    
    elif check_box_month and not check_box_year:
        data = dp.check_box_month(
            range_slider_year,range_slider_month,windmill,aggregation
            )
    else:
        data = DashPerformance.DashPerformance.check_box_year(
            range_slider_year,range_slider_month,windmill,aggregation
            )

    logging.debug('data: {}'.format(data))

    # create list for Performance bar
    perf_bar_list = []

    # add values to perf_bar_list for the graph
    perf_bar_list.append({
        'x':dp.perf_bar[aggregation], 
        'y':dp.perf_bar.PLANPERFORMANCE, 
        'z':dp.perf_bar.ISPERFORMANCE,
        'type': 'bar',
        'text':header, 
        'name': 'Plan', 
        'marker':{
            'color':design['colors']['BarPlan']
            },
            'hovertemplate':"<extra></extra><b>%{text} </b> <br>PLAN: %{y} kWh", 
            'hoverinfo':'y'
        
    })

    perf_bar_list.append({
        'x':dp.perf_bar[aggregation], 
        'y':dp.perf_bar.ISPERFORMANCE, 
        'type': 'bar',
        'text':header, 
        'name': 'IS', 
        'marker':{
            'color':design['colors']['BarIs']
            },
            'hovertemplate':"<extra></extra><b>%{text} </b> <br>IS: %{y} kWh", 
            'hoverinfo':'y'
        
    })
    
    if median:
        perf_bar_list.append({
            'x':dp.perf_median[aggregation], 
            'y':dp.perf_median.ISPERFORMANCE, 
            'type': 'scatter',
            'text':header, 
            'name': 'median', 
            'marker':{
                'color':design['colors']['BarMedian']
                },
                'hovertemplate':"<extra></extra><b>%{text} </b> <br>IS: %{y} kWh", 
                'hoverinfo':'y'
            
        })
    dp.perf_median
    return dp.perf_gauge,{##### return values for bar
                'data': perf_bar_list,
                'layout':{
                    'title':'Energy Performance ' + "by " + str(aggregation),
                    'showlegend':True,
                    'legend':{'x':0,'y':"test"},
                    'margin':{'l':40,'r':0,'t':40,'b':30},
                    'plot_bgcolor':design['colors']['background'],
                    'paper_bgcolor':design['colors']['background'],
                    'fontcolor':design['colors']['text'],    
                }       
             },{#### return values for pie
                'data': [
                    {
                        'values': dp.pie_chart['WINDMILL_ID'].to_list(),
                        'labels':dp.pie_chart['TYPE'].to_list(),
                        'type': 'pie',
                        'name': 'windmilltype','marker':{'colors':design['colors']['PieType']}},
                
                ],
                'layout':{
                    'title':'Windmill',
                    'showlegend':True,
                    'legend':{'x':0,'y':"test"},
                    'margin':{'l':40,'r':0,'t':40,'b':30},
                    'plot_bgcolor':design['colors']['background'],
                    'paper_bgcolor':design['colors']['background'],
                    'fontcolor':design['colors']['text'],    
                }
            }
  

#################################################
@app.callback(
    Output('windmill','options'),
    [
        Input('location','value')
    ]
)
def GetWindmills(location):
    ''' Get the windmills based on the first dropdown. '''
    # check the location
    data = Windmill.copy()
    if str(location) == '1':
        # return all windmills 
        logging.info("return all Windmills")
        return [
            {'label':label,'value':value} for label, value in zip(data['WINDMILL'],data['WINDMILL_ID'])
        ]


    else:
        # return those within selected location
        logging.info(f'return Windmills from {location}')
        return [
            {'label':label,'value':value} \
            for label, value in zip(data.loc[data['LOCATION'] == location].WINDMILL,\
            data.loc[data['LOCATION'] == location].WINDMILL_ID)
        ]
##################################################
@app.callback(
    Output('Invest','figure'),
    [
        Input('button','n_clicks'),
        Input('total_invest','value')
     ],
    [
        State('aggregation','value'),
        State('check_box_year','value'),
        State('check_box_month','value'),
        State('range_slider_year','value'),
        State('range_slider_month','value')
     ]
)
def UpdateInvestGraph(n_clicks,total_invest,aggregation,check_box_year,check_box_month,range_slider_year,range_slider_month):
    '''function to show the deposit and income of the year based on the values of the year/month slider'''

    # # return values of deposit and income
    return {
            'data': [
                {'x': [0],'y': [40000], 'type': 'bar', 'name': 'Invest', 'marker':{'color': design['colors']['BarInvest']}},
                {'x': [0],'y': [10000], 'type': 'bar', 'name': 'Income', 'marker':{'color': design['colors']['BarIncome']}},
                {'x': [0],'y': [2000],'type': 'bar', 'name': 'Tax', 'marker':{'color': design['colors']['BarTax']}},
                {'x': [0],'y': [8000],'type': 'bar', 'name': 'Win', 'marker':{'color': design['colors']['BarWin'] if 8000 >= 0 else design['colors']['BarLose']}}
            ],
            'layout':{
                'title':'Investment ',
                'showlegend':True,
                'legend':{'x':0,'y':"test"},
                'margin':{'l':40,'r':0,'t':40,'b':30},
                'plot_bgcolor':design['colors']['background'],
                'paper_bgcolor':design['colors']['background'],
                'fontcolor':design['colors']['text'],    
            }        
        }



##################################################
@app.callback(
    Output('Windspeed','figure'),
    [
        Input('button','n_clicks'),
        Input('windspeed_year','value')
    ],
    [
        State('aggregation','value'),
        State('check_box_year','value'),
        State('check_box_month','value'),
        State('range_slider_year','value'),
        State('range_slider_month','value')
     ]
)
def UpdateWindspeedGraph(n_clicks,windspeed_year,aggregation,check_box_year,check_box_month,range_slider_year,range_slider_month):
    '''function to show the Windpeed of the selected slider Year/month'''

    # convert Date to Datetime
    Weather['DATE'] = pd.to_datetime(Weather['DATE']).dt.strftime('%Y-%m')
    # group Windspeed by year month 
    data = Weather.groupby(['DATE'],as_index=False).mean()[['DATE','WINDSPEED']]

    # convert Date to Datetime once more
    data['DATE'] = data['DATE'].apply(pd.to_datetime)
    # set Year
    data['YEAR'] = data['DATE'].dt.strftime('%Y')
    # set month
    data['MONTH'] = data['DATE'].dt.strftime('%m')

    # convert Year, Month to numeric
    data[['YEAR','MONTH']] = data[['YEAR','MONTH']].apply(pd.to_numeric)

    # checkbox Year and/or Month were checked
    if check_box_year and check_box_month:
        # create df from selected year and month
        data = data.loc[(data['YEAR'] >= range_slider_year[0]) & (data['YEAR'] <= range_slider_year[1])]
        data = data.loc[(data['MONTH'] >= range_slider_month[0]) & (data['MONTH'] <= range_slider_month[1])]

    elif check_box_year and not check_box_month: 
        # create df from selected years
        data = data.loc[(data['YEAR'] >= range_slider_year[0]) & (data['YEAR'] <= range_slider_year[1])]

    elif check_box_month and not check_box_year:
        # create df from selected months
        data = data.loc[(data['MONTH'] >= range_slider_month[0]) & (data['MONTH'] <= range_slider_month[1])]

    data = data.set_index('YEAR')
    
    r_data = []
    if windspeed_year: 
        data = data.reset_index()
        for year in range(range_slider_year[0],range_slider_year[1]):
            r_data.append({'x':data.loc[data['YEAR'] == year]['MONTH'], 'y':data.loc[data['YEAR'] == year]['WINDSPEED'], 'name': f'Windspeed {year}'})
    else:
        r_data = [{
            'x':data.DATE,'y':data.WINDSPEED, 'name':f'Windspeed'
        }]
        # return collected data
    return {
        'data': r_data,
        'layout':{
                'title':'Windspeed by MONTH',
                'showlegend':True,
                'legend':{'x':0,'y':"test"},
                'margin':{'l':40,'r':0,'t':40,'b':30},
                'plot_bgcolor':design['colors']['background'],
                'paper_bgcolor':design['colors']['background'],
                'fontcolor':design['colors']['text'],    
            }        
    }

##################################################
##################################################
#start the server

#server = app.server # for production
if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0',port='8071')
