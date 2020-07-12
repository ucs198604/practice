class animal:
    '''we are all animals'''
    def __init__(self,name,age):
        self.name = name
        self.age = age
        print(f'here comes a {self.age}-year-old animal')
        
    def speak(self):
        print('bark or mew')
        
class cat(animal):
    def __init__(self, name, age, weight):
        animal.__init__(self, name, age)
        self.wieght = weight
        print(f'a cat called {self.name} is comming')
    def speak(self):
        print('mew')
        
class dog(animal):
    def __init__(self, name, age, weight):
        animal.__init__(self,name,age)
        self.weight = weight
        print(f'a dog called {self.name} is comming')
    def speak(self):
        print('bark')
        
        
a = cat('poka',5,100)
b = dog('husky',1,34)

a.speak()
b.speak()