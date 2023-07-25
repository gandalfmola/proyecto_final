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


    

    

    


