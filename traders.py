import random
import matplotlib.pyplot as plt

class Trader:
    def __init__(self, id, type):
        self.id = id
        self.type = type  # 'ZI-U' or 'ZI-C'
        self.bid = self.make_bid()

    def make_bid(self):
        if self.type == 'ZI-U':
            return random.uniform(0, 500)
        elif self.type == 'ZI-C':
            return random.uniform(0, 100)

class Market:
    def __init__(self, num_sellers, num_buyers, num_rounds, trader_type):
        self.sellers = [Trader(i, trader_type) for i in range(num_sellers)]
        self.buyers = [Trader(i, trader_type) for i in range(num_buyers, num_buyers + num_sellers)]
        self.bids_ZI_U = []
        self.bids_ZI_C = []
        self.run_market(num_rounds)

    def run_market(self, num_rounds):
        for _ in range(num_rounds):
            bids_ZI_U = [trader.make_bid() for trader in self.sellers]
            bids_ZI_C = [trader.make_bid() for trader in self.buyers]
            self.bids_ZI_U.extend(bids_ZI_U)
            self.bids_ZI_C.extend(bids_ZI_C)

    def plot_results(self):
        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.hist(self.bids_ZI_U, bins=20, alpha=0.5, label='Vendeurs')
        plt.title('Distribution des offres des vendeurs')
        plt.xlabel('Offre')
        plt.ylabel('Fréquence')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.hist(self.bids_ZI_C, bins=20, alpha=0.5, label='Acheteurs')
        plt.title('Distribution des offres des acheteurs')
        plt.xlabel('Offre')
        plt.ylabel('Fréquence')
        plt.legend()

        plt.tight_layout()
        plt.show()

trader_type = input("Entrez 0 pour les traders ZI-H et 1 pour les traders ZI-C: ")
trader_type = 'ZI-U' if trader_type == '0' else 'ZI-C'
market = Market(10, 10, 50, trader_type)  # 10 vendeurs, 10 acheteurs, 50 tours
market.plot_results()
