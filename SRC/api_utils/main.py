from functions import *
from variables import *

url = define_search_url()
first_search_url = url %(1)
results = search_api(url)
total_pages = results['totalPages']
df = results_to_df(results)
df_tot = concat_df(df, df_tot)

for i in range(2, total_pages):
    url = url %(i)
    results = search_api(url)
    df = results_to_df(results)
    df_tot = concat_df(df, df_tot)

df_to_csv(df_tot)