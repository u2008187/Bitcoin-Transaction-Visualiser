#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import ssl
from matplotlib import pyplot as plt
import time
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

def plot_vert(number): # plot number of transactions
    sending_rectangle = plt.Rectangle((3, 3), width=4, height=2, facecolor="gainsboro", edgecolor="black")
    plt.annotate(addr, ((0)*7+5, 4), horizontalalignment='center', verticalalignment='center', fontsize=3)
    ax = plt.gca()  
    for n in range(number):
        rect = plt.Rectangle((10, (n)*3+3), width=4, height=2, facecolor="gainsboro", edgecolor="black")
        transaction_line = plt.arrow(7, 4, 3, 3*(n), edgecolor="lightgray", linewidth=3)
        plt.annotate(str(dataframe['Amount'][n]/(10**8)) + ' BTC', (7.1, 3.6+3*(n)), fontsize=6)
        plt.annotate(dataframe['Transactions'][n], (12, 4+3*(n)), horizontalalignment='center', verticalalignment='center', fontsize=3)
        
        ax.add_patch(rect)
        ax.add_patch(transaction_line)      
        
    ax.add_patch(sending_rectangle)
       
def plot_trans(number):
    get_branches(number)
    get_branch_amt(number)
    plot_vert(number)
    annotate_vert(number)
    show_plot()
    
def show_plot():
    plt.axis("scaled")
    plt.axis("off")
    plt.show()
    


# In[13]:


# Test case 1: Bitcoin address with 2 output addresses and amounts
addr = '1qh4RVaUHC1qkYUotCnvPpJSZQByVW4S7'
df = get_df(addr)
brn = get_branches(4)
brnamt = get_branch_amt(4)
data = {'Transactions': brn,
        'Amount': brnamt}
dataframe = pd.DataFrame(data)
plot_vert(2)
show_plot()


# In[14]:


# Test case 2: Bitcoin address with varying output address (3)
addr = '1qh4RVaUHC1qkYUotCnvPpJSZQByVW4S7'
df = get_df(addr)
brn = get_branches(4)
brnamt = get_branch_amt(4)
data = {'Transactions': brn,
        'Amount': brnamt}
dataframe = pd.DataFrame(data)
plot_vert(3)
show_plot()


# In[18]:


# Test case 3: Different Bitcoin address with 3 outputs
addr = '18Vemn3r58s8Vnoow81bhFwfEmnmxX8rJ'
df = get_df(addr)
brn = get_branches(3)
brnamt = get_branch_amt(3)
data = {'Transactions': brn,
        'Amount': brnamt}
dataframe = pd.DataFrame(data)
plot_vert(3)
show_plot()


# In[ ]:




