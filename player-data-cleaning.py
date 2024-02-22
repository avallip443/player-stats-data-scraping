from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

# file generated from web-scraping.py
df = pd.read_csv('stat.csv', skiprows=1)

# modifies Age to only years
df['Age'] = df['Age'].str.split('-').str[0]

# modifies Player Names to UFT-8
df['Player'] = df['Player'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

# specifies which columns to include 
df = df.drop('90s', axis=1)
selected_columns = df.iloc[:, list(range(15)) + [df.shape[1] - 2]]

selected_columns.to_csv('player_data.csv', index=False)
