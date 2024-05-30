import math
import random

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

a_Buyer = 147 # A € [133,200]
v_Seller = 14  # V € [0,67]
default_rounds = 20 

class Trader:
    def __init__(self, id, trader_type, num_rounds = default_rounds):
        self.id = id
        self.trader_type = trader_type
        # chaque vendeur dispose d'une unité de bien et chaque acheteur dispose de 0 unité
        self.init_qty = np.full(num_rounds, 1) 
        self.redemption_value = (a_Buyer - 7*self.id) if trader_type == "buyer" else None
        self.cost = (v_Seller + 7*self.id) if trader_type == "seller" else None
        self.sold_quantities = np.full(num_rounds, 0)  if  trader_type == "seller" else None
        self.bought_quantities = np.full(num_rounds, 0) if trader_type == "buyer" else None
        self.ask = 0 if  trader_type == "seller" else None
        self.bid = 0 if trader_type == "buyer" else None
        
    def has_traded(self, round):    
        """Determine si un trader a tradé au tour courant

        Args:
            round (int): indice du tour courant

        Returns:
            bool: True si le trader a tradé au tour courant, False sinon
        """
        if self.trader_type == "buyer":
            return self.bought_quantities[round] ==1
        elif self.trader_type == "seller":
            return self.sold_quantities[round] ==1
        

def create_traders():
    """Créé les traders qui vont participé à la imulation de marché 
    Il doit y avoir autant de traders que de rounds. 
    

    Returns:
        Table: contient deux types de traders, le vendeurs et les acheteurs 
    """
    buyers = [Trader(i,"buyer") for i in range(default_rounds)]
    sellers = [Trader(i,"seller") for i in range(default_rounds)]
    return buyers + sellers

def determine_price(ask,bid,type_price_determined) :
    """Cette fonction détermine le 
    Args:
        ask (double): prix généré par le vendeur pour le tour
        bid (double): prix généré par l'acheteur pour le tour
        type_price_determined (double): valeur qui permet d'indiquer la manière avec laquelle le 
        prix de l'échange sera fixé

    Returns:
        double: prix que va proposé un trader en fonction 
    du type d'échanges que l'onsouhaite simuler
    """
    if type_price_determined == 1 :
        return random.choice([ask,bid])
    elif type_price_determined == 2 :
        return int(random.uniform(ask,bid))
    elif type_price_determined == 3 :
        return (ask + bid)/2
def initialise_ask(ZI_C, change_random, sellers,buyers,type_price_determined):
    if change_random:
        if ZI_C :
            seller_costs = [seller.cost for seller in sellers]
            buyer_redemption_values = [buyer.redemption_value for buyer in buyers]
            mu = determine_price(sum(seller_costs)/len(seller_costs), sum(buyer_redemption_values)/len(buyer_redemption_values), type_price_determined)  # Mean
            sigma = 30  # Standard deviation
        else :
            mu = 100  # Mean
            sigma = 30  # Standard deviation
        for t in sellers:
            t.ask = random.gauss(mu, sigma)
            while t.ask < 0 or t.ask > 200:
                t.ask = random.gauss(mu, sigma)
        for t in buyers:
            t.bid = random.gauss(mu, sigma)
            while t.bid < 0 or t.bid > 200:
                t.bid = random.gauss(mu, sigma)

            
    else :
        if ZI_C :
            for t in sellers:
                t.ask = random.uniform(t.cost, 200)
            for t in buyers:
                t.bid = random.uniform(0, t.redemption_value)
        else :
            for t in sellers:
                t.ask = random.uniform(0, 200)
            for t in buyers:
                t.bid = random.uniform(0, 200)
    
        
import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Simulation")

        # Create left frame for parameters
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        # Create right frame for plots
        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create parameter entries
        self.parameters = {
            "type_double_auction": tk.StringVar(),
            "type_price_determined": tk.StringVar(),
            "ZI_C": tk.StringVar(),
            "change_random": tk.StringVar()
        }
        for i, (name, var) in enumerate(self.parameters.items()):
            tk.Label(self.left_frame, text=name).grid(row=i, column=0)
            tk.Entry(self.left_frame, textvariable=var).grid(row=i, column=1)

        # Create run button
        self.run_button = tk.Button(self.left_frame, text="Simuler", command=self.run_simulation)
        self.run_button.grid(row=len(self.parameters), column=0, columnspan=2)

        # Create next button
        self.next_button = tk.Button(self.left_frame, text="Next", command=self.next_plot)
        self.next_button.grid(row=len(self.parameters) + 1, column=0, columnspan=2)

        # Create prev button
        self.prev_button = tk.Button(self.left_frame, text="Prev", command=self.prev_plot)
        self.prev_button.grid(row=len(self.parameters) + 2, column=0, columnspan=2)

        # Create end button
        self.end_button = tk.Button(self.left_frame, text="End", command=self.close_window)
        self.end_button.grid(row=len(self.parameters) + 3, column=0, columnspan=2)

        # Create plot area
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create text area for allocative efficiency
        self.text_area = tk.Text(self.right_frame, height=2)
        self.text_area.pack(side=tk.BOTTOM, fill=tk.X)

    def run_simulation(self):
        # Get parameters
        params = {name: var.get() for name, var in self.parameters.items()}
        
        # Convert parameters to appropriate types
        type_double_auction = int(params["type_double_auction"])
        type_price_determined = int(params["type_price_determined"])
        ZI_C = params["ZI_C"].lower() == 'true'
        change_random = params["change_random"].lower() == 'true'
        
        traders = create_traders()
        random.shuffle(traders)
        effective_profit = 0
        max_profit = 0

        self.demand = [] # à chaque tuple [quantité,itération] on associera un prix. 
        self.supply = [] # à chaque tuple [quantité,itération] on associera un prix. 
        self.prices = [] # représente les différents prix auquels ont été vendus les produits à chaque round
        
        for i in range(default_rounds):  # Run for default_rounds rounds
            buyers = [t for t in traders if t.trader_type ==  "buyer" and not t.has_traded(i)]
            sellers = [t for t in traders if t.trader_type ==  "seller" and not t.has_traded(i)]
            initialise_ask(ZI_C,change_random,sellers,buyers,type_price_determined)
            asks = sorted([t.ask for t in sellers])
            bids = sorted([t.bid for t in buyers], reverse=True)
        
            if not buyers or not sellers:
                break  # No more trades can be made
            else :
                if type_double_auction == 1 : 

                    # Find the maximum number of possible trades
                    m = 0
                    while m < len(asks) and m < len(bids) and asks[m] <= bids[m]:
                        m += 1

                    if m == 0:
                        print("No trade occurred")
                    else:
                        # Trades occur, choose price as the average of the highest ask and lowest bid among the m trades
                        price = determine_price(max(asks[:m]), min(bids[:m]), type_price_determined)
                        print(f"{m} trades occurred at price = {price} with buyer's price = {min(bids[:m])} and seller price = {max(asks[:m])}")
                        
                        
                        # Update quantities and calculate individual gains
                        for buyer in buyers[:m]:
                            buyer.bought_quantities[i] = 1
                            effective_profit += max(0, (buyer.redemption_value - price)*buyer.bought_quantities[i])
                        for seller in sellers[:m]:
                            seller.sold_quantities[i] = 1
                            effective_profit += max(0, (price - seller.cost)*seller.sold_quantities[i])
                        print(effective_profit)
                        max_profit += sum(abs(buyer.redemption_value - seller.cost) for buyer, seller in zip(buyers[:m], sellers[:m]))*m*sellers[0].init_qty[i]
                        self.demand.append(min(bids[:m]))
                        self.supply.append(max(asks[:m]))
                        # Record prices
                        self.prices.append(price)

                if type_double_auction == 2 :
                    buyer = max(buyers, key=lambda t: t.bid) # semande la plus grande 
                    seller = min(sellers, key=lambda t: t.ask) #offre la plus petite.
                    
                    if buyer.bid < seller.ask:
                        print("No trade occurred")
                    else:
                        # Trade occurs, choose price randomly between buyer value and seller value
                        
                        price = determine_price(seller.ask, buyer.bid, type_price_determined)
                        print(f"Trade occurred: buyer value = {buyer.bid}, seller value = {seller.ask}, price = {price}")
                        buyer.bought_quantities[i] = 1
                        seller.sold_quantities[i] = 1
                        effective_profit += (buyer.redemption_value - price)*buyer.bought_quantities[i] + (price - seller.cost)*seller.sold_quantities[i]
                        max_profit += abs(buyer.redemption_value - seller.cost)*seller.init_qty[i]
                        # Record demand and supply
                        self.demand.append(buyer.bid)
                        self.supply.append(seller.ask)
                        self.prices.append(price)

        # ...
        # Calculez l'efficience allocative
        if max_profit == 0:
            print("No trades were made, allocative efficiency is undefined.")
        else:
            allocative_efficiency = effective_profit / max_profit
            # Affichez l'efficience allocative
            print(f"Allocative efficiency: {allocative_efficiency * 100}%")

        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.plot(range(len(self.demand)), sorted(self.demand, reverse=True), drawstyle='steps', label='Demand')
        ax.plot(range(len(self.supply)), sorted(self.supply), drawstyle='steps', label='Supply')
        self.canvas.draw()

        # Update text area
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, f"Allocative efficiency: {allocative_efficiency * 100}%")
        self.current_plot = 0  # Add this line to keep track of the current plot

    def next_plot(self):
        self.current_plot += 1
        self.update_plot()

    def prev_plot(self):
        self.current_plot -= 1
        self.update_plot()

    def update_plot(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        if self.current_plot == 0:
            ax.plot(range(len(self.demand)), sorted(self.demand, reverse=True), drawstyle='steps', label='Demand')
            ax.plot(range(len(self.supply)), sorted(self.supply), drawstyle='steps', label='Supply')
        elif self.current_plot == 1:
            ax.plot(range(len(self.prices)), self.prices, label='Prices', marker='o')
            ax.set_xlabel('Quantity')
            ax.set_ylabel('Price')
            ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # Ensure x-axis values are integers
            ax.legend()
        self.canvas.draw()
    def close_window(self):
        self.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()