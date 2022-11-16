#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 05:04:01 2022

@author: fernando
"""


import requests
from getpass import getpass
from requests.exceptions import HTTPError
#import ipywidgets as widgets
import markdown 
from ipywidgets import HTMLMath

#import json
#import csv
#from json2html import json2html


class PM:
    
    base_url = None
    header = None
    email = None
    pwd = None
    
    def __init__(self, email,pwd=None,local = False):
        if local:
            self.base_url = "http://127.0.0.1:8000/"
        else:
            self.base_url = "https://api.matecbi.net/"
        if pwd:
            self.pwd = pwd
        self.email = email
        
    
    def conecta(self, local=False):
        
        try:
            resp = requests.post(self.base_url+'login', 
                             data=[('email',self.email), ('password',self.pwd)])
    
            resp.raise_for_status()
        except HTTPError as http_err:
            print(f'Ha ocurrido un error de HTTP: {http_err}')  
            
        except Exception as err:
            print(f'Ha ocurrido algún error: {err}')  
        else:
            self.header = {"Authorization": "Bearer "+resp.json()}
            print('¡Conexión establecida!')
        
    def html_nota(self, nt):
        html = markdown.markdown("####"+nt['titulo']+'\n'+nt["contenido"])
        return HTMLMath(html)
    
        
    def get_nota(self, bloque_nota_id): #espera el id del enlance nota-bloque!!!
        data = {"id": bloque_nota_id}
        
        try:
            nota = requests.get(self.base_url+"contenido/nota", params=data, headers=self.header)
            # If the response was successful, no Exception will be raised
            nota.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
            return None
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
            return None
        else:
            nt = nota.json() 
            html = self.html_nota(nt)
            return {'nota': nt}
    