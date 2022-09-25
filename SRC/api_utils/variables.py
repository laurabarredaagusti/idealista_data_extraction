import pandas as pd

country = 'es' 
locale = 'es' 
language = 'es' #
max_items = '50'
operation = 'rent' 
property_type = 'homes'
order = 'priceDown' 
center = '40.4167,-3.70325' 
distance = '60000'
sort = 'desc'
bankOffer = 'false'
maxprice = '750'

file_path = '../data/idealista_test.csv'

df_tot = pd.DataFrame()