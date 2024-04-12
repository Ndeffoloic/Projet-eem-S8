import random

import matplotlib.pyplot as plt
import numpy as np


# Define the ZI-trader class
class ZITrader:
    def __init__(self, id, type, trader_type):
        self.id = id
        self.type = type  # 'buyer' or 'seller'
        self.trader_type = trader_type  # 'ZI-C' or 'ZI-U'
        self.offer = None
        self.demand = None

    def generate_offer_demand(self):
        if self.trader_type == 'ZI-C':
            self.offer = random.randint(1, 200) if self.type == 'seller' else None
            self.demand = random.randint(1, 200) if self.type == 'buyer' else None
        elif self.trader_type == 'ZI-U':
            self.offer = random.randint(1, 200) if self.type == 'seller' else None
            self.demand = random.randint(1, 200) if self.type == 'buyer' else None

# Ask the user to enter 1 for ZI-C and 0 for ZI-U
trader_type_input = int(input("Veuillez entrer 1 pour que le code considère les ZI-C et 0 pour que le code considère les ZI-U dans sa simulation: "))
trader_type = 'ZI-C' if trader_type_input == 1 else 'ZI-U'

# Initialize the market with 24 ZI-traders
traders = [ZITrader(i, 'buyer' if i < 12 else 'seller', trader_type) for i in range(24)]

# Each ZI-trader generates an offer and a demand
for trader in traders:
    trader.generate_offer_demand()

# Define the double auction mechanism
def double_auction(traders):
    # Sort the sellers by their offer price in ascending order and the buyers by their demand price in descending order
    sellers = sorted([t for t in traders if t.type == 'seller'], key=lambda t: t.offer)
    buyers = sorted([t for t in traders if t.type == 'buyer'], key=lambda t: t.demand, reverse=True)

    # Initialize the list of transactions
    transactions = []

    # While there are still sellers and buyers
    while sellers and buyers:
        # If the highest demand price is greater than or equal to the lowest offer price
        if buyers[0].demand >= sellers[0].offer:
            # A transaction occurs at the price of the earliest order
            price = sellers[0].offer if sellers[0].offer < buyers[0].demand else buyers[0].demand
            transactions.append((sellers[0].id, buyers[0].id, price))

            # Remove the seller and the buyer from the market
            sellers.pop(0)
            buyers.pop(0)
        else:
            # The market clears
            break

    # Return the list of transactions
    return transactions

# Run the double auction mechanism and print the transactions
transactions = double_auction(traders)
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
c
# Plot the transaction prices
plt.figure(figsize=(12, 6))
plt.plot(transaction_prices)
plt.xlabel('Transaction')
plt.ylabel('Prix')
plt.title('Prix des transactions')

# Show the plots
plt.show()