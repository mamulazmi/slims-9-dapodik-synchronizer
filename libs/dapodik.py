import requests
import json
from models.persertaDidik import PesertaDidik
from models.gtk import Gtk

class Dapodik:
    
    def __init__(self, host, npsn, apiKey):
        self.host = host
        self.npsn = npsn
        self.apiKey = apiKey
        
        self.headers = {
            'authorization': 'Bearer ' + apiKey
        }
        
        self.params = {
            'npsn': npsn
        }
        
    def getPesertaDidik(self):
        response = requests.get(self.host + '/WebService/getPesertaDidik', 
                                headers=self.headers,
                                params=self.params)
        return PesertaDidik.schema().loads(
            json.dumps(response.json()['rows']), many=True)
    
    def getGtk(self):
        response = requests.get(self.host + '/WebService/getGtk', 
                                headers=self.headers,
                                params=self.params)
        return Gtk.schema().loads(
            json.dumps(response.json()['rows']), many=True)