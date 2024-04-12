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

# Each ZI-trader generates an offer and a demand
for trader in traders:
    trader.generate_offer_demand()

# Define the double auction mechanism
def double_auction(traders,num_rounds):
    # Sort the sellers by their offer price in ascending order and the buyers by their demand price in descending order
    sellers = sorted([t for t in traders if t.type == 'seller'], key=lambda t: t.offer)
    buyers = sorted([t for t in traders if t.type == 'buyer'], key=lambda t: t.demand, reverse=True)

    # Initialize the list of transactions
    transactions = []
    i = 0
    # While there are still sellers and buyers
    while len(transactions) < num_rounds:
        # If the highest demand price is greater than or equal to the lowest offer price
        if buyers[i%12].trade == False and sellers[i%12].trade == False:
            # A transaction occurs at the price of the earliest order
            price = sellers[i%12].offer if sellers[i%12].offer < buyers[i%12].demand else buyers[i%12].demand
            if sellers[i%12].accept_offer_demand(price) and buyers[i%12].accept_offer_demand(price) :
                transactions.append((sellers[i%12].id, buyers[i%12].id, price))
                i +=1    
        else:
            # The market clears
            break

    # Return the list of transactions
    return transactions

# Run the double auction mechanism and print the transactions
transactions = double_auction(traders,500)
for transaction in transactions:
    print(f"Seller {transaction[0]} and buyer {transaction[1]} made a transaction at price {transaction[2]}.")

# Get the final offers and demands
final_offers = [t.offer for t in traders if t.type == 'seller']
final_demands = [t.demand for t in traders if t.type == 'buyer']

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