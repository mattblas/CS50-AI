import random

class test_set():

    def __init__(self, mines=8):
        self.mines = set()

        for i in range(8):
            h = random.randrange(4)
            w = random.randrange(4)
            self.mines.add((h,w))

    def print(self):
        print(self.mines)

my_test_set = test_set()
my_test_set.print()        
