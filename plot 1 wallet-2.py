#!/usr/bin/env python
# coding: utf-8

# In[40]:


import pandas as pd
import ssl
import time
import textwrap
from matplotlib import pyplot as plt
from matplotlib.patches import FancyArrowPatch

def get_df(addr):
    ssl._create_default_https_context = ssl._create_unverified_context
    transactions_url = 'https://blockchain.info/rawaddr/' + addr
    df = pd.read_json(transactions_url)
    time.sleep(10)
    return df

def find_transactions(df): 
    transactions = df['txs']
    return transactions 

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

# Vertical plotting
def get_branches(number):
    brn = []
    for b in range(number):
        brnch = find_outputaddr(df)[b]
        brn.append(brnch)
    return brn

def get_branch_amt(number):
    brnamt = []
    for a in range(number):
        amount = find_amounts(df)[a]
        brnamt.append(amount)
    return brnamt

def plot_vert(number,df): # plot number of transactions
    sending_rectangle = plt.Rectangle((3, 3), width=4, height=2, facecolor="gainsboro", edgecolor="black")
    plt.annotate(textwrap.fill(addr,width=17), ((0)*7+5, 4), horizontalalignment='center', verticalalignment='center', fontsize=8)
    ax = plt.gca()  
    for n in range(number):
        rect = plt.Rectangle((10, (n)*3+3), width=4, height=2, facecolor="gainsboro", edgecolor="black")
        arrow = FancyArrowPatch((7, 4), (10, 3*(n)+4), edgecolor="lightgray", arrowstyle="simple",mutation_scale=10,connectionstyle="angle3")
        plt.annotate(str(df['Amount'][n]/(10**8)) + ' BTC', (7.1, 3.6+3*(n)), fontsize=8)
        plt.annotate(textwrap.fill(df['Transactions'][n],width=17), (12, 4+3*(n)), horizontalalignment='center', verticalalignment='center', fontsize=8)
        
        ax.add_patch(rect)
        ax.add_patch(arrow)      
    ax.add_patch(sending_rectangle)

    plt.axis("scaled")
    plt.axis("on")
    plt.show()


# In[41]:


## Test case 1: Bitcoin address with 2 output addresses and amounts
addr = '1qh4RVaUHC1qkYUotCnvPpJSZQByVW4S7'
numoftrans = 2

df = get_df(addr)
brn = get_branches(numoftrans)
brnamt = get_branch_amt(numoftrans)
data = {'Transactions': brn,
        'Amount': brnamt}
dataframe = pd.DataFrame(data)
plot_vert(numoftrans,dataframe)


# In[3]:


## Test case 2: Bitcoin address with varying output address (3)
addr = '1qh4RVaUHC1qkYUotCnvPpJSZQByVW4S7'
numoftrans = 3

df = get_df(addr)
brn = get_branches(numoftrans)
brnamt = get_branch_amt(numoftrans)
data = {'Transactions': brn,
        'Amount': brnamt}
dataframe = pd.DataFrame(data)
plot_vert(numoftrans,dataframe)


# In[4]:


## Test case 3: Different Bitcoin address with 3 outputs
addr = '18Vemn3r58s8Vnoow81bhFwfEmnmxX8rJ'
numoftrans = 3

df = get_df(addr)
brn = get_branches(numoftrans)
brnamt = get_branch_amt(numoftrans)
data = {'Transactions': brn,
        'Amount': brnamt}
dataframe = pd.DataFrame(data)
plot_vert(numoftrans,dataframe)


# In[5]:


## Test case 4:  Bitcoin address with varying output address (excessive)
addr = '18Vemn3r58s8Vnoow81bhFwfEmnmxX8rJ'
numoftrans = 10

df = get_df(addr)
brn = get_branches(numoftrans)
brnamt = get_branch_amt(numoftrans)
data = {'Transactions': brn,
        'Amount': brnamt}
dataframe = pd.DataFrame(data)
plot_vert(numoftrans,dataframe)


# In[6]:


## Test case 5:  Bitcoin address with varying output address (zero)
addr = '18Vemn3r58s8Vnoow81bhFwfEmnmxX8rJ'
numoftrans = 0

df = get_df(addr)
brn = get_branches(numoftrans)
brnamt = get_branch_amt(numoftrans)
data = {'Transactions': brn,
        'Amount': brnamt}
dataframe = pd.DataFrame(data)
plot_vert(numoftrans,dataframe)


# In[16]:


import matplotlib.pyplot as plt
import matplotlib.text as mpl_text

## create an object
class TextObject(object):
    def __init__(self, text, color):
        self.my_text = text
        self.my_color = color

## define the methods
class TextObjectHandler(object):
    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        width, height = handlebox.width, handlebox.height
        patch = mpl_text.Text(x=0, y=0, text=orig_handle.my_text)
        handlebox.add_artist(patch)
        return patch

obj_1 = TextObject("1", "black")
obj_2 = TextObject("2", "black")
obj_3 = TextObject("3", "black")
    
plt.legend([obj_1,obj_2,obj_3],[str(addr),str(dataframe['Transactions'][0]),str(dataframe['Transactions'][1])],
    bbox_to_anchor=(1.05,1),loc='upper left',
    handler_map={obj_1:TextObjectHandler(), obj_2:TextObjectHandler(),obj_3:TextObjectHandler()}
)
plt.show()


# In[18]:


## Testing our the legend option for address display - Text handlers

def plot_vert(number): # plot number of transactions
    sending_rectangle = plt.Rectangle((3, 3), width=4, height=2, facecolor="gainsboro", edgecolor="black")
    plt.text(5,4,1,horizontalalignment='center',verticalalignment='center',fontsize=8)
    ax = plt.gca()  
    for n in range(number):
        rect = plt.Rectangle((10, (n)*3+3), width=4, height=2, facecolor="gainsboro", edgecolor="black")
        arrow = FancyArrowPatch((7, 4), (10, 3*(n)+4), edgecolor="lightgray", arrowstyle="simple",mutation_scale=10,connectionstyle="angle3")
        plt.annotate(str(dataframe['Amount'][n]/(10**8)) + ' BTC', (7.1, 3.6+3*(n)), fontsize=8)
        plt.text(12,4+3*(n),(n+2),horizontalalignment='center',verticalalignment='center',fontsize=8)
        
        ax.add_patch(rect)
        ax.add_patch(arrow)      
    ax.add_patch(sending_rectangle)
    plt.axis("scaled")
    plt.axis("off")
    plt.show()


# In[19]:


addr = '1qh4RVaUHC1qkYUotCnvPpJSZQByVW4S7'
numoftrans = 2

df = get_df(addr)
brn = get_branches(numoftrans)
brnamt = get_branch_amt(numoftrans)
data = {'Transactions': brn,
        'Amount': brnamt}
dataframe = pd.DataFrame(data)

plot_vert(numoftrans,dataframe)
obj_1 = TextObject("1", "black")
obj_2 = TextObject("2", "black")
obj_3 = TextObject("3", "black")
    
plt.legend([obj_1,obj_2,obj_3],[str(addr),str(dataframe['Transactions'][0]),str(dataframe['Transactions'][1])],
    bbox_to_anchor=(1.05,1),loc='upper left',
    handler_map={obj_1:TextObjectHandler(), obj_2:TextObjectHandler(),obj_3:TextObjectHandler()}
)


# In[5]:


## Testing shapes and colours as legend handlers
def plot_vert(number): # plot number of transactions
    sending_rectangle = plt.Rectangle((3, 3), width=4, height=2, facecolor="gainsboro", edgecolor="black",label=addr)
    plt.text(5,4,1,horizontalalignment='center',verticalalignment='center',fontsize=8)
    ax = plt.gca()  
    for n in range(number):
        ## change rectangles to circles
        circle = plt.Circle((12, (n)*3+4), radius = 1, facecolor="gainsboro", edgecolor="black",label=dataframe['Transactions'][n])
        arrow = FancyArrowPatch((7, 4), (11, 3*(n)+4), edgecolor="lightgray", arrowstyle="simple",mutation_scale=10,connectionstyle="angle3")
        plt.annotate(str(dataframe['Amount'][n]/(10**8)) + ' BTC', (7.1, 3.6+3*(n)), fontsize=8)
        plt.text(12,4+3*(n),(n+2),horizontalalignment='center',verticalalignment='center',fontsize=8)
        
        ax.add_patch(circle)
        ax.add_patch(arrow)
    ax.add_patch(sending_rectangle)
    plt.legend(bbox_to_anchor=(1.05,1),loc='upper left')
    plt.axis("scaled")
    plt.axis("off")
    plt.show()


# In[21]:


addr = '1qh4RVaUHC1qkYUotCnvPpJSZQByVW4S7'
numoftrans = 2

df = get_df(addr)
brn = get_branches(numoftrans)
brnamt = get_branch_amt(numoftrans)
data = {'Transactions': brn,
        'Amount': brnamt}
dataframe = pd.DataFrame(data)


# In[22]:


plot_vert(numoftrans,dataframe)
## ??


# In[65]:


from matplotlib.widgets import Slider

axslider = plt.axes([0.25, 0.1, 0.65, 0.03])
slider = Slider(
    ax = axslider,
    label="Value",
    valmin = 1,
    valmax = 3,
    valinit = 1, ## default value
    valstep = 1
)


# In[32]:


## Testing slider widget
addr = '1qh4RVaUHC1qkYUotCnvPpJSZQByVW4S7'
numoftrans = 5

df = get_df(addr)
brn = get_branches(numoftrans)
brnamt = get_branch_amt(numoftrans)
data = {'Transactions': brn,
        'Amount': brnamt}
dataframe = pd.DataFrame(data)


# In[39]:


from ipywidgets import interact,fixed

interact(plot_vert,number=(1,numoftrans,1),df=fixed(dataframe))


# In[ ]:




