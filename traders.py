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
        self.equilibrium_prices = []
        self.total_surplus = []
        self.run_market(num_rounds)

    def run_market(self, num_rounds):
        for _ in range(num_rounds):
            bids = [trader.make_bid() for trader in self.traders]
            bids.sort()
            equilibrium_price = bids[len(bids)//2]
            self.equilibrium_prices.append(equilibrium_price)
            self.total_surplus.append(sum(bid for bid in bids if bid <= equilibrium_price))

    def plot_results(self):
        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.plot(self.equilibrium_prices)
        plt.title('Prix d\'équilibre au fil du temps')
        plt.xlabel('Tour d\'enchère')
        plt.ylabel('Prix d\'équilibre')

        plt.subplot(1, 2, 2)
        plt.plot(self.total_surplus)
        plt.title('Surplus total extrait au fil du temps')
        plt.xlabel('Tour d\'enchère')
        plt.ylabel('Surplus total extrait')

        plt.tight_layout()
        plt.show()

market = Market(10, 50)
market.plot_results()
