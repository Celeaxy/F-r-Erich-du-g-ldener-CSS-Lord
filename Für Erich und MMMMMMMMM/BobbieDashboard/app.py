import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output , State
import dash
import time
from dash_html_components.Iframe import Iframe
import pandas as pd
import random as r
import requests
from dash.exceptions import PreventUpdate
from requests.api import get
from scrapeNews import getNews
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform


#Dashboard written in Python dash
#Requirements to run. Logged in Browser Instance for HS and Zabbix. seleniumTestFirefoxMain.py is a script that provides automatic login with cookies.
#I ran in problems displaying Zabbix in IFrame on Chrome why im using Firefox -> !You have to have XFRAME Extensions for Firefox installed in order to see data from zabbix
# and the autologin script has to start its instance with that specific profil which has the extension installed further information is in the Script itself!
#Backend Flask , Frontend React.js , Diagram generating Assistant plotly.js
#Ever outside CSS can be easily placed in assets/style.css, not import is needed even though its a mess and you probably dont want to lock at it (:
#in assets you can set a favicon.ico displaying the icon of your application dash finds favicon.ico automatically
#data.json holds news with the tag german. Every hour it gets refreshed if the server is running
#overall we have a grid layout with 4 boxes for every different data:
#Hubspot -> going through a provided list of hubspot Urls shown in IFrame
#Zabbix ->  going through a provided list of hubspot Urls shown in IFrame
#NewsFeed -> getting Data from newsapi.org/tag=german (currently with my private key) storing it in data.json which gets updated every hour when the server is running,
#currently only displaying the title and the image of the news
#Rainfall Radar -> provided by https://www.rainviewer.com displayed in IFrame the view of radar should be costumizable via their website where you can generate a new link
#google meet Button -> Opens Google Meet Session, currently in the same browser tab, so after meeting you have to click back with browser
#User Interaction -> by clicking on Hubspot or Zabbix Frame you can skip to the next Diagram


#------------------------------------------------------------------------------------------------------------------------------------------------
#initialising global News variable and URLS outsourcing of data is planned

global newsJSON
newsJSON = pd.read_json(r'D:\Bobbie2.0\BobbieDashboard2.0-ScriptFirefox\BobbieDashboard\data.json')
hubspotUrls = ["https://app.hubspot.com/reports-dashboard/9232473/view/8358342","https://app.hubspot.com/reports-dashboard/9232473/view/8358360","https://app.hubspot.com/reports-dashboard/9232473/view/8358362","https://app.hubspot.com/reports-dashboard/9232473/view/8358354"]
zabbixUrls=["https://zabbix.bobbie.de/zabbix.php?action=dashboard.view&dashboardid=3","https://zabbix.bobbie.de/zabbix.php?action=dashboard.view&dashboardid=4","https://zabbix.bobbie.de/zabbix.php?action=dashboard.view&dashboardid=6","https://zabbix.bobbie.de/zabbix.php?action=dashboard.view&dashboardid=8","https://zabbix.bobbie.de/zabbix.php?action=dashboard.view&dashboardid=7","https://zabbix.bobbie.de/zabbix.php?action=dashboard.view&dashboardid=5"]


#------------------------------------------------------------------------------------------------------------------------------------------------
#get new Newsdata every hour put it into json


from apscheduler.schedulers.background import BackgroundScheduler


def scheduleTaskNews():
    global newsJSON
    getNews()
    newsJSON = pd.read_json(r'D:\Bobbie2.0\BobbieDashboard2.0-ScriptFirefox\BobbieDashboard\data.json')
    print("We are updating data.json")

scheduler = BackgroundScheduler()
scheduler.add_job(func=scheduleTaskNews, trigger="interval", seconds=60*60)
scheduler.start()
#------------------------------------------------------------------------------------------------------------------------------------------------
#initialising dash app with external stylesheets for dash bootstrap -> dbc

app = DashProxy(
    external_stylesheets=[dbc.themes.BOOTSTRAP],transforms=[MultiplexerTransform(proxy_location="inplace")]
)


#------------------------------------------------------------------------------------------------------------------------------------------------
#placeholder Function

def card_content():
    return [
        dbc.CardHeader("Hier stehen mal tolle Sachen"),
        dbc.CardBody(
            [
                html.Iframe(src="",style={"width":"100%","height":"100%"}),   
            ]
        ),
    ]


#------------------------------------------------------------------------------------------------------------------------------------------------
# defining grid layout for page -> 2 row and each row has 2 columns

cards = html.Div(
    [
        dbc.Row(
            [
                html.Div(dbc.Col(id="card1"),className="inlinecontainer",id="card1trigger"),
                html.Div(dbc.Col(id="card2"),className="inlinecontainer",id="card2trigger"),
                
            ],
            className="wrapper",
        ),
        dbc.Row(
            [
                html.Div(dbc.Col(id="card3"),className="inlinecontainer"),
                html.Div(dbc.Col(id="card4"),className="inlinecontainer"),
                
            ],
            className="wrapper",
        ),
      
    ],
    
className=""
)


#------------------------------------------------------------------------------------------------------------------------------------------------
#defining button for google meet and the Bobbie Image for top Page

button = dbc.Button("Google Meet", outline=True, color="success",id="googleMeet",size="lg",href="https://dash.plotly.com/dash-html-components/button")
bobbieImage = html.Img(src="https://www.bobbie.de/static/version1629715850/frontend/Bobbie/Theme/de_DE/images/logo.svg",style={"width":"10%","height":"10%"})


#------------------------------------------------------------------------------------------------------------------------------------------------
#general layout for page
#interval initialize callback function with the specific id name defining the time for the interval in -> 
# 1000 = 1 sekunde

def serve_layout():
    
    return html.Div([
        dcc.Interval(id='my-interval1', interval=20*1000),#card1 hubspot
        dcc.Interval(id='my-interval2', interval=20*1000),#card2 zabbix
        dcc.Interval(id='my-interval3', interval=80*1000),#card3 news           
        dcc.Interval(id='my-interval4', interval=80*1000),#card4 weather 
        dcc.Interval(id='intervalresetter', interval=8*1000,max_intervals=0),
        dcc.Interval(id='intervalresetter1', interval=8*1000,max_intervals=0),#card4 weather 
        dcc.Store(id='newsstorage', storage_type='memory'),#placeholder
        
        html.Div(bobbieImage,className="bobbieimage"),#topimage bobbie of webpage
        
        html.Div(cards,id="cards"),#predefined cards object gets put into div and gets id
        
        html.Div(button,className="button1"),#google meet button

        
    ])


#------------------------------------------------------------------------------------------------------------------------------------------------
#fully set app layout

app.layout = serve_layout


#------------------------------------------------------------------------------------------------------------------------------------------------


#callback functions are functions that are called from specific events either from intervals, button press or more complex calls.
#they can have multiple amounts of inputs aswell as outputs where you have to define the id and value of a component, example: 
# Input('myinterval'=id,'n-intervals'=number of times the interval has happened as int)
#it needs a decorator with @nameofyourapp.callback, it binds a function that only can be called via the callback
#output have to be dash components
#------------------------------------------------------------------------------------------------------------------------------------------------
#we will return dash bootstrap components and refresh them with the updated data
#------------------------------------------------------------------------------------------------------------------------------------------------
#on callback configuring the Card component for Hubspot 


#------------------------------------------------------------------------------------------------------------------------------------------------
#stop and reenabling timer when u click on Frame Hubspot to give buffer for the user when wanting to watch a specific chart not working cardtrigger 1 doesnt work for unknown reason
"""@app.callback(
    [Output('my-interval1', 'max_intervals'), Output('intervalresetter','max_intervals')],
    Input('intervalresetter','n_intervals')
)
def makeStuff(a):
    if a is None:
        return 0 , -1
    else:
        
        return -1 , 0
    


@app.callback(
    Output('intervalresetter', 'max_intervals'), 
    Input('card1trigger','n_clicks')
)
def makeStuff(a):
    if a is None:
        raise PreventUpdate
    return -1




#------------------------------------------------------------------------------------------------------------------------------------------------
#stop and reenabling timer when u click on Frame Zabbix to give buffer for the user when wanting to watch a specific chart
@app.callback(
    [Output('my-interval2', 'max_intervals'), Output('intervalresetter1','max_intervals')],
    [Input('intervalresetter1','n_intervals')]
)
def makeStuff(a):
    if a is None:
        return 0 , -1
        
    else:
        print("releasing stop")
        return -1 , 0
    


@app.callback(
    Output('intervalresetter1', 'max_intervals'), 
    [Input('card2trigger','n_clicks')]
)

def makeStuff(a):
    print(a)
    return -1
"""

#------------------------------------------------------------------------------------------------------------------------------------------------

@app.callback(
    [
        Output('card1', 'children'), 
        Output('my-interval1', 'n_intervals')
    ],
    [Input('my-interval1', 'n_intervals'), Input('card1trigger','n_clicks')])
def display_output(n,n1): 
    #n = intervals
    
    dashboards=hubspotUrls
    x=n
    ctx = dash.callback_context
    triggerdID = ctx.triggered[0]['prop_id'].split('.')[0]#finding out what triggered the callback in this case clicking on the Hubspot Card or the Interval
    
    if triggerdID == "card1trigger":
        x+=1
        if x >= len(dashboards):
            x=0
    
    
    #x is new interval              
    
    if x==None or x==-1:
        x=0
    #setting x for when server starts just get first element or when we are out of range
    
    karte =[
        dbc.CardHeader("Hubspot"),
        dbc.CardBody(
            [ 
                
                html.Iframe(src=dashboards[x],className="hubspot"),   
            ],

        className="outerdiv"),
    ]
    if x==len(dashboards)-1: #prevent index of out range Error
        x=-1
    return dbc.Card(karte, color="primary", inverse=True,className="fuckcss"),x


#------------------------------------------------------------------------------------------------------------------------------------------------
#on callback configuring the Card component for Zabbix

@app.callback(
    [
        Output('card2', 'children'), 
        Output('my-interval2', 'n_intervals')
    ],
    [Input('my-interval2', 'n_intervals'), Input('card2trigger','n_clicks')])
def display_output(n,n1):
    x1=n  
    
    #x1 is new interval              
    dashboards1=zabbixUrls

    ctx = dash.callback_context
    triggerdID = ctx.triggered[0]['prop_id'].split('.')[0]#finding out what triggered the callback in this case clicking on the Hubspot Card or the Interval
    
    if triggerdID == "card2trigger":
        x1+=1
        if x1 >= len(dashboards1):
            x1=0

    if x1==None or x1==-1:
        x1=0
    #setting x1 for when server starts just get first element
    karte =[
        dbc.CardHeader("Zabbix"),
        dbc.CardBody(
            [
                html.Iframe(src=dashboards1[x1],className="zabbix"),   
            ],
            className="outerdiv"
        ),
    ]
    if x1==len(dashboards1)-1:
        x1=-1
    return dbc.Card(karte, color="primary", inverse=True,className="fuckcss"),x1


#------------------------------------------------------------------------------------------------------------------------------------------------
#on callback configuring the Card component NewsFeed

@app.callback(
    Output('card3', 'children'),
    [Input('my-interval3', 'n_intervals'),State('newsstorage', 'data')])
def display_output(n,df):
    
    global newsJSON
    art=newsJSON["articles"][r.randint(0,len(newsJSON["articles"])-1)]
    
    karte =[
        dbc.CardHeader("News"),
        dbc.CardBody(html.Div(
            [
                html.H1(art["title"]),
                html.Img(src=art["urlToImage"],style={'height':'30%', 'width':'30%'}),                                     
                  
            ]
        ),
        className="")
    ]
    return dbc.Card(karte, color="primary", inverse=True,className="fuckcss")


#------------------------------------------------------------------------------------------------------------------------------------------------
#on callback configuring the Card component Weather

@app.callback(
    Output('card4', 'children'),
    [Input('my-interval4', 'n_intervals')])
def display_output(n):
    karte =[
        dbc.CardHeader("Weather"),
        dbc.CardBody(
            [
                html.Iframe(className="yeet",src="https://www.rainviewer.com/map.html?loc=52.5229,13.4033,5&oFa=0&oC=0&oU=0&oCS=1&oF=1&oAP=1&rmt=4&c=1&o=83&lm=0&th=0&sm=1&sn=1",style={"width":"100%","height":"100%"}),   
            ]
        ),
    ]
    return dbc.Card(karte, color="primary", inverse=True,className="fuckcss")


#------------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    app.run_server(debug=True)