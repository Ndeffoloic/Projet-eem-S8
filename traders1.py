import random

import matplotlib.pyplot as plt
import numpy as np

a_Buyer = 147 # A € [133,200]
v_Seller = 14  # V € [0,67]
default_rounds = 20 

class Trader:
    def __init__(self, id, trader_type, num_rounds = default_rounds):
        self.id = id
        self.trader_type = trader_type
        # chaque vendeur dispose d'une unité de bien et chaque acheteur dispose de 0 unité
        self.init_qty = np.full(num_rounds, 1) if trader_type == "seller" else None
        self.redemption_value = (a_Buyer - 7*self.id) if trader_type == "buyer" else None
        self.cost = (v_Seller + 7*self.id) if trader_type == "seller" else None
        self.sold_quantities = np.full(num_rounds, 0)  if  trader_type == "seller" else None
        self.bought_quantities = np.full(num_rounds, 0) if trader_type == "buyer" else None
        self.ask = 0 if  trader_type == "seller" else None
        self.bid = 0 if trader_type == "buyer" else None
        
    def has_traded(self, round):    
        """Determine si un trader a tradé au tour courant

        Args:
            round (int): indice du tour courant

        Returns:
            bool: True si le trader a tradé au tour courant, False sinon
        """
        if self.trader_type == "buyer":
            return np.any(self.bought_quantities ==1)
        elif self.trader_type == "seller":
            return np.any(self.sold_quantities ==1)
        

def create_traders():
    """Créé les traders qui vont participé à la imulation de marché 
    Il doit y avoir autant de traders que de rounds. 
    

    Returns:
        Table: contient deux types de traders, le vendeurs et les acheteurs 
    """
    buyers = [Trader(i,"buyer") for i in range(default_rounds)]
    sellers = [Trader(i,"seller") for i in range(default_rounds)]
    return buyers + sellers

def determine_price(ask,bid,type_price_determined) :
    """Cette fonction détermine le 
    Args:
        ask (double): prix généré par le vendeur pour le tour
        bid (double): prix généré par l'acheteur pour le tour
        type_price_determined (double): valeur qui permet d'indiquer la manière avec laquelle le 
        prix de l'échange sera fixé

    Returns:
        double: prix que va proposé un trader en fonction 
    du type d'échanges que l'onsouhaite simuler
    """
    if type_price_determined == 1 :
        return random.uniform(ask,bid)
    elif type_price_determined == 2 :
        return int(random.uniform(ask,bid))
    elif type_price_determined == 3 :
        return (ask + bid)/2
    
def run_simulation(type_double_auction, type_price_determined, ZI_C = False):
    traders = create_traders()
    random.shuffle(traders)
    
    demand = [] # à chaque tuple [quantité,itération] on associera un prix. 
    supply = [] # à chaque tuple [quantité,itération] on associera un prix. 
    prices = [] # représente les différents prix auquels ont été vendus les produits à chaque round

    for i in range(default_rounds):  # Run for default_rounds rounds
        buyers = [t for t in traders if t.trader_type ==  "buyer" and not t.has_traded(i)]
        sellers = [t for t in traders if t.trader_type ==  "seller" and not t.has_traded(i)]
        if ZI_C :
            for t in sellers:
                t.ask = random.uniform(t.cost, 200)
            for t in buyers:
                t.bid = random.uniform(0, t.redemption_value)
        else :
            for t in sellers:
                t.ask = random.uniform(0, 200)
            for t in buyers:
                t.bid = random.uniform(0, 200)
            
        asks = sorted([t.ask for t in sellers])
        bids = sorted([t.bid for t in buyers], reverse=True)
       
        if not buyers or not sellers:
            break  # No more trades can be made
        if type_double_auction == 1 : 

            # Find the maximum number of possible trades
            m = 0
            while m < len(asks) and m < len(bids) and asks[m] <= bids[m]:
                m += 1

            if m == 0:
                print("No trade occurred")
            else:
                # Trades occur, choose price as the average of the highest ask and lowest bid among the m trades
                price = determine_price(max(asks[:m]), min(bids[:m]), type_price_determined)
                print(f"{m} trades occurred at price = {price}")
                
                # Update quantities and calculate individual gains
                for buyer in buyers[:m]:
                    buyer.bought_quantities[i] = 1
                for seller in sellers[:m]:
                    seller.sold_quantities[i] = 1
                
                # Record demand and supply
                demand.append(min(bids[:m]))
                supply.append(max(asks[:m]))
                # Record prices
                prices.append(price)

        if type_double_auction == 2 :
            buyer = max(buyers, key=lambda t: t.bid) # semande la plus grande 
            seller = min(sellers, key=lambda t: t.ask) #offre la plus petite.
            
            if buyer.bid < seller.ask:
                print("No trade occurred")
            else:
                # Trade occurs, choose price randomly between buyer value and seller value
                
                price = determine_price(seller.ask, buyer.bid, type_price_determined)
                print(f"Trade occurred: buyer value = {buyer.bid}, seller value = {seller.ask}, price = {price}")
                buyer.bought_quantities[i] = 1
                seller.sold_quantities[i] = 1
                # Record demand and supply
                demand.append(buyer.bid)
                supply.append(seller.ask)
                prices.append(price)
    # Plot demand and supply
    plt.figure(figsize=(10, 5))
    plt.plot(range(len(demand)), sorted(demand, reverse=True), drawstyle='steps', label='Demand')
    plt.plot(range(len(supply)), sorted(supply), drawstyle='steps', label='Supply')
    plt.xlabel('Quantity')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

    # Plot prices
    plt.figure(figsize=(10, 5))
    plt.plot(range(len(prices)), prices, label='Prices', marker='o')
    plt.xlabel('Quantity')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

run_simulation(1,1,1)
