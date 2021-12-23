import os


class Addressbook:

    def __init__(self, cache_directory):
        self.addressbook = {}
        self.filename = os.path.join(cache_directory, "addressbook.txt")
        self.cache = open(self.filename, "w")

    def add(self, name, address):
        self.addressbook[name] = address

    def lookup(self, name):
        return self.addressbook[name]

    def names(self):
        return set(self.addressbook.keys())

    def clear(self):
        self.cache.close()
        os.remove(self.filename)
