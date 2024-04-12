import random


class ZITrader : 
    def __init__(self,id,ZI_type,type,ZI_limit = 0) -> None:
        self.ZI_type = ZI_type
        self.type = type
        self.ZI_limit = 0 if self.ZI_type == 'ZI-U' else ZI_limit
        self.id = id
        self.redemption_value = None
        self.cost = None
        self.offer = None
        self.demand = None
        
    def generate_offer_demand(self):
        if self.ZI_type == 'ZI-U' :
            self.redemption_value = random.randint(1,200) if self.type == 'buyer' else None
            self.cost = random.randint(1,200) if self.type == 'seller' else None
            self.offer = random.randint(1, 200) if self.type == 'seller' else None
            self.demand = random.randint(1, 200) if self.type == 'buyer' else None
        elif self.ZI_type == 'ZI-C' :
            self.redemption_value = random.randint(1,200) if self.type == 'buyer' else None
            self.cost = random.randint(1,200) if self.type == 'seller' else None
            self.offer = random.randint(1, self.redemption_value) if self.type == 'seller' else None
            self.demand = random.randint(self.cost, 200) if self.type == 'buyer' else None
    def accept_offer_demand(self, price):
        if self.ZI_type == 'ZI-U' : 
            
        elif self.ZI_type == 'ZI-C' : 
            
    