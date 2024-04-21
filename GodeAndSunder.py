import random

import matplotlib.pyplot as plt
import numpy as np


class ZITrader : 
    def __init__(self,id,type,ZI_type,ZI_limit = 0) -> None:
        self.ZI_type = ZI_type
        self.type = type
        self.ZI_limit = 0 if self.ZI_type == 'ZI-U' else ZI_limit
        self.id = id
        self.redemption_value = None
        self.cost = None
        self.offer = None
        self.demand = None
        self.trade = False
        self.profit = 0
        
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
            self.trade = True
            self.profit = price - self.cost if self.type == 'seller' else self.redemption_value - price
        elif self.ZI_type == 'ZI-C' : 
            self.trade = (price < self.redemption_value ) if self.type == 'buyer' else (price > self.cost)
            self.profit = price - self.cost if self.type == 'seller' else self.redemption_value - price
        return self.trade

# Ask the user to enter 1 for ZI-C and 0 for ZI-U
trader_type_input = int(input("Veuillez entrer 1 pour que le code considère les ZI-C et 0 pour que le code considère les ZI-U dans sa simulation: "))
trader_type = 'ZI-C' if trader_type_input == 1 else 'ZI-U'

# Initialize the market with 24 ZI-traders
traders = [ZITrader(i, 'buyer' if i < 12 else 'seller', trader_type) for i in range(24)]

# Define the double auction mechanism
def double_auction(traders,num_rounds):
    # Initialize the list of transactions
    transactions = []
    # Initialize the list of equilibrium prices
    equilibrium_prices = []
    # Initialize the list of average offer and demand prices
    avg_offer_prices = []
    avg_demand_prices = []
    # For each product
    for _ in range(num_rounds):
        # Each ZI-trader generates an offer and a demand
        for trader in traders:
            trader.generate_offer_demand()
        # Sort the sellers by their offer price in ascending order and the buyers by their demand price in descending order
        sellers = sorted([t for t in traders if t.type == 'seller'], key=lambda t: t.offer)
        buyers = sorted([t for t in traders if t.type == 'buyer'], key=lambda t: t.demand, reverse=True)
        # While there are still sellers and buyers
        while sellers and buyers:
            # If the highest demand price is greater than or equal to the lowest offer price
            if buyers[0].demand >= sellers[0].offer:
                # A transaction occurs at the price of the earliest order
                price = sellers[0].offer
                if sellers[0].accept_offer_demand(price) and buyers[0].accept_offer_demand(price) :
                    transactions.append((sellers[0].id, buyers[0].id, price))
                    # Remove the seller and the buyer from the list
                    sellers.pop(0)
                    buyers.pop(0)
            else:
                # The market clears
                break
        # Calculate the equilibrium price (the price of the last transaction)
        equilibrium_prices.append(transactions[-1][2] if transactions else 0)
        # Calculate the average offer and demand prices
        avg_offer_prices.append(sum([t.offer for t in traders if t.type == 'seller']) / len([t for t in traders if t.type == 'seller']))
        avg_demand_prices.append(sum([t.demand for t in traders if t.type == 'buyer']) / len([t for t in traders if t.type == 'buyer']))
    # Return the list of transactions, the list of equilibrium prices, and the lists of average offer and demand prices
    return transactions, equilibrium_prices, avg_offer_prices, avg_demand_prices

# Run the double auction mechanism and print the transactions
transactions, equilibrium_prices, avg_offer_prices, avg_demand_prices = double_auction(traders,200)
for transaction in transactions:
    print(f"Seller {transaction[0]} and buyer {transaction[1]} made a transaction at price {transaction[2]}.")

# Plot the equilibrium prices
plt.figure(figsize=(12, 6))
plt.plot(equilibrium_prices)
plt.xlabel('Produit')
plt.ylabel('Prix')
plt.title('Prix d\'équilibre')

# Plot the average offer and demand prices
plt.figure(figsize=(12, 6))
plt.plot(avg_offer_prices, label='Offre moyenne')
plt.plot(avg_demand_prices, label='Demande moyenne')
plt.xlabel('Produit')
plt.ylabel('Prix')
plt.title('Offre et demande moyennes')
plt.legend()

# Show the plots
plt.show()
