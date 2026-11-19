"""Module with definitions of considered species"""
import random

class Creature:

    alive: bool = True

    def __init__(self, p_death: float, p_reproduce: float):
        self.p_death = p_death
        self.p_reproduce = p_reproduce

    def kill(self):
        if self.alive and (random.random() < self.p_death):
            self.alive = False

    def reproduce(self):
        if self.alive and (random.random() < self.p_reproduce):
            return self.__class__(p_death=self.p_death, p_reproduce=self.p_reproduce)
        return None

    @property
    def p_death(self):
        return self.__p_death

    @p_death.setter
    def p_death(self, value):
        #upwenia sie ze 0 <= wartosc <= 1
        value = min(1.0, max(0.0, value))
        self.__p_death = value

    @property
    def p_reproduce(self):
        return self.__p_reproduce

    @p_reproduce.setter
    def p_reproduce(self, value):
        #upwenia sie ze 0 <= wartosc <= 1
        value = min(1.0, max(0.0, value))
        self.__p_reproduce = value


class Prey(Creature):
    def __init__(self, p_death: float, p_reproduce: float, p_hunt = 0.5):
        super().__init__(p_death, p_reproduce)
        self.p_hunt = p_hunt

    def reproduce(self): #zeby odobniki klasy Prey otrzymywaly tez p_hunt
        if self.alive and random.random() < self.p_reproduce:
            return Prey(
                p_death=self.p_death,
                p_reproduce=self.p_reproduce,
                p_hunt=self.p_hunt
            )
        return None

    @property
    def p_hunt(self):
        return self.__p_hunt

    @p_hunt.setter
    def p_hunt(self, value):
        value = min(1.0, max(0.0, value))
        self.__p_hunt = value


class Predator(Creature):
    p_death_hungry: float = 0.5

    def __init__(self, p_death: float, p_reproduce: float, hungry: bool = True):
        super().__init__(p_death, p_reproduce)
        self.hungry = hungry

    def hunt(self, prey: Prey):
        if self.hungry and random.random() < prey.p_hunt:
            prey.alive = False
            self.hungry = False
        else:
            self.hungry = True

    def kill(self):
        if not self.alive:
            return
        if self.hungry:
            prev_p_death = self.p_death
            self.p_death = self.p_death_hungry
            super().kill()
            self.p_death = prev_p_death
        else:
            super().kill()