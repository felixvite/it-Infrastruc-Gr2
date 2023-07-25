import unittest

def calculate_total_price(quantity, unit_price):
    if quantity <= 0 or unit_price is None:
        return None
    
    return quantity * unit_price
    
if __name__ == '__main__':
    unittest.main()
