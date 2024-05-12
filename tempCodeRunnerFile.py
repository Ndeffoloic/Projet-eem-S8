    import matplotlib.ticker as ticker

    # ...
    # Plot demand and supply
    plt.figure(figsize=(10, 5))
    plt.plot(range(len(demand)), sorted(demand, reverse=True), drawstyle='steps', label='Demand')
    plt.plot(range(len(supply)), sorted(supply), drawstyle='steps', label='Supply')
    plt.xlabel('Quantity')
    plt.ylabel('Price')
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # Ensure x-axis values are integers
    plt.legend()
    plt.show()

    # Plot prices
    plt.figure(figsize=(10, 5))
    plt.plot(range(len(prices)), prices, label='Prices', marker='o')
    plt.xlabel('Quantity')
    plt.ylabel('Price')
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # Ensure x-axis values are integers
    plt.legend()
    plt.show()