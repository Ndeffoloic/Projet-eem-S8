import random

import matplotlib.pyplot as plt

a_Buyer = 133 # A € [133,200]
v_Seller = 0  # V € [0,67]
#limit_ZI = 

class Trader:
    def __init__(self, id,ZI_type,trader_type,limit_ZI):
        self.id = id
        self.ZI_type = ZI_type
        self.trader_type = trader_type
        # chaque vendeur dispose d'une unité de bien et chaque acheteur dispose de 0 unité
        self.init_qty = 1 if trader_type == "seller" else None
        self.redemption_value = a_Buyer - 7*self.id if trader_type == "buller" else None
        self.cost = v_Seller + 7*self.id if trader_type == "seller" else None
        self.sold_quantities = 0  if  trader_type == "seller" else None
        self.bought_quantities = 0 if trader_type == "buller" else None

def create_traders(A, V):
    buyers = [Trader(A - i * 7, True) for i in range(20)]
    sellers = [Trader(V + i * 7, False) for i in range(20)]
    return buyers + sellers

def run_simulation(A, V):
    traders = create_traders(A, V)
    random.shuffle(traders)

    demand = []
    supply = []

    for i in range(20):  # Run for 20 rounds
        buyers = [t for t in traders if t.is_buyer and not t.has_traded]
        sellers = [t for t in traders if not t.is_buyer and not t.has_traded]

        if not buyers or not sellers:
            break  # No more trades can be made

        buyer = max(buyers, key=lambda t: t.value)
        seller = min(sellers, key=lambda t: t.value)

        if buyer.value > seller.value:
            # Trade occurs, choose price randomly between buyer value and seller value
            price = random.uniform(seller.value, buyer.value)
            print(f"Trade occurred: buyer value = {buyer.value}, seller value = {seller.value}, price = {price}")
            buyer.has_traded = True
            seller.has_traded = True
        else:
            print("No trade occurred")

        # Record demand and supply
        demand.append(buyer.value)
        supply.append(seller.value)

    # Plot demand and supply
    plt.plot(range(len(demand)), sorted(demand, reverse=True), label='Demand')
    plt.plot(range(len(supply)), sorted(supply), label='Supply')
    plt.xlabel('Quantity')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

run_simulation(150, 50)

run_simulation(150, 50)