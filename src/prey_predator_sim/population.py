import random
from .species import Creature, Prey, Predator
import matplotlib.pyplot as plt

class Population:

    _instances: set[Creature] #wszystkie aktualnie zyjace Creature
    history: list[dict] #historia liczebnosci populacji

    def __init__(self, population_data: dict, **kwargs):

        self._instances = set()
        for cls, count in population_data.items(): #cls-nazwa klasy, count-ilczba osobnikow
            for _ in range(count):
                self._instances.add(cls(**kwargs))

        self.history = [self.n]

    def count_species(self) -> dict:
        """zlicza ilosc zyjacych osobnikow poszczegolnych grup"""
        counts = {Prey: 0, Predator: 0}
        for creature in self._instances:
            if creature.alive:
                cls = type(creature)
                counts[cls] = counts.get(cls, 0) + 1
        return counts

    def hunting(self):
        """interakcje miedzy predatorem i ofiara"""
        predators = [c for c in self._instances if c.alive and isinstance(c, Predator)]
        preys = [c for c in self._instances if c.alive and isinstance(c, Prey)]
        random.shuffle(predators)
        random.shuffle(preys)

        for pred, prey in zip(predators, preys):
            pred.hunt(prey)
    
    def natural_selection(self): #zmiana kolejnosci, zeby osobniki mogly miec potomstwo nawet jesli zgina w iteracji
        """symuluje jeden cykl selekcji naturalnej: rozmazanie, polowanie, smierc"""
        offspring = set()

        for creature in self._instances:
            new_creature = creature.reproduce()

            if new_creature is not None:
                offspring.add(new_creature)
    
        self.hunting()

        for creature in self._instances:
            creature.kill()

        self._instances = set([creature for creature in self._instances if creature.alive])
        self._instances.update(offspring)

        self.history.append(self.n)


    def plot_history(self):
        prey_hist = [h.get(Prey, 0) for h in self.history]
        pred_hist = [h.get(Predator, 0) for h in self.history]
        plt.plot(prey_hist, label="Prey")
        plt.plot(pred_hist, label="Predator")
        plt.xlabel("Pokolenie")
        plt.ylabel("Liczebność populacji")
        plt.title("Historia populacji")
        plt.grid()
        plt.legend()
        plt.show()

    def plot_histogram(self, attr: str):
        values = [getattr(c, attr) for c in self._instances if c.alive and hasattr(c, attr)]
        plt.hist(values, bins=15)
        plt.xlabel(attr)
        plt.ylabel("Liczebność")
        plt.title(f"Histogram: {attr}")
        plt.show()

    @property
    def n(self):
        return self.count_species()
