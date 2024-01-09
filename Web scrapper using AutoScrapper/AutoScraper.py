#!/usr/bin/env python
# coding: utf-8

# In[3]:


from autoscraper import AutoScraper
import pandas as pd
import requests
from lxml import html


# In[41]:


import pandas as pd
from autoscraper import AutoScraper

head = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}

PAGES = 13

def scrape_product_info_1(url):
    train_url = "https://yoshops.com/products"  
    wanted_list = [
        "Reliance Jio Phone",
        "https://isteam.wsimg.com/ip/a8efe83b-6857-477d-9d0f-f13ca0229a20/ols/1354_original/:/rs=w:600,h:600", 
        "₹1,499.00",
    ]

    scraper = AutoScraper()
    scraper.build(train_url, wanted_list)
    scraper.get_result(train_url, grouped=True)

    return scraper.get_result_similar(url, grouped=True)

def scrape_product_info_2(url):
    train_url = "https://yoshops.com/t/toys"  
    wanted_list = [
        "Sony PlayStation PS2 Gaming Console 150 GB Hard Disk With 50 Games Preloaded(Black)",
        "https://isteam.wsimg.com/ip/a8efe83b-6857-477d-9d0f-f13ca0229a20/ols/3083_original/:/rs=w:600,h:600",
        "₹8,999.00",
    ]
    scraper = AutoScraper()
    scraper.build(train_url, wanted_list)
    scraper.get_result(train_url, grouped=True)

    return scraper.get_result_similar(url, grouped=True)

def create_excel_file(product_info, opt):
    df = pd.DataFrame(product_info)

    df['Status'] = True

    if 'image' in df.columns:
        df.loc[df['image'].isnull(), 'Status'] = False
        
    if opt==1 or opt==3:
        columns_to_drop = [1, 2, 5, 6]
        df = df.drop(df.columns[columns_to_drop], axis=1)
    else:
        columns_to_drop = [1, 2]
        df = df.drop(df.columns[columns_to_drop], axis=1)
        
    columns_to_rename = {0: 'Product Title', 1: 'Product Image', 2: 'Product Price', 3: 'Status'}
    df.columns = [columns_to_rename[col] if col in columns_to_rename else col for col in range(len(df.columns))]
        
    df.to_excel('product_details.xlsx', index=False)
    print("Excel file created successfully with product details.")

def scrape_and_create_excel(url, opt):
    if opt == 1 or opt == 3:
        product_info = scrape_product_info_1(url)
    else:
        product_info = scrape_product_info_2(url)
    create_excel_file(product_info, opt)

print("Enter 1 for Input value = Yoshops.com")
print("Enter 2 for Input value = Any main categories")
print("Enter 3 for Input value = Any sub-main categories")

user_input = input("Enter your choice: ")

if user_input == '1':
    website_url = "https://yoshops.com/products"  
    scrape_and_create_excel(website_url, 1)
elif user_input == '2':
    try:
        custom_url = input("Enter the custom url: ")
        scrape_and_create_excel(custom_url, 2)
    except Exception as e:
        print(f"An error occurred: {e}")
elif user_input == '3':
    try:
        custom_url = input("Enter the custom url: ")
        scrape_and_create_excel(custom_url, 3)
    except Exception as e:
        print(f"An error occurred: {e}")


# In[4]:


def scrape_product_info_1(url):
    train_url = "https://yoshops.com/products"  
    wanted_list = [
        "Reliance Jio Phone",
        "4.8 star rating",
    ]

    scraper = AutoScraper()
    scraper.build(train_url, wanted_list)
    scraper.get_result(train_url, grouped=True)

    return scraper.get_result_similar(url, grouped=True)
 
scrape_product_info_1("https://yoshops.com/products")


# In[ ]:




