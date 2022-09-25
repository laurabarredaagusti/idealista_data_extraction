import requests
from bs4 import BeautifulSoup as bs
from time import sleep
from variables import *
from credentials import *


def province_url(provinces_list):
    '''
    This function will get the given provinces list and return the specific url for every province
    '''
    all_provinces_urls = []   # Create an empty list which will contain all the urls

    root_url = 'https://www.idealista.com/alquiler-viviendas/'   # root url for all the provinces

    for index, provincia in enumerate(provinces_list):   # loop on all the provinces in the provinces list
        url_provincia = root_url + provincia + '/'   # create the province url by concatenating strings
        all_provinces_urls.append(url_provincia)   # add the resulting url to the previously created list

    return all_provinces_urls