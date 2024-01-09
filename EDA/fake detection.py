#!/usr/bin/env python
# coding: utf-8

# # Task-:Fake buyer Identification System:
# EDA Report Generate below input value(1 to 5)using Test Data file(Yoshops.com Sale Order file) :
# ### Input value for generate PDF and CSV file:
# ##### 1.The shipping address differs from the billing address.
# ##### 2.Multiple orders of the same item.
# ##### 3.Unusually large orders.
# ##### 4.Multiple orders to the same address with different payment method.
# ##### 5.Unexpected international orders.

# In[27]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib.backends.backend_pdf import PdfPages

# def diff_address(file_path):
    
def multiple_orders(file_path):
    # Group by 'Item' and 'Address', then count occurrences
    item_address_counts = df.groupby(['LineItem Name', 'Shipping Street Address']).size().reset_index(name='OrderCount')

    # Filter rows where order count is greater than 1
    multiple_orders_same_item_address = item_address_counts[item_address_counts['OrderCount'] > 1]

    # Get the rows corresponding to multiple orders of the same item to the same address
    orders_multiple_same_item_address = df.merge(multiple_orders_same_item_address, on=['LineItem Name', 'Shipping Street Address'], how='inner')

    # Display or further analyze orders with multiple orders of the same item to the same address
    selected_columns = ['Order #', 'Shipping Street Address', 'LineItem Name']  # Add the columns you want to display
    result = orders_multiple_same_item_address[selected_columns]
    return result

    
def large_orders(file_path):
    df = pd.read_csv(file_path)
    # Filter rows where the quantity is greater than or equal to 3
    large_order = df[df['LineItem Qty'] >= 10][['Order #', 'LineItem Name', 'Shipping Street Address Qty']]
    return large_order

# def diff_payment(file_path):
    
def intl_orders(file_path):
    df = pd.read_csv(file_path)
    intl_orders = df[df['Shipping Country'] != 'IND'][['Order #', 'LineItem Name', 'LineItem Qty','Shipping Country']]
    return intl_orders

option=int(input())
if option==2:
    print(multiple_orders(r"C:\Users\nitin\Downloads\orders_2020_2021_DataSet_Updated.csv"))
elif option==3:
    print(large_orders(r"C:\Users\nitin\Downloads\orders_2020_2021_DataSet_Updated.csv"))
    
elif option==5:
    print(intl_orders(r"C:\Users\nitin\Downloads\orders_2020_2021_DataSet_Updated.csv"))


# In[ ]:




