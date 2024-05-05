    for i in range(20):  # Run for 20 rounds
        buyers = [t for t in traders if t.trader_type ==  "buyer" and not t.has_traded]
        sellers = [t for t in traders if t.trader_type ==  "seller" and not t.has_traded]
        nmr_qty = 0 # nombre d'échanges au cours de ce round
        if not buyers or not sellers:
            break  # No more trades can be made
        if type_double_auction == 1 : 
            # Generate and sort asks and bids
            asks = sorted([t.generate_ask() for t in sellers])
            bids = sorted([t.generate_bid() for t in buyers], reverse=True)
