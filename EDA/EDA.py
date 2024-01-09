#!/usr/bin/env python
# coding: utf-8

# # Create EDA using Test Data file(Yoshops.com Sale Order file) :
# #### Input Value for genrate Graph chart:
# #### Enter 2 to see the analysis of different payment methods used by the Customers
# #### Enter 3 to see the analysis of Top Consumer States of India
# #### Enter 4 to see the analysis of Top Consumer Cities of India
# #### Enter 7 to see the analysis of Number of Orders Per Month Per Year
# #### Enter 8 to see the analysis of Reviews for Number of Orders Per Month Per Year
# #### Enter 9 to see the analysis of Number of Orders Across Parts of a Day
# #### Enter 10 to see the Full Report
# #### Enter the number to see the analysis of your choice: 1
# #### OutPut:Genrate analysis report in format PDF and Excel file.

# In[19]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib.backends.backend_pdf import PdfPages

def analyze_reviews(file_path, opt):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Extract numeric part from 'stars' column and convert to float
    df['stars'] = df['stars'].str.extract('(\d+)')
    df['stars'] = df['stars'].astype(float).fillna(np.nan)

    # Heatmap for null values
    sns.heatmap(df.isnull(), yticklabels=False)

    # Countplot with 'stars' vs 'category'
    sns.set(style='whitegrid')
    plt.figure(figsize=(10, 6))
    ax = sns.countplot(x='stars', hue='category', data=df, palette='Paired')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha='right')
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    plt.savefig('countplot.pdf')
    plt.close()

    # Filling the NaN values with rating mean of that particular category
    means_by_category_rounded = np.round(df.groupby('category')['stars'].mean(), 1)
    df['stars'].fillna(df['category'].map(means_by_category_rounded), inplace=True)

    # Boxplot for 'stars'
    plt.figure(figsize=(8, 6))
    sns.boxplot(df['stars'])
    plt.savefig('boxplot.pdf')
    plt.close()

    # Calculate the interquartile range (IQR)
    Q1 = df['stars'].quantile(0.25)
    Q3 = df['stars'].quantile(0.75)
    IQR = Q3 - Q1

    # Define the threshold for outliers using IQR
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Remove outliers from the DataFrame
    df_no_outliers = df[~((df['stars'] < lower_bound) | (df['stars'] > upper_bound))]
    plt.figure(figsize=(8, 6))
    sns.boxplot(df_no_outliers['stars'])
    plt.savefig('boxplot_no_outliers.pdf')
    plt.close()

    if opt==1:
        # Barplot for mean 'stars' per 'category'
        plt.figure(figsize=(12, 6))
        ax = sns.barplot(data=df, x='category', y='stars', estimator=np.mean)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='right')
        plt.savefig('barplot.pdf')
        plt.close()

        # Statistical summaries
        category_stats = df.groupby('category')['stars'].agg(['mean'])
        category_quantiles_25 = df.groupby('category')['stars'].quantile(0.25)
        category_quantiles_75 = df.groupby('category')['stars'].quantile(0.75)

        # Create DataFrame with mean, 25th, and 75th percentile for each category
        summary_df = pd.DataFrame({
            'Mean': category_stats['mean'],
            '25th Percentile': category_quantiles_25,
            '75th Percentile': category_quantiles_75
        })

        # Save statistical summaries to Excel
        with pd.ExcelWriter('statistical_summary.xlsx') as writer:
            summary_df.to_excel(writer, sheet_name='Summary')
    else:
        # Histogram to visualize distribution without outliers
        plt.figure(figsize=(8, 6))
        sns.histplot(df_no_outliers['stars'], kde=True)
        plt.title('Distribution of stars (No Outliers)')
        plt.xlabel('stars')
        plt.ylabel('Frequency')
        plt.savefig('histogram.pdf')
        plt.close()

        mean_reviews = df_no_outliers['stars'].mean()
        std_reviews = df_no_outliers['stars'].std()
        percentile_25 = df_no_outliers['stars'].quantile(0.25)
        percentile_75 = df_no_outliers['stars'].quantile(0.75)

        # Create a DataFrame for the statistical measures
        stats_df = pd.DataFrame({
            'Statistic': ['Mean', 'Standard Deviation', '25th Percentile', '75th Percentile'],
            'Value': [mean_reviews, std_reviews, percentile_25, percentile_75]
        })

        # Save the DataFrame to an Excel file
        stats_df.to_excel('reviews_statistics.xlsx', index=False)        

def analyze_top_categories(file_path):
    df = pd.read_csv(file_path)

    # Count occurrences of each category as sales
    category_sales = df['category'].value_counts().sort_values(ascending=False)

    # Determine the most selling category
    most_selling_category = category_sales.idxmax()

    # Plot sales for each category, highlighting the most selling category
    plt.figure(figsize=(10, 6))
    category_sales.plot(kind='bar', color=df['category'].apply(lambda x: 'skyblue' if x == most_selling_category else 'lightgrey'))
    plt.title('Total Sales by Product Category')
    plt.xlabel('Product Category')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('category_sales_highlighted.pdf')
    plt.close()
    
    category_sales_df = pd.DataFrame({'Product Category': category_sales.index, 'Total Sales': category_sales.values})
    category_sales_df.to_excel('category_sales_count.xlsx', index=False)

def analyze_top_states_cities(file_path, opt):
    df = pd.read_csv(file_path)

    # Filter data for India
    df_india = df[df['Shipping Country'] == 'IND']
    
    if opt==3:
        # Count occurrences of each state in India
        top_states = df_india['Shipping State'].value_counts().sort_values(ascending=False)

        # Create a DataFrame with state counts
        state_counts_df = pd.DataFrame({'State': top_states.index, 'Number of Consumers': top_states.values})

        # Save state counts information to an Excel file
        state_counts_df.to_excel('state_consumers_count.xlsx', index=False)

        # Plot the top consumer states in India
        plt.figure(figsize=(10, 6))
        top_states.plot(kind='bar', color='skyblue')
        plt.title('Top Consumer States in India')
        plt.xlabel('State')
        plt.ylabel('Number of Customers')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('top_consumer_states_india.pdf')
        plt.close()
        
    else:
        # Count occurrences of each city in India
        top_cities = df_india['Shipping City'].value_counts().sort_values(ascending=False)
        
        # Create a DataFrame with state counts
        city_counts_df = pd.DataFrame({'City': top_cities.index, 'Number of Consumers': top_cities.values})
        
        # Save city counts information to an Excel file
        city_counts_df.to_excel('city_consumers_count.xlsx', index=False)

        # Plot the top consumer cities in India
        plt.figure(figsize=(10, 6))
        top_cities.plot(kind='bar', color='skyblue')
        plt.title('Top Consumer Cities in India')
        plt.xlabel('City')
        plt.ylabel('Number of Customers')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('top_consumer_cities_india.pdf')
        plt.close()     

options = [
    "1. Analysis of Reviews given by Customers",
    "2. Analysis of different payment methods used by the Customers",
    "3. Analysis of Top Consumer States of India",
    "4. Analysis of Top Consumer Cities of India",
    "5. Analysis of Top Selling Product Categories",
    "6. Analysis of Reviews for All Product Categories",
    "7. Analysis of Number of Orders Per Month Per Year",
    "8. Analysis of Reviews for Number of Orders Per Month Per Year",
    "9. Analysis of Number of Orders Across Parts of a Day",
    "10. Full Report"
]

print("\n".join(options))
option=int(input("enter your option: "))
if option==1:
    file_path = r"C:\Users\nitin\Downloads\review_dataset.csv"
    analyze_reviews(file_path, 1)
elif option==3:
    file_path = r"C:\Users\nitin\Downloads\orders_2020_2021_DataSet_Updated.csv"
    analyze_top_states_cities(file_path, 3)
elif option==4:
    file_path = r"C:\Users\nitin\Downloads\orders_2020_2021_DataSet_Updated.csv"
    analyze_top_states_cities(file_path, 4)
elif option==5:
    file_path = r"C:\Users\nitin\Downloads\review_dataset.csv"
    analyze_top_categories(file_path)
elif option==6:
    file_path = r"C:\Users\nitin\Downloads\review_dataset.csv"
    analyze_reviews(file_path, 6)


# In[16]:


df = pd.read_csv(r"C:\Users\nitin\Downloads\orders_2020_2021_DataSet_Updated.csv")
# Assuming 'df' is your DataFrame
# Filter rows where 'Country' is 'India'
india_data = df[df['Shipping Country'] == 'India']

# Check for null values in the 'State' column for India
null_values_in_india = india_data['Shipping City'].isnull()

# Count the number of null values in the 'State' column for India
num_null_values_in_india = null_values_in_india.sum()

print(f"Number of null values in 'State' column for India: {num_null_values_in_india}")


# In[ ]:




