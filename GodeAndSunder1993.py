import random

import matplotlib.pyplot as plt
import numpy as np


class Market:
    def __init__(self, market_type, num_traders, trader_type):
        self.market_type = market_type
        self.traders = [ZITrader(i, 'buyer' if i < num_traders//2 else 'seller', trader_type, market_type) for i in range(num_traders)]

    def simulate(self, num_rounds):
        transactions = []
        for _ in range(num_rounds):
            # Reset trade status and generate new offers/demands for each round
            for trader in self.traders:
                trader.trade = False
                trader.generate_offer_demand()

            # Continue trading until all traders have traded
            while not all(trader.trade for trader in self.traders):
                transaction_proposals = {i:0 for i in range(len(self.traders))}
                for trader in self.traders:
                    if not trader.trade:
                        transaction_proposals[self.traders.index(trader)] = trader.generate_offer_demand()

                sellers = sorted([t for t in self.traders if t.type == 'seller' and not t.trade], key=lambda t: t.offer)
                buyers = sorted([t for t in self.traders if t.type == 'buyer' and not t.trade], key=lambda t: t.demand, reverse=True)

                # Initialize earliestTrader with the first seller who has not yet traded
                earliestTrader = next((s for s in sellers if not s.trade), None)
                if earliestTrader is None:
                    break

                for i in range(min(len(buyers), len(sellers))):
                    if(sellers[i].ltr != buyers[i].ltr) :
                        earliestTrader = sellers[i] if sellers[i].trade == False else earliestTrader 
                    price = earliestTrader.generate_offer_demand()
                    if sellers[i].accept_offer_demand(price) and buyers[i].accept_offer_demand(price) :
                        transactions.append((sellers[i].id, buyers[i].id, price))
                        break
        return transactions



class ZITrader : 
    def __init__(self, id, type, ZI_type, market_type, ZI_limit = 0) -> None:
        self.ZI_type = ZI_type
        self.type = type
        self.market_type = market_type
        self.ZI_limit = 0 if self.ZI_type == 'ZI-U' else ZI_limit
        self.id = id
        self.redemption_value = None
        self.cost = None
        self.offer = None
        self.demand = None
        self.trade = False
        self.profit = 0
        self.ltr = 0 #last_trade_round
        self.traded_goods = []  
        self.surplus = []  
        
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
        return self.offer if self.type == 'seller' else None

    def accept_offer_demand(self, price):
        if self.ZI_type == 'ZI-U' : 
            self.trade = True
            self.profit = price - self.cost if self.type == 'seller' else self.redemption_value - price
        elif self.ZI_type == 'ZI-C' : 
            self.trade = (price < self.redemption_value ) if self.type == 'buyer' else (price > self.cost)
            self.profit = price - self.cost if self.type == 'seller' else self.redemption_value - price
        if self.trade:
            self.traded_goods.append(1) 
            self.surplus.append(self.profit)  
        return self.trade

# Ask the user to enter 1 for ZI-C and 0 for ZI-U
trader_type_input = int(input("Veuillez entrer 1 pour que le code considère les ZI-C et 0 pour que le code considère les ZI-U dans sa simulation: "))
trader_type = 'ZI-C' if trader_type_input == 1 else 'ZI-U'

# Ask the user to enter the market type
market_type_input = int(input("Veuillez entrer le type de marché (1 à 5): "))

# Initialize the market with 24 ZI-traders
market = Market(market_type_input, 24, trader_type)

# Run the double auction mechanism and print the transactions
transactions = market.simulate(12)
for transaction in transactions:
    print(f"Seller {transaction[0]} and buyer {transaction[1]} made a transaction at price {transaction[2]}.")

# Get the final offers and demands
final_offers = [t.offer for t in market.traders if t.type == 'seller']
final_demands = [t.demand for t in market.traders if t.type == 'buyer']

# Sort the offers and demands
final_offers.sort()
final_demands.sort(reverse=True)

# Plot the supply and demand curves
plt.figure(figsize=(12, 6))
plt.step(np.arange(len(final_offers)), final_offers, where='post', label='Offre')
plt.step(np.arange(len(final_demands)), final_demands, where='post', label='Demande')
plt.xlabel('Trader')
plt.ylabel('Prix')
plt.title('Courbes d\'offre et de demande')
plt.legend()

# Get the transaction prices
transaction_prices = [t[2] for t in transactions]

# Plot the transaction prices
plt.figure(figsize=(12, 6))
plt.plot(transaction_prices)
plt.xlabel('Transaction')
plt.ylabel('Prix')
plt.title('Prix des transactions')

# Show the plots
plt.show()
print(len(transactions))
# Print the number of goods traded by each trader
for i, trader in enumerate(market.traders):
    print(f"Trader {i} traded {sum(trader.traded_goods)} goods.")

# Print the surplus of each trader
for i, trader in enumerate(market.traders):
    print(f"Trader {i} has a surplus of {sum(trader.surplus)}.")

# Plot the surplus of buyers and sellers
plt.figure(figsize=(12, 6))
plt.plot([sum(t.surplus) for t in market.traders if t.type == 'buyer'], label='Acheteurs')
plt.plot([sum(t.surplus) for t in market.traders if t.type == 'seller'], label='Vendeurs')
plt.xlabel('Période')
plt.ylabel('Surplus')
plt.title('Surplus des acheteurs et des vendeurs par période')
plt.legend()
plt.show()

