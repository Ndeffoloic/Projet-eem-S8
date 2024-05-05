import random

import matplotlib.pyplot as plt

a_Buyer = 147 # A € [133,200]
v_Seller = 14  # V € [0,67]

a_Buyer = 147 # A € [133,200]
v_Seller = 14  # V € [0,67]

class Trader:
    def __init__(self, id, trader_type, ZI_C=False):
        self.id = id
        self.trader_type = trader_type
        self.init_qty = 1 if trader_type == "seller" else None
        self.redemption_value = (a_Buyer - 7*self.id) if trader_type == "buyer" else None
        self.cost = (v_Seller + 7*self.id) if trader_type == "seller" else None
        self.sold_quantities = 0  if  trader_type == "seller" else None
        self.bought_quantities = 0 if trader_type == "buyer" else None
        self.has_traded = self.bought_quantities ==1 if trader_type == "buyer" else self.sold_quantities ==1
        self.ZI_C = ZI_C

    def generate_bid(self):
        if self.ZI_C:
            return random.uniform(0, self.redemption_value)
        else:
            return random.uniform(0, 200)

    def generate_ask(self):
        if self.ZI_C:
            return random.uniform(self.cost, 200)
        else:
            return random.uniform(0, 200)

def create_traders():
    buyers = [Trader(i,"buyer") for i in range(20)]
    sellers = [Trader(i,"seller") for i in range(20)]
    return buyers + sellers

def determine_price(cost,redemtion_value,type_price_determined) :
    if type_price_determined == 1 :
        return random.uniform(cost,redemtion_value)
    elif type_price_determined == 2 :
        return random.randint(cost,redemtion_value)
    elif type_price_determined == 3 :
        return (cost + redemtion_value)/2

def run_simulation(type_double_auction, type_price_determined, ZI_C = False):
    traders = create_traders()
    random.shuffle(traders)
    
    demand = {} if type_double_auction == 1 else [] # à chaque tuple [quantité,itération] on associera un prix. 
    supply = {} if type_double_auction == 1 else [] # à chaque tuple [quantité,itération] on associera un prix. 
    prices = [] # représente les différents prix auquels ont été vendus les produits à chaque round

    for i in range(20):  
        # Run for 20 rounds
        buyers = [t for t in traders if t.trader_type ==  "buyer" and not t.has_traded]
        sellers = [t for t in traders if t.trader_type ==  "seller" and not t.has_traded]
        nmr_qty = 0 # nombre d'échanges au cours de ce round
        if not buyers or not sellers:
            break  # No more trades can be made
        if type_double_auction == 1 : 
            # Generate and sort asks and bids
            asks = sorted([t.generate_ask() for t in sellers])
            bids = sorted([t.generate_bid() for t in buyers], reverse=True)


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
                    buyer.bought_quantities = 1
                for seller in sellers[:m]:
                    seller.sold_quantities = 1
                
                # Record demand and supply
                demand[(m, i)] = price
                supply[(m, i)] = price
                
                # Record prices
                prices.append(price)

        if type_double_auction == 2 :
            buyer = max(buyers, key=lambda t: t.redemption_value) # semande la plus grande 
            seller = max(sellers, key=lambda t: t.cost) #offre la plus petite.

            if buyer.redemption_value < seller.cost:
                print("No trade occurred")
            else:
                # Trade occurs, choose price randomly between buyer value and seller value
                price = determine_price(seller.cost, buyer.redemption_value,type_price_determined)
                print(f"Trade occurred: buyer value = {buyer.redemption_value}, seller value = {seller.cost}, price = {price}")
                buyer.bought_quantities = 1
                seller.sold_quantities = 1
            # Record demand and supply
            demand.append(buyer.redemption_value)
            supply.append(seller.cost)
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

run_simulation(1,1)
