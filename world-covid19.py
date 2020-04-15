import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import requests
import io
import json
from dash.dependencies import Input,Output
from datetime import date,datetime,timedelta
import plotly.graph_objects as go
from bs4 import BeautifulSoup
import re

external_stylesheet = ["https://codepen.io/chriddyp/pen/dZVMbK.css"]


headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
url = "https://www.worldometers.info/coronavirus/?//"
req = requests.get(url, headers)
soup = BeautifulSoup(req.content, 'html.parser')

str1 = str(soup.find_all(class_='maincounter-number'))

l = []
l = str1.split('>')
list1 = l[2].split('<')
total_confirmed = list1[0]
total_confirmed = re.split(r'[;,\s]\s*',total_confirmed)
del total_confirmed[3]
s = ''
for element in total_confirmed:
    s = s+element
total_confirmed1 = int(s)


list2 = l[6].split('<')
total_deaths = list2[0]
total_deaths = re.split(r'[;,\s]\s*',total_deaths)
s = ''
for element in total_deaths:
    s = s+element
total_deaths1 = int(s)

list3 = l[10].split('<')
total_recovered = list3[0]
total_recovered = re.split(r'[;,\s]\s*',total_recovered)
s = ''
for element in total_recovered:
    s = s+element
total_recovered1 = int(s)

active_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
deaths_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
recovered_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv" 
s = requests.get(active_url).content
active_df = pd.read_csv(io.StringIO(s.decode('utf-8')))

s = requests.get(deaths_url).content
deaths_df = pd.read_csv(io.StringIO(s.decode('utf-8')))

s = requests.get(recovered_url).content
recovered_df = pd.read_csv(io.StringIO(s.decode('utf-8')))

dates = []
day = '22/Jan/2020'
day1 = '22/Jan'
# today_date = datetime.datetime.today()
# print(today_date)
delta = date.today()-date(2020,1,22)
diff = int(delta.days)
dates.append(day1)
for i in range(1,diff+2):
    dt = datetime.strptime(day, '%d/%b/%Y')
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=i)
    dates.append(end.strftime('%d/%b'))
del dates[0]
del dates[0]

# print(len(active_df.columns))

last_col = active_df.columns[len(active_df.columns)-1]
print(last_col)


total_active = int(active_df.sum(axis=0)[last_col])
total_deceased = int(deaths_df.sum()[last_col])
total_recovered = int(recovered_df.sum()[last_col])

active_df1 = active_df.groupby(by=['Country/Region']).sum()
recovered_df1 = recovered_df.groupby(by=['Country/Region']).sum()
deaths_df1 = deaths_df.groupby(by=['Country/Region']).sum()

recovered_df1.reset_index(inplace=True)
active_df1.reset_index(inplace=True)
deaths_df1.reset_index(inplace=True)

top10_active = active_df1.nlargest(10,[last_col])
top10_recovered = recovered_df1.nlargest(10,[last_col])
top10_deaths = deaths_df1.nlargest(10,[last_col])
# print(top10_active)

def reemovNestings(l,output): 
        for i in l: 
                if type(i) == list: 
                        reemovNestings(i,output) 
                else: 
                        output.append(i) 
        return output

def update_top10_active():
        traces = []
        top10 = top10_active['Country/Region'].to_numpy()
        top10_active.drop(['Lat','Long'],axis=1,inplace=True)
        # print(top10_active)

        
        for country in top10:
                country_row = top10_active[top10_active['Country/Region']==country]
                country_row.drop(['Country/Region'],axis=1,inplace=True)
                data_list = []
                
                for col in country_row.columns:
                        # print(type(country_row[col]))
                        ser = country_row[col].tolist()
                        data_list.append(ser)
                empty_list = []
                
                data_list = reemovNestings(data_list,empty_list)
                # print((data_list))
                traces.append(go.Scatter(x=dates,y=data_list,name=country,mode='lines+markers'))
        
        return {'data':traces,'layout':go.Layout(title='Top 10 Countries with Highest Number of Confirmed Cases')}

def update_top10_recovered():
        traces = []
        top10 = top10_recovered['Country/Region'].to_numpy()
        top10_recovered.drop(['Lat','Long'],axis=1,inplace=True)
        
        for country in top10:
                country_row = top10_recovered[top10_recovered['Country/Region']==country]
                country_row.drop(['Country/Region'],axis=1,inplace=True)
                data_list = []
                
                for col in country_row.columns:
                        # print(type(country_row[col]))
                        ser = country_row[col].tolist()
                        data_list.append(ser)
                empty_list = []
                
                data_list = reemovNestings(data_list,empty_list)
                # print((data_list))
                traces.append(go.Scatter(x=dates,y=data_list,name=country,mode='lines+markers'))
        
        return {'data':traces,'layout':go.Layout(title='Top 10 Countries with Highest Number of Recoveries')}

def update_top10_deaths():
        traces = []
        top10 = top10_deaths['Country/Region'].to_numpy()
        top10_deaths.drop(['Lat','Long'],axis=1,inplace=True)
        
        for country in top10:
                country_row = top10_deaths[top10_deaths['Country/Region']==country]
                country_row.drop(['Country/Region'],axis=1,inplace=True)
                data_list = []
                
                for col in country_row.columns:
                        # print(type(country_row[col]))
                        ser = country_row[col].tolist()
                        data_list.append(ser)
                empty_list = []
                
                data_list = reemovNestings(data_list,empty_list)
                # print((data_list))
                traces.append(go.Scatter(x=dates,y=data_list,name=country,mode='lines+markers'))
        
        return {'data':traces,'layout':go.Layout(title='Top 10 Countries with Highest Number of Fatalities')}



        
        


app = dash.Dash(__name__,external_stylesheets=external_stylesheet)
server = app.server

app.layout = html.Div(id='main-container',children = [
                    html.Div(id='top-bar',children = [
                        html.P('\n\nCOVID-19 DASHBOARD',style={'fontSize':35,'color':'#ffffff','fontFamily':'Helvetica','textAlign':'center',
                        'marginBottom':'2%'})
                    ],style={'marginLeft':'0%','marginRight':'0%','width':'100%','marginTop':'0%','marginBottom':'2%'}),
                    

                    html.Div(id='dashboard-main',children=[
                        html.Div(id='confirmed-cases',style={'display':'inline-block','marginLeft':'5%','marginRight':'1%','width':'27.7%',
                                                            'textAlign':'center','backgroundColor':'black'},
                                children=[html.P('Total Confirmed',style={'color':'#F3E80E','fontSize':18,'frontWeight':'bold','fontFamily':'Helvetica'}),
                                        html.H1(id = 'total_active',style={'color':'#F3E80E','fontFamily':'Helvetica'})]),
                        html.Div(id='recovered-cases',style={'display':'inline-block','marginLeft':'2%','marginRight':'1%','width':'27.7%',
                                                            'textAlign':'center','backgroundColor':'black'},
                                children=[html.P('Total Recovered',style={'color':'#0EC829','fontSize':18,'frontWeight':'bold','fontFamily':'Helvetica'}),
                                        html.H1(id='total_recovered',style={'color':'#0EC829','fontFamily':'Helvetica'})]),
                        html.Div(id='death-cases',style={'display':'inline-block','marginLeft':'1%','marginRight':'3%','width':'27.7%',
                                                            'textAlign':'center','backgroundColor':'black'},
                                children=[html.P('Total Deaths',style={'color':'#D2062D','fontSize':18,'frontWeight':'bold','fontFamily':'Helvetica'}),
                                        html.H1(id='total_deceased',style={'color':'#D2062D','fontFamily':'Helvetica'})])
                        
                    ],style={'marginTop':'4%','marginBottom':'2%'}),
                

               
                    html.Div([
                            html.Pre('Recovery Rate: {:.2f}%'.format((total_recovered1/total_confirmed1)*100),style={'color':'#3deb34','fontWeight':'bold',
                                    'fontFamily':'Helvetica','textAlign':'center','fontSize':18}),
                            html.Pre('Fatality Rate: {:.2f}%'.format((int(total_deaths1)/int(total_confirmed1))*100),style={'color':'#e31212','fontWeight':'bold',
                                    'fontFamily':'Helvetica','textAlign':'center','fontSize':18})
                           
                    ]),

                     html.Div(
                                children=[
                        dcc.Tabs(colors={'border':'white','background':'gold','primary':'gold'},
                                style={'fontFamily':'Helvetica','fontSize':16,'marginLeft':'2%','width':500},children=[
                            dcc.Tab(label='Visualize COVID-19 Trends',children=[
                                        html.Div(id='map-area',children=[
                                                              dcc.Graph(id='current-map',figure={'data':[go.Choropleth(locations=deaths_df1['Country/Region'],locationmode='country names',
                                                                            z=active_df1[last_col]-(deaths_df1[last_col]+recovered_df1[last_col]),colorscale='sunset')],
                                                                    'layout':go.Layout(title='Currently Active Cases Worldwide',autosize=False,height=600,width=1200)},
                                                              style={'color':'#eeeeee'})


                                         ],style={'marginBottom':'0.5%','marginTop':'0.5%','marginRight':'2%','marginLeft':'2%'}),
                                         html.Div(id='map-area1',children=[
                 
                                                                dcc.Graph(id='active-map',figure={'data':[go.Choropleth(locations=active_df1['Country/Region'],locationmode='country names',
                                                                            z=active_df1[last_col],colorscale='Blues')],
                                                                    'layout':go.Layout(title='Total Confirmed Cases Worldwide',autosize=False,height=600,width=1200)},
                                                                style={'color':'#eeeeee'})
                                         ],style={'marginBottom':'0.5%','marginTop':'0.5%','marginRight':'2%','marginLeft':'2%'}),

                                        html.Div([
                                                dcc.Graph(figure=update_top10_active())
                                        ],style={'marginRight':'2%','marginLeft':'2%','marginTop':'1%','marginBottom':'1%'}),
                   
                                         html.Div(id='map-area2',children=[
                                                                        dcc.Graph(id='deaths-map',figure={'data':[go.Choropleth(locations=deaths_df1['Country/Region'],locationmode='country names',
                                                                            z=deaths_df1[last_col],colorscale='Reds')],
                                                                    'layout':go.Layout(title='Number of Deaths Worldwide',autosize=False,height=600,width=1200,)},
                                                                        style={'color':'#eeeeee'})


                                         ],style={'marginBottom':'0.5%','marginTop':'0.5%','marginRight':'2%','marginLeft':'2%'} ),
                                
                                        html.Div([
                                                dcc.Graph(figure=update_top10_deaths())
                                        ],style={'marginRight':'2%','marginLeft':'2%','marginTop':'1%','marginBottom':'1%'}),
                    
                                        html.Div(id='map-area3',children=[
                                                                dcc.Graph(id='recovery-map',figure={'data':[go.Choropleth(locations=recovered_df1['Country/Region'],locationmode='country names',
                                                                            z=recovered_df1[last_col],colorscale='Greens')],
                                                                    'layout':go.Layout(title='Number of Recoveries Worldwide',autosize=False,height=600,width=1200,)},
                                         style={'color':'#eeeeee'})],style={'marginBottom':'0.5%','marginTop':'0.5%','marginRight':'2%','marginLeft':'2%'} ),
                    
                                        html.Div([
                                                 dcc.Graph(figure=update_top10_recovered())
                                         ],style={'marginRight':'2%','marginLeft':'2%','marginTop':'1%','marginBottom':'1%'}),

                                         dcc.Interval(id='interval_component',interval=10000,n_intervals=0)

                                        
                                ]),
                        dcc.Tab(label='Country Status',children=[
                                html.Div(children=[
                                html.H2('Select a Country',style={'textAlign':'center','fontFamily':'Helvetica','color':'#ffffff','marginBottom':'1%'}),
                                dcc.Dropdown(id='country-dropdown',options=[{'label':i,'value':i} for i in active_df1['Country/Region'].unique()],value='US'),
                                dcc.Graph(id='country-status')
                        ],style={'marginLeft':'2%','marginRight':'2%','marginTop':'4%'})
                                ])
                        ])
                ]),
                html.Div([
                        html.Footer([
                                html.P(''),
                                html.P(''),
                                html.P('Created by - Gurjinder Kaur'),
                                html.P('STAY HOME STAY SAFE')
                        ],style={
                                'textAlign':'center','fontFamily':'Helvetica','fontSize':'14','color':'#ffffff','marginTop':'5%'
                        })
                ],style={'backgroundColor':'#000000','height':80})
                    

],style={'backgroundColor':'#1c0f57'})



@app.callback(Output('country-status','figure'),[Input('country-dropdown','value')])
def update_country_status(selected_country):
        country_row = active_df1[active_df1['Country/Region']==selected_country]
        country_row.drop(['Country/Region','Lat','Long'],axis=1,inplace=True)
        data_list = []

        for col in country_row.columns:
                ser = country_row[col].tolist()
                data_list.append(ser)
        empty_list = []
        data_list = reemovNestings(data_list,empty_list)
        trace1 = go.Scatter(x=dates,y=data_list,name='Total',mode='lines+markers',marker={'color':'#1c0f57'})

        country_row2 = recovered_df1[recovered_df1['Country/Region']==selected_country]
        country_row2.drop(['Country/Region','Lat','Long'],axis=1,inplace=True)

        data_list2 = []
        for col in country_row2.columns:
                ser = country_row2[col].tolist()
                data_list2.append(ser)
        data_list2 = reemovNestings(data_list2,[])
        trace2 = go.Scatter(x=dates,y=data_list2,mode='lines+markers',name='Recovered',marker={'color':'#3deb34'})

        country_row3 = deaths_df1[deaths_df1['Country/Region']==selected_country]
        country_row3.drop(['Country/Region','Lat','Long'],axis=1,inplace=True)

        data_list3 = []
        for col in country_row3.columns:
                ser = country_row3[col].tolist()
                data_list3.append(ser)
        data_list3 = reemovNestings(data_list3,[])
        trace3 = go.Scatter(x=dates,y=data_list3,mode='lines+markers',name='Deaths',marker={'color':'#e31212'})

        return {'data':[trace1,trace2,trace3],'layout':go.Layout(title='Status of {}'.format(selected_country))}



@app.callback(Output('total_active','children'),
                [Input('interval_component','n_intervals')])
def update_live_confirmed(n):
        headers = requests.utils.default_headers()
        headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
        url = "https://www.worldometers.info/coronavirus/?//"
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')

        str1 = str(soup.find_all(class_='maincounter-number'))

        l = []
        l = str1.split('>')
        list1 = l[2].split('<')
        total_confirmed = list1[0]

        list2 = l[6].split('<')
        total_deaths = list2[0]

        list3 = l[10].split('<')
        total_recovered = list3[0]

        return total_confirmed

@app.callback(Output('total_recovered','children'),
                [Input('interval_component','n_intervals')])
def update_live_recovered(n):
        headers = requests.utils.default_headers()
        headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
        url = "https://www.worldometers.info/coronavirus/?//"
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')

        str1 = str(soup.find_all(class_='maincounter-number'))

        l = []
        l = str1.split('>')
        list1 = l[2].split('<')
        total_confirmed = list1[0]

        list2 = l[6].split('<')
        total_deaths = list2[0]

        list3 = l[10].split('<')
        total_recovered = list3[0]

        return total_recovered

@app.callback(Output('total_deceased','children'),
                [Input('interval_component','n_intervals')])
def update_live_deceased(n):
        headers = requests.utils.default_headers()
        headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
        url = "https://www.worldometers.info/coronavirus/?//"
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')

        str1 = str(soup.find_all(class_='maincounter-number'))

        l = []
        l = str1.split('>')
        list1 = l[2].split('<')
        total_confirmed = list1[0]

        list2 = l[6].split('<')
        total_deaths = list2[0]

        list3 = l[10].split('<')
        total_recovered = list3[0]

        return total_deaths



if __name__=='__main__':
    app.run_server()
    