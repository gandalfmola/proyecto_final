import requests

class Position():
    def __init__(self, moment, coin_from,q, coin_to,r, value_u):
        self.moment = moment
        self.coin_from = coin_from
        self.q = q
        self.coin_to = coin_to
        self.r = r
        self.value_u = value_u
        
        

    def __str__(self):
        return f"Objeto Position {self.moment} {self.coin_from} {self.q} {self.coin_to} {self.r} {self.value_u}"

''' 
    def actual_value(self):
        apikey = "F36C75E1-23E6-4A6E-9049-9345741ED24E"
        url = f"https://rest.coinapi.io/v1/exchangerate/{self.coin}/EUR?apikey={apikey}"
        response = requests.get(url)
        value = response.json()
        print("value del método es", value)   
        print(response.status_code, response.text)    

        return value["rate"]*self.number
'''
    

    

    


