"""
Write a class to represent a Cash Register.
You class should keep the state of price total and purchased items
------------------------
1. you can add new variables and function if you want to
2. you will NEED to add accepted method parameters where required.
For example, method add_item probably accepts some kind of an item?..
3. You will need to write some examples of how your code works.
"""
import pandas as pd
import unittest

class CashRegister:
    list = []
    subtotal = 0
    total = 0
    discount = 0
    payment = 0

    """Adds Items through register"""
    def add_item(self, item):
        self.list.append(item)
        self.subtotal = item.final_price + self.subtotal
        self.discount = item.discount_currency + self.discount

    """Calculates the total"""
    def get_total(self):
        self.total = self.subtotal

    """Accepts payment from customer"""
    def cash_payment(self, payment):
        self.change = payment - self.total

    """resets register"""
    def reset_register(self):
        self.list = []
        self.subtotal = 0
        self.total = 0
        self.discount = 0
        self.payment = 0

    """removes items from checkout"""
    def remove_item(self, item):
        self.list.remove(item)
        self.subtotal = item.final_price + self.subtotal
        self.discount = self.subtotal * 0.19

    """formats subtotal"""
    def __str__(self):
        return " Subtotal: {:.2f}".format(self.subtotal)

class Item:
    def __init__(self, item, code, price, discount):
        self.item = item
        self.code = int(code)
        self.price = float(price)
        """In place of def apply_discount"""
        self.discount = float(discount)  # DECIMAL format
        self.discount_currency = self.discount * self.price  # currency format
        self.final_price = self.price - self.discount_currency
        self.percentage_discount = self.discount * 100

    """In place of def show_items"""
    def __str__(self):
        return "Item:  {:25s}   \n  Price: {:.2f}  |    Discount: -  {:.2f}  ({} %) \n  Final Price: {:.2f}  |" \
            .format(self.item.values[0], self.price, self.discount_currency, self.percentage_discount, self.final_price)

"""Code that reads the file as csv that contains the item list"""
df = pd.read_csv('items.txt', ',', index_col=False, header=0, skiprows=0)

"""unit testing"""
class ItemTest(unittest.TestCase):
    # testing the final price of item 1
    def test_Item_26(self):
        self.item = Item('Cashmere Dress', 1, 1590.99, 0.25)
        self.assertEqual(1193.24, round(self.item.final_price, 2))

    # testing the subtotal of two items, item 7 + item 8
    def test_Items_7_and_8(self):
        self.total = CashRegister()
        self.total.add_item(Item('Wool Trousers', 7, 890.99, 0.45))
        self.total.add_item(Item('Cashmere Socks', 8, 159.99, 0.45))
        self.assertEqual(578.04, round(self.total.subtotal, 2))

    # testing the give change function  by adding items 7 and 8 and paying 700 in cash
    def test_Items_7_and_8_give_change(self):
        self.total = CashRegister()
        self.total.add_item(Item('Wool Trousers', 7, 890.99, 0.45))
        self.total.add_item(Item('Cashmere Socks', 8, 159.99, 0.45))
        self.total.get_total()
        self.total.cash_payment(700)
        self.assertEqual(121.96, round(self.total.change, 2))

"""code that gets executed"""
def start():
    total = CashRegister()
    a = []
    flag = True
    e = 0
    """displays item list for ease of reference for cashier and then prints note to cashier"""
    print(df.head(15))
    print('                                          ')
    print(
        'NOTE TO FARFETCH POP-UP STAFF: Today is BLACK FRIDAY! all items are discounted for one day only! UP TO 50% OFF'"\n"
        'CASH ONLY TILL')
    print(
        '--------------------------------------------------------------------------------------------------------------')
    """while loop to allow for continuous entry of items unless terminated by end"""
    while flag:
        print('Item Code numbers range from 1-15 and should be input one item code at a time.'"\n"
              'When all items are entered type END to checkout.'"\n"
              'Please enter the Item Code here:')
        code = input()
        if len(code) < 1:
            continue
        elif 'end' == code.lower():
            total.get_total()
            print(total)
            print(" Total Discount APPLIED: £ {:.2f}  ""\n"
                  "*****************************************""\n"
                  " TOTAL TO PAY: £ {:.2f}".format(total.discount, total.total))
            print('*****************************************')
            print('Enter the amount paid by the customer:')
            payment = input()
            while len(payment) < 1:
                print('Enter the amount paid by the customer:')
                payment = input()
                continue
            payment = float(payment)
            total.cash_payment(payment)
            while total.change < 0:
                print('The amount paid MUST be greater than the total')
                payment = float(input())
                total.cash_payment(payment)
            print("Change: {:.2f}".format(total.change))
            print('*****************************************')
            flag = False

        else:
            df_find = df[df['Code'] == int(code)]
            if len(df_find) == 0:
                print('Unfortunately, that code does not exist')
                continue
            item = df_find.Item
            price = df_find.Price
            discount = df_find.Discount
            a.append(Item(item, code, price, discount))
            total.add_item(a[e])
            print(total.list[e], total)
            e += 1

start()

if __name__ == '__main__':
    unittest.main()
