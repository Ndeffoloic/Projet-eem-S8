import matplotlib.pyplot as plt
import numpy as np


class ZITrader:
    def __init__(self, id, type, ZI_type, ZI_limit=0, value=0):
        self.ZI_type = ZI_type
        self.type = type
        self.ZI_limit = 0 if self.ZI_type == 'ZI-U' else ZI_limit
        self.id = id
        self.value = value  # redemption_value for buyers, cost for sellers
        self.offer = None
        self.demand = None
        self.trade = False
        self.profit = 0
        self.units = 1 if self.type == 'seller' else 0  # sellers start with 1 unit, buyers with 0

    def generate_offer_demand(self):
        if self.ZI_type == 'ZI-U':
            self.offer = np.random.randint(1, 200) if self.type == 'seller' else None
            self.demand = np.random.randint(1, 200) if self.type == 'buyer' else None
        elif self.ZI_type == 'ZI-C':
            if self.type == 'seller' and self.value > 1:
                self.offer = np.random.randint(1, self.value)
            elif self.type == 'buyer':
                self.demand = np.random.randint(self.value, 200)
                
    def accept_offer_demand(self, price):
        if self.ZI_type == 'ZI-U':
            self.trade = True
            self.profit = price - self.value if self.type == 'seller' else self.value - price
        elif self.ZI_type == 'ZI-C':
            self.trade = (price < self.value) if self.type == 'buyer' else (price > self.value)
            self.profit = price - self.value if self.type == 'seller' else self.value - price
        return self.trade

# Initialize the market with 20 ZI-traders
A = 200  # buyer's maximum willingness to pay
V = 0  # seller's minimum acceptable price
traders = [ZITrader(i, 'buyer', 'ZI-C', value=A - 7 * i) for i in range(20)] + \
           [ZITrader(i + 20, 'seller', 'ZI-C', value=V + 7 * i) for i in range(20)]

def double_auction(traders, num_rounds):
    transactions = []
    equilibrium_prices = []
    avg_offer_prices = []
    avg_demand_prices = []
    for _ in range(num_rounds):
        for trader in traders:
            if trader.units > 0:  # only generate offer/demand if the trader has units left
                trader.generate_offer_demand()
        sellers = sorted([t for t in traders if t.type == 'seller' and t.units > 0], key=lambda t: t.offer)
        buyers = sorted([t for t in traders if t.type == 'buyer' and t.units < 1], key=lambda t: t.demand, reverse=True)
        while sellers and buyers and buyers[0].demand >= sellers[0].offer:
            price = (sellers[0].offer + buyers[0].demand) / 2  # transaction price is the average of offer and demand
            if sellers[0].accept_offer_demand(price) and buyers[0].accept_offer_demand(price):
                transactions.append((sellers[0].id, buyers[0].id, price))
                sellers[0].units -= 1
                buyers[0].units += 1
                sellers.pop(0)
                buyers.pop(0)
        equilibrium_prices.append(transactions[-1][2] if transactions else 0)
        avg_offer_prices.append(np.mean([t.offer for t in traders if t.type == 'seller' and t.units > 0]))
        avg_demand_prices.append(np.mean([t.demand for t in traders if t.type == 'buyer' and t.units < 1]))
    return transactions, equilibrium_prices, avg_offer_prices, avg_demand_prices

transactions, equilibrium_prices, avg_offer_prices, avg_demand_prices = double_auction(traders, 12)

plt.figure(figsize=(12, 6))
plt.plot(equilibrium_prices)
plt.xlabel('Produit')
plt.ylabel('Prix')
plt.title('Prix d\'équilibre')

plt.figure(figsize=(12, 6))
plt.plot(avg_offer_prices, label='Offre moyenne')
plt.plot(avg_demand_prices, label='Demande moyenne')
plt.xlabel('Produit')
plt.ylabel('Prix')
plt.title('Offre et demande moyennes')
plt.legend()

plt.show()