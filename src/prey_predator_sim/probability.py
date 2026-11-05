
class Probability:
    def __set_name__(self, owner, name):

        self.name = name
        self.owner = owner

    def __set__(self, instance, value):

        instance.__dict__[self.name] = max(0, min(1, value))

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]

class Test:

    def __init__(self, p):
        self.probability = p
    
    probability = Probability()

test = Test(1.5)
print(test.probability)
print(test.__dict__)