#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import plotly.express as px
import pandas as pd


# In[2]:


## producing a simple scatter plot
x = list(np.random.random(100))
y = list(np.random.random(100))
s = list(np.random.random(100)) ## varying cicle size
c = list(np.random.random(100)) ## varying colour

df = pd.DataFrame({'x':x,'y':y,'s':s})
fig = px.scatter(df,x=x,y=y,size="s") ## setting axis with equals sign
fig.show()


# In[3]:


import plotly.graph_objects as go

fig = go.Figure(go.Scatter(x=[0,0,2,2,0],y=[0,1,1,0,0],fill="toself")) ## example of a rectangular shape
fig.show()


# In[6]:


fig=go.Figure()
fig.add_shape(type="rect",
    x0=1, y0=1, x1=2, y1=3,
    line=dict(color="RoyalBlue"),
)
fig.add_shape(type="rect",
    x0=3, y0=1, x1=6, y1=2,
    line=dict(
        color="RoyalBlue",
        width=2,
    ),
    fillcolor="LightSkyBlue",
)
## creating multiple shapes


# In[5]:


from bokeh.plotting import figure,show
import numpy as np

x = np.random.random(50)*10
y = np.random.random(50)*200

p = figure(title="Scatter plot",
          x_axis_label = "x axis",
          y_axis_label = "y axis")

p.circle(x=x, y=y,legend_label ="Points",color="blue",size=5)
show(p)


# In[40]:


from bokeh.plotting import figure,show
import numpy as np

x = np.arange(0,5,1)
y = np.random.random(5)*100

p = figure(title="Bar plot",
          x_axis_label = "x axis",
          y_axis_label = "y axis")

p.vbar(x=x, top=y,width=0.5,color="red",bottom=0)
show(p)


# In[67]:


## Data retrieval
import pandas as pd
import ssl
import time
import datetime

def get_df(addr):
    ssl._create_default_https_context = ssl._create_unverified_context
    transactions_url = 'https://blockchain.info/rawaddr/' + addr
    df = pd.read_json(transactions_url)
    time.sleep(10)
    return df

def find_transactions(df): 
    transactions = df['txs']
    return transactions 

def find_inputaddr(df,address):
    inputs = find_transactions(df) 
    inadr = []
    for i in inputs:
        input = i['inputs'][0]['prev_out']['addr']
        inadr.append(input)
    return inadr

def find_outputaddr(df):
    outputs = find_transactions(df) 
    adr = []
    for i in outputs:
        output = i['out'][0]['addr']
        adr.append(output)
    return adr

def find_amounts(df):
    amounts = find_transactions(df)
    amt = []
    for a in amounts:
        amount = a['result']
        amt.append(amount)
    return amt

def find_time(df):
    times = []
    for t in find_transactions(df):
        time = t['time']
        times.append(time)
    return times
        
## vertical plotting
def get_branches(number):
    brn = []
    for b in range(number):
        brnch = find_outputaddr(df)[b]
        brn.append(brnch)
    return brn

def get_inbranches(number):
    inbrn = []
    for i in range(number+1)[1:]:
        inbrnch = find_inputaddr(df,address=addr)[i]
        inbrn.append(inbrnch)
    return inbrn

def get_branch_amt(number):
    brnamt = []
    for a in range(number):
        amount = find_amounts(df)[a]
        brnamt.append(amount)
    return brnamt

## define get time
def get_time(number):
    tmes = []
    for t in range(number):
        time = find_time(df)[t]
        dt = datetime.datetime.fromtimestamp(time)
        dt_string = dt.strftime("%Y-%m-%d %H:%M:%S")
        tmes.append(dt_string)
    return tmes


# In[112]:


## plotting with PLotly
import plotly.graph_objects as go
import plotly.offline as pyo
import textwrap
from ipywidgets import interact,fixed

pyo.init_notebook_mode()
m_size = 30

def plotly_vert(number,df):
    fig = go.Figure()
    fig.add_shape(type="rect", x0=3, x1=7,y0=3, y1=5, line=dict(color="RoyalBlue",width=2)) ## adds sending rect
    fig.add_trace(go.Scatter(x=[5], y=[4],
                             mode="markers", marker_size = m_size,
                             name = df['input_address'][0],
                             hovertemplate = 
                             '<b>Time of transaction</b>: %{text}',
                             text = [df['time_of_transaction'][0]]
                             )) ## adds circle
    for n in range(number):
        fig.add_shape(type="rect", x0=10, x1=14,y0=(n)*3+3, y1=(n)*3+5, line=dict(color="RoyalBlue",width=2))
        fig.add_annotation(x=10, y=(n)*3+4,xref="x",yref="y",
                           showarrow=True,
                           axref="x", ayref='y', 
                           ax=7, ay=4,
                           arrowhead=3, arrowwidth = 4)
        fig.add_annotation(x=9, y=(n)*3+4.5,xref="x",yref="y",
                            text = str(df['amount'][n]/(10**8)) + ' BTC',
                           showarrow=False,
                           axref="x", ayref='y', 
                           ax=7, ay=4,
                           arrowhead=3, arrowwidth = 4)
        fig.add_trace(go.Scatter(x=[12], y=[(n)*3+4],
                                 mode="markers",
                                 marker_size = m_size,
                                 name=df['transactions'][n],
                                 hovertemplate = 
                                 '<b>Time of transaction</b>: %{text}',
                                 text = [df['time_of_transaction'][n]]
                                ))
    fig.show()


# In[68]:


addr = '1qh4RVaUHC1qkYUotCnvPpJSZQByVW4S7'
numoftrans = 5

df = get_df(addr)
brn = get_branches(numoftrans)
inbrn = get_inbranches(numoftrans)
brnamt = get_branch_amt(numoftrans)
tmes = get_time(numoftrans)
data = {'input_address': inbrn,
        'transactions': brn,
        'amount': brnamt,
        'time_of_transaction':tmes
       }
dataframe = pd.DataFrame(data)


# In[69]:


dataframe


# In[113]:


interact(plotly_vert,number=(1,numoftrans,1),df=fixed(dataframe))


# In[18]:


find_transactions(df)


# In[59]:


find_transactions(df)[0]['time']
## cant figure out what time represents


# In[6]:


dataframe


# In[51]:


def find_inputaddr(df,address):
    inputs = find_transactions(df) 
    inadr = []
    for i in inputs:
        input = i['inputs'][0]['prev_out']['addr']
        inadr.append(input)
    return inadr

def get_inbranches(number):
    inbrn = []
    for i in range(number+1)[1:]:
        inbrnch = find_inputaddr(df,address=addr)[i]
        inbrn.append(inbrnch)
    return inbrn


# In[52]:


find_inputaddr(df,addr)


# In[53]:


get_inbranches(5)


# In[ ]:




