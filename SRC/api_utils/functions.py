import base64
import requests as rq
import json
from variables import *
import pandas as pd
from credentials import *

def get_oauth_token():
    api_key = API_KEY
    secret = SECRET

    message = api_key + ":" + secret

    auth = "Basic " + base64.b64encode(message.encode("ascii")).decode("ascii")

    headers_dic = {"Authorization" : auth,
                   "Content-Type" : "application/x-www-form-urlencoded;charset=UTF-8"}

    params_dic = {"grant_type" : "client_credentials",
                  "scope" : "read"}

    r = rq.post("https://api.idealista.com/oauth/token",
                      headers = headers_dic,
                      params = params_dic)

    token = json.loads(r.text)['access_token']

    return token


def define_search_url():
    url = ('https://api.idealista.com/3.5/'+country+
           '/search?operation='+operation+
           '&maxItems='+max_items+
           '&order='+order+
           '&center='+center+
           '&distance='+distance+
           '&propertyType='+property_type+
           '&sort='+sort+ 
           '&numPage=%s'+
           '&maxPrice='+maxprice+
           '&language='+language)
    
    return url


def search_api(url):  
    token = get_oauth_token()
    headers = {'Content-Type': 'Content-Type: multipart/form-data;', 'Authorization' : 'Bearer ' + token}
    content = rq.post(url, headers = headers)
    result = json.loads(content.text)

    return result


def results_to_df(results):
    df = pd.DataFrame.from_dict(results['elementList'])
    return df


def concat_df(df, df_tot):
    pd.concat([df_tot,df])
    return df_tot


def df_to_csv(df):
    df = df.reset_index()
    df.to_csv(file_path, index=False)