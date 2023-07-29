import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

class LimitOrderBook:
    """The Limit Order Book (LOB)."""

    def __init__(self):
        """Initialize a new empty limit order book."""
        self._book = pd.DataFrame({
            'Time' : pd.Series(dtype='str'),
            'Side': pd.Series(dtype='str'),
            'Price': pd.Series(dtype='float'),
            'Size': pd.Series(dtype='float'),
            'Quantity': pd.Series(dtype='int')
            })

    def from_CBLev2(self, cb_data):
        """Initialize a limit order book from a Coinbase API Level 2 request."""
        asks, bids = pd.DataFrame(cb_data['asks']), pd.DataFrame(cb_data['bids'])
        asks['Side'] = 'Ask'
        bids['Side'] = 'Bid'
        self._book = pd.concat([asks, bids]).rename(
            columns={0:'Price', 1:'Size', 2:'Quantity'})
        self._book['Time'] = str(cb_data['time'])
        self._book['Price'] = self._book['Price'].astype(float)
        self._book['Size'] = self._book['Size'].astype(float)
        self._book  = self._book [['Time', 'Side', 'Price', 'Size', 'Quantity']]

    def best_ask(self) : 
        return self._book.loc[self._book['Side']=='Ask'].sort_values(by='Price', ascending=True).iloc[0]
        
    def best_bid(self) : 
        return self._book.loc[self._book['Side']=='Bid'].sort_values(by='Price', ascending=False).iloc[0]
    
    def spread(self) : 
        return self.best_ask()['Price'] - self.best_bid()['Price']

    def __del__(self):
        """Delete this limit order book."""
        del self._book

    def clear(self):
        """Clear all the orders in the book."""
        self._book = pd.DataFrame({
            'Time' : pd.Series(dtype='str'),
            'Side': pd.Series(dtype='str'),
            'Price': pd.Series(dtype='float'),
            'Size': pd.Series(dtype='float'),
            'Quantity': pd.Series(dtype='int')
            })
        
    def display(self, depth=3):
        """Plot a book with specified depth. No aggregation."""
        top_asks = self._book.loc[self._book['Side']=='Ask'].sort_values(by='Price', ascending=True).iloc[:depth]
        top_bids = self._book.loc[self._book['Side']=='Bid'].sort_values(by='Price', ascending=False).iloc[:depth]

        mid_price = 0.5*(self.best_ask()['Price']+self.best_bid()['Price'])
        fig, ax = plt.subplots()
        ax.axvline(x=0, color='black', label=f'Mid-Price={mid_price}')
        ax.bar(top_asks.Price-mid_price, top_asks.Quantity, color='red', width=0.1, edgecolor='black', label='Asks')
        ax.bar(top_bids.Price-mid_price, top_bids.Quantity, color='blue', width=0.1, edgecolor='black', label='Bids')

        ax.xaxis.set_major_formatter('{x:1.2f}')
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        ax.set_xlabel('Quantity')
        ax.set_xlabel('Quantity')
        plt.legend(frameon=True)
        plt.show()

    def display_aggregated(self, depth=3):
        """Plot a book with specified depth. 
        Aggregation."""
        top_asks = self._book.loc[self._book['Side']=='Ask'].sort_values(by='Price', ascending=True).iloc[:depth]
        top_bids = self._book.loc[self._book['Side']=='Bid'].sort_values(by='Price', ascending=False).iloc[:depth]

        mid_price = 0.5*(self.best_ask()['Price']+self.best_bid()['Price'])
        fig, ax = plt.subplots()
        ax.axvline(x=0, color='black', label=f'Mid-Price={mid_price}')
        ax.bar(top_asks.Price-mid_price, top_asks.Quantity, color='red', width=0.1, edgecolor='black', label='Asks')
        ax.bar(top_bids.Price-mid_price, top_bids.Quantity, color='blue', width=0.1, edgecolor='black', label='Bids')

        ax.xaxis.set_major_formatter('{x:1.2f}')
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        ax.set_xlabel('Quantity')
        ax.set_xlabel('Quantity')
        plt.legend(frameon=True)
        plt.show()


    def limit_sell(self, order_id, quantity, price):
        """
        Place a sell limit order with given quantity and price.

        Args:
            order_id: the ID for the order to add
            quantity: the quantity of shares in the limit order to place
            price: the price of the limit order to place

        Returns:
            None

        """
        # Library.functions.limit_sell(self._book, order_id, quantity, price)

    # def limit_buy(self, order_id, quantity, price):
    #     """
    #     Place a sell limit order with given quantity and price.

    #     Args:
    #         order_id: the ID for the order to add
    #         quantity: the quantity of shares in the limit order to place
    #         price: the price of the limit order to place

    #     Returns:
    #         None

    #     """
    #     Library.functions.limit_buy(self._book, order_id, quantity, price)

    # def limit(self, side, order_id, quantity, price):
    #     """
    #     Place a sell limit order with given quantity and price.

    #     Args:
    #         side: the side of the order to place
    #         order_id: the ID for the order to add
    #         quantity: the quantity of shares in the limit order to place
    #         price: the price of the limit order to place

    #     Returns:
    #         None

    #     """
    #     Library.functions.limit(self._book, side, order_id, quantity, price)

    # def has(self, order_id):
    #     """
    #     Return true if the order with given ID is in the book, false otherwise.

    #     Args:
    #         order_id: the ID of the order to check for existence of

    #     Returns:
    #         True if the order is in the book, False otherwise

    #     """
    #     return Library.functions.has(self._book, order_id)

    # # def get(self, order_id):
    # #     """
    # #     Return a pointer to the order with given ID.
    # #
    # #     Args:
    # #         order_id: the ID of the order to get
    # #
    # #     Returns:
    # #         an order object wrapped around the pointer
    # #
    # #     """
    # #     # pointer = Library.functions.get(self._book, order_id)
    # #     raise NotImplementedError

    # def cancel(self, order_id):
    #     """
    #     Cancel an order with given order ID.

    #     Args:
    #         order_id: the ID of the order to cancel

    #     Returns:
    #         None

    #     """
    #     Library.functions.cancel(self._book, order_id)

    # def market_sell(self, order_id, quantity):
    #     """
    #     Place a market sell order.

    #     Args:
    #         order_id: the ID for the order to add
    #         quantity: the quantity of shares in the market order to place

    #     Returns:
    #         None

    #     """
    #     Library.functions.market_sell(self._book, order_id, quantity)

    # def market_buy(self, order_id, quantity):
    #     """
    #     Place a market buy order.

    #     Args:
    #         order_id: the ID for the order to add
    #         quantity: the quantity of shares in the market order to place

    #     Returns:
    #         None

    #     """
    #     Library.functions.market_buy(self._book, order_id, quantity)

    # def market(self, side, order_id, quantity):
    #     """
    #     Place a market order.

    #     Args:
    #         side: the side of the order to place
    #         order_id: the ID for the order to add
    #         quantity: the quantity of shares in the market order to place

    #     Returns:
    #         None

    #     """
    #     Library.functions.market(self._book, side, order_id, quantity)

    # def best_sell(self):
    #     """Return the best sell price in the book."""
    #     return Library.functions.best_sell(self._book)

    # def best_buy(self):
    #     """Return the best buy price in the book."""
    #     return Library.functions.best_buy(self._book)

    # def best(self, side):
    #     """
    #     Return the best price for the given side.

    #     Args:
    #         side: the side of the book to get the best price for (False=sell)

    #     Returns:
    #         the best price for the given side of the book

    #     """
    #     return Library.functions.best(self._book, side)

    # def volume_sell(self, price=None):
    #     """
    #     Return the volume of the sell side of the book at the given price.

    #     Args:
    #         price: the price to get the volume at

    #     Returns:
    #         the volume of orders at the given price

    #     Note:
    #         returns the total sell-side volume if price is `None`

    #     """
    #     if price is None:
    #         return Library.functions.volume_sell(self._book)
    #     return Library.functions.volume_sell_price(self._book, price)

    # def volume_buy(self, price=None):
    #     """
    #     Return the volume of the buy side of the book at the given price.

    #     Args:
    #         price: the price to get the volume at

    #     Returns:
    #         the volume of orders at the given price

    #     Note:
    #         returns the total buy-side volume if price is `None`

    #     """
    #     if price is None:
    #         return Library.functions.volume_buy(self._book)
    #     return Library.functions.volume_buy_price(self._book, price)

    # def volume(self, price=None):
    #     """
    #     Return the volume of the book at the given price.

    #     Args:
    #         price: the price to get the volume at

    #     Returns:
    #         the volume of orders at the given price

    #     Note:
    #         returns the total volume if price is `None`

    #     """
    #     if price is None:
    #         return Library.functions.volume(self._book)
    #     return Library.functions.volume_price(self._book, price)

    # def count_at(self, price):
    #     """
    #     Return the count at the given limit price.

    #     Args:
    #         price: the price to get the count of the book for

    #     Returns:
    #         the count of the book at the given price

    #     """
    #     return Library.functions.count_at(self._book, price)

    # def count_sell(self):
    #     """Return the count of the book on the sell side."""
    #     return Library.functions.count_sell(self._book)

    # def count_buy(self):
    #     """Return the count of the book on the buy side."""
    #     return Library.functions.count_buy(self._book)

    # def count(self):
    #     """Return the total count of the book (number of orders)."""
    #     return Library.functions.count(self._book)
