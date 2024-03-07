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
    def __init__(self, num_traders, num_rounds):
        self.traders = [Trader(i, 'ZI-U' if i < num_traders // 2 else 'ZI-C') for i in range(num_traders)]
        self.bids_ZI_U = []
        self.bids_ZI_C = []
        self.run_market(num_rounds)

    def run_market(self, num_rounds):
        for _ in range(num_rounds):
            bids_ZI_U = [trader.make_bid() for trader in self.traders if trader.type == 'ZI-U']
            bids_ZI_C = [trader.make_bid() for trader in self.traders if trader.type == 'ZI-C']
            self.bids_ZI_U.extend(bids_ZI_U)
            self.bids_ZI_C.extend(bids_ZI_C)

    def plot_results(self):
        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.hist(self.bids_ZI_U, bins=20, alpha=0.5, label='ZI-U')
        plt.title('Distribution des offres des traders ZI-U')
        plt.xlabel('Offre')
        plt.ylabel('Fréquence')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.hist(self.bids_ZI_C, bins=20, alpha=0.5, label='ZI-C')
        plt.title('Distribution des offres des traders ZI-C')
        plt.xlabel('Offre')
        plt.ylabel('Fréquence')
        plt.legend()

        plt.tight_layout()
        plt.show()

market = Market(10, 50)
market.plot_results()
