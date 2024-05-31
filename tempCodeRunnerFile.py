
    def run_simulation(self):
        # Get parameters
        params = {name: var.get() for name, var in self.parameters.items()}
        
        # Convert parameters to appropriate types
        type_double_auction = int(params["Type de double enchère"])
        type_price_determined = int(params["Méthode pour le prix d'équilibre"])
        ZI_C = params["ZI-Traders C(1) ou U(0)"].lower() == 'true'
        change_random = params["Random Gaussien(1) ou Uniforme(0)"].lower() == 'true'
        
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
                            effective_profit += (buyer.redemption_value - price)*buyer.bought_quantities[i]
                        for seller in sellers[:m]:
                            seller.sold_quantities[i] = 1
                            effective_profit += (price - seller.cost)*seller.sold_quantities[i]
                        print(effective_profit)
                        max_profit += sum((buyer.redemption_value - seller.cost) for buyer, seller in zip(buyers[:m], sellers[:m]))*m*sellers[0].init_qty[i]
                        self.demand.append(min(bids[:m]))
                        self.supply.append(max(asks[:m]))
                        # Record prices
                        self.prices.append(price)

                if type_double_auction == 2 :
                    buyer = max(buyers, key=lambda t: t.bid) # offre la plus grande 
                    seller = min(sellers, key=lambda t: t.ask) #demande la plus petite.
                    
                    if buyer.bid < seller.ask:
                        print("No trade occurred")
                    else:
                        price = determine_price(seller.ask, buyer.bid, type_price_determined)
                        print(f"Trade occurred: buyer value = {buyer.bid}, seller value = {seller.ask}, price = {price}")
                        buyer.bought_quantities[i] = 1
                        seller.sold_quantities[i] = 1
                        effective_profit += (buyer.redemption_value - price)*buyer.bought_quantities[i] + (price - seller.cost)*seller.sold_quantities[i]
                        max_profit += (buyer.redemption_value - seller.cost)*seller.init_qty[i]
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
        ax.set_xlabel('Round')
        ax.set_ylabel('Price')
        ax.plot(range(len(self.demand)), sorted(self.demand, reverse=True), drawstyle='steps', label='Demand')
        ax.plot(range(len(self.supply)), sorted(self.supply), drawstyle='steps', label='Supply')
        #ax.plot(range(len(self.demand)), drawstyle='steps', label='Demand',marker='o')
        #ax.plot(range(len(self.supply)), drawstyle='steps', label='Supply')
        self.canvas.draw()

        # Update text area
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, f"Allocative efficiency: {allocative_efficiency * 100}%")
        self.current_plot = 0  # Add this line to keep track of the current plot

    def next_plot(self):
        self.current_plot =(self.current_plot + 1)%2
        self.update_plot()

    def prev_plot(self):
        self.current_plot =(self.current_plot - 1)%2
        self.update_plot()

    def update_plot(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.set_xlabel('Round')
        ax.set_ylabel('Price')
        if self.current_plot == 0:

            ax.plot(range(len(self.demand)), sorted(self.demand, reverse=True), drawstyle='steps', label='Demand')
            ax.plot(range(len(self.supply)), sorted(self.supply), drawstyle='steps', label='Supply')
            # ax.plot(range(len(self.demand)), drawstyle='steps', label='Demand',marker='o')
            # ax.plot(range(len(self.supply)), drawstyle='steps', label='Supply')
        elif self.current_plot == 1:
            ax.plot(range(len(self.prices)), self.prices, label='Prices', marker='o')
            ax.legend()
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # Ensure x-axis values are integers

        self.canvas.draw()
    def close_window(self):
        self.destroy()
