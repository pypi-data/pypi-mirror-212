# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 20:03:41 2023

@author: rodbl
"""

import requests
import pandas as pd
from urllib.parse import urljoin

API_URL = "https://latinex-blasser-analytica.herokuapp.com/"



class Utilities:
    
    def whois():
        url = API_URL
        response = requests.get(url)
        return response.text
    
    def welcome():
        url = urljoin(API_URL,"latinex_developer/welcome")
        response = requests.get(url)
        res = response.json()['respuesta']
        
        return res
    
    def register(email_address):
        
        url = urljoin(API_URL,"/latinex_developer/key")
        querystring = {"email_address":email_address}
        response = requests.post(url, params=querystring)
            
        return response.json()['response']
        
        
    def get_historic(key, fecha_inicio, fecha_fin, tipo_emision):
        
    
        querystring = {"fecha_inicio":fecha_inicio,
                       "fecha_fin":fecha_fin,
                       "tipo_emision":tipo_emision}

        headers = {"key": key}

        url = urljoin(API_URL,"/latinex_developer/historicos")
        response = requests.post(url, headers=headers, params=querystring)
        
        if response.status_code == 200:
            
            if response.json()['data_dict'] == "Invalid Key":
                
                r =  "Invalid API Key"
            
            else:
                
                d0 = pd.DataFrame(response.json()['data_dict'])
                d0['proc_date'] = pd.to_datetime(d0['proc_date']).dt.date
                
                r = d0
        
        
        return r
        
        
        
        