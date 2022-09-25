from credentials import *
from bs4 import BeautifulSoup as bs
from variables import *
import requests
from time import sleep
import pandas as pd


class Extract():
    '''
    This class will extract all the necessary data from Idealista using scraping
    '''
    def __init__(self, all_provinces_url):
        self.all_provinces_url = all_provinces_url
        self.container_lists()
        self.extract_all_data()
        self.create_dict()
        self.df_from_dict()
        self.save_csv()
        

    def container_lists(self):
        '''
        This function will create all the empty list which will contain the column values for the dataframe
        '''
        self.total_de_inmuebles = []   # total number of listings in the province
        self.title_list = []   # list of all listing titles
        self.price_list = []   # list of all listing prices
        self.province_list = []   # list of all provinces
        self.meters_list = []   # list of all square meters
        self.rooms_list = []   # list of all the room numbers
        self.comunidades_autonomas = []   # list of all the 'comunidad autonoma'
        self.listing_number = []


    def get_listing_number(self):
        '''
        This function will get the number of listins/province
        '''
        self.numero_de_inmuebles = self.soup.find('span', class_='breadcrumb-navigation-element-info').text
        self.numero_de_inmuebles = self.numero_de_inmuebles.replace('.','')
        return self.numero_de_inmuebles


    def append_extra_data(self):
        '''
        This function will add the province name and the number of listings/province to the empty lists
        '''
        self.province_list.append(lista_nombres_provincias[self.index_provincia])   # Name of province
        self.total_de_inmuebles.append(self.numero_de_inmuebles)   # Total number of listings
        self.listing_number.append(self.listing_number)   # Number of listings/province

    
    def append_comunidad_autonoma(self):
        '''
        This function will add the name of the comunidad autonoma to the empty list
        '''
        for key, value in diccionario_comunidades.items():   # This loop iterates over the dictionary of 
            for individual_value in value:                   # comunidades autonomas
                if individual_value == lista_nombres_provincias[self.index_provincia]:   # Add the desired province
                    self.comunidades_autonomas.append(key)                               # to the empty list


    def extract_titles(self):
        '''
        This function will extract all the titles in the page and add them to the empty list of titles
        '''
        try:
            all_titles = self.soup.find_all("a", class_="item-link")   # Find all the titles in the page
            for title in all_titles:   # This loop will iterate over all the titles
                title = title.text
                self.title_list.append(title)   # Add each of them to the empty list
                self.append_extra_data()   # Append to the list extra content
                self.append_comunidad_autonoma()
                self.count_title += 1   # Add 1 to the title count, in order to keep track of the added titles
        except:
            self.title_list.append(None)   # In case there's no title, fill the list with a None and
            self.append_extra_data()       # still add the extra content
            self.append_comunidad_autonoma()

    
    def extract_prices(self):
        '''
        This function will extract all the prices from the page and add them to the empty prices list
        '''
        try:
            all_prices = self.soup.find_all("span", class_="item-price h2-simulated")   # Extract all the prices
            for price in all_prices:   # Iterate over all the prices
                price = price.text
                self.price_list.append(price[:-5].replace('.',''))   # Append the prices to the list
        except:
            self.price_list.append(None)   # If there is no price, fill the list with a None

    
    def extract_all_details(self):
        '''
        This function will extract all the details from the page and add them to the empty list
        '''
        try:
            all_details = self.soup.find_all('div', class_='item-detail-char')   # Find all the details
            for detail_chart in all_details:   # Iterate over them and get the inner details
                detail_list_chart = detail_chart.find_all('span', class_='item-detail')
                for index, detail in enumerate(detail_list_chart):   # Iterate over the inner details
                    detail = detail.text
                    if index == 0:   # If index is 0, the detail is meters 
                        try:
                            self.meters_list.append(detail[:-5])   # Append the meters to the list
                        except:
                            self.meters_list.append(None)   # If there are no meters, fill the list with None
                    elif index == 1:   #  If index is 1, the detail is rooms
                        try:
                            self.rooms_list.append(detail[:-3])   # Append the rooms to the list
                        except:
                            self.rooms_list.append(None)   # If there are no rooms, fill the list with None
                if len(self.rooms_list) < len(self.meters_list):   # In case it doesn't show the rooms, fill
                    self.rooms_list.append(None)                   # the list with None
        except:
            self.meters_list.append(None)   # If the previous action receives and error, fill the lists with None
            self.rooms_list.append(None)


    def get_soup(self, url):
        '''
        This function will create a soup from a given url
        '''
        response = requests.get(url, headers= headers)
        html_content = response.content
        self.soup = bs(html_content, "lxml")
        return self.soup


    def extract_all_data(self):
        '''
        This function will iterate over all the provinces url, and add all the content to the empty lists
        '''
        for self.index_provincia, self.provincia in enumerate(self.all_provinces_url):
            count = 1
            self.count_title = 1
            self.url = self.provincia
            self.soup = self.get_soup(self.url)
            self.numero_de_inmuebles = self.get_listing_number()

            while (int(self.numero_de_inmuebles) > self.count_title):
                self.extract_titles()
                self.extract_prices()
                self.extract_all_details()

                count += 1
                sleep(1)
                self.url_pag = self.provincia + 'pagina-' + str(count) + '.htm'
                self.soup = self.get_soup(self.url_pag)

    
    def create_dict(self):
        '''
        This function will create a dictionary with the keys as the desired dataframe columns, and the
        values as the extracted data
        '''
        diccionario_keys = ['number_of_listings', 'provincia','comunidad autonoma', 'titulo', 'precio', 'habitaciones', 'metros', 'total inmuebles/comunidad']
        diccionario_values = [self.numero_de_inmuebles, self.province_list, self.comunidades_autonomas, self.title_list, self.price_list, self.meters_list, self.rooms_list, self.total_de_inmuebles]
        self.diccionario_datos = dict(zip(diccionario_keys, diccionario_values))

    def df_from_dict(self):
        '''
        This funtion will create a dataframe from the given dictionary
        '''
        self.df = pd.DataFrame.from_dict(self.diccionario_datos)


    def save_csv(self):
        '''
        This function will save the dataframe as a csv file
        '''
        self.df.to_csv('rent_spain_scraping_dataset.csv')
