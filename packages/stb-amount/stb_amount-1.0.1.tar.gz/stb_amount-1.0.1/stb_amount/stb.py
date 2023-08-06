# stock and finance calculation
# using for add, remove and update old value with old value to return value that leave
class ISTBAmount:

    def __init__(self, available: int | float):
        self._available = available

    @property
    def available(self):
        return self._available

    @available.setter
    def available(self, available):
        self._available = available


class STBAmount(ISTBAmount):

    def insert(self, amount):
        self.available = self.available + amount
        return self.available

    def update_insert(self, last_amount, new_amount):
        self.available = self.available - last_amount + new_amount
        return self.available

    def update_remove(self, last_amount, new_amount):
        self.available = self.available + last_amount - new_amount
        return self.available

    def remove(self, amount):
        self.available = self.available - amount
        return self.available
