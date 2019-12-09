class Parent:
    def __init__(self, num):
        self.id = num

class Child(Parent):
    def __init__(self, num):
        Parent.__init__(self, num)
        print(self.id)

c = Child(5)    