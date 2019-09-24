#Dining Philosiphers, http://rosettacode.org/wiki/Dining_philosophers
import random

maxT = int(input("Max tick wait: "))

names = ["Albert",
         "Betty ",
         "Canary",
         "Danice",
         "Eldon "]
forks = [True, True, True, True, True]

class Phil:
    def __init__(self, ind):
        global names, maxT
        self.state = random.choice([True, False])
        self.time = random.randint(max(int(maxT / 10), 1), maxT)
        self.forks = False
        self.pos = ind
        self.name = names[ind]

    def tick(self):
        global forks, maxT
        if(self.state): #If eating
            if(self.forks == False):
                if(forks[self.pos] and forks[(self.pos + 1) % 5]):
                    forks[self.pos] = forks[(self.pos + 1) % 5] = False
                    self.forks = True
                    print("%s starts eating." % self.name)
            else:
                self.time -= 1
                if(self.time == 0):
                    forks[self.pos] = forks[(self.pos + 1) % 5] = True
                    self.forks = False
                    self.state = False
                    print("%s goes away to think about forty-two." % self.name)
                    self.time = random.randint(max(int(maxT / 10), 1), maxT)
        else: #If thinking
            self.time -= 1
            if(self.time == 0):
                self.state = True
                print("%s comes to the table to eat." % self.name)
                self.time = random.randint(max(int(maxT / 10), 1), maxT)
                if(forks[self.pos] and forks[(self.pos + 1) % 5]):
                    forks[self.pos] = forks[(self.pos + 1) % 5] = False
                    self.forks = True
                    print("\t%s already sees forks, and starts eating." % self.name)
    def __str__(self):
        if(self.state):
            if(self.forks):
                return "%s	eating				%s	-> thinking" % (self.name, self.time)
            else:
                return "%s		forks?" % self.name
        else:
            return     "%s			thinking	%s	-> eating" % (self.name, self.time)

phils = [Phil(i) for i in range(5)]



while True:
    [i.tick() for i in phils]
    print()
    for i in phils:
        print(i)
    input()
    print("\n" * 5)
            
                
            
            
