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
        return self

    def update_insert(self, last_amount, new_amount):
        self.available = self.available - last_amount + new_amount
        return self

    def update_remove(self, last_amount, new_amount):
        self.available = self.available + last_amount - new_amount
        return self

    def remove(self, amount):
        self.available = self.available - amount
        return self

    def get(self):
        return self.available

# sf = SFCalculator(10)
# sf.insert(1)
# print("insert: {}".format(sf.get()))
# sf.update_insert(1, 2)
# print("update insert: {}".format(sf.get()))
# sf.update_remove(1, 2)
# print("update remove: {}".format(sf.get()))
# sf.remove(1)
# print("remove: {}".format(sf.get()))
