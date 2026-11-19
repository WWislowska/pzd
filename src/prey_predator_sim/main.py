#zrobilam dla 100 symulacji a nie 150, bo moj laptop nie dawal rady

import random
import statistics
from .species import Prey, Predator
from .population import Population

# test 100 krokow i powtarzalnosc
random.seed(42)
pop_a = Population(
    {Prey: 30, Predator: 70},
    p_death=0.1,
    p_reproduce=0.2,
)
for _ in range(100):
    pop_a.natural_selection()

random.seed(42)
pop_b = Population(
    {Prey: 30, Predator: 70},
    p_death=0.1,
    p_reproduce=0.2,
)
for _ in range(100):
    pop_b.natural_selection()

print("Identyczne dla tego samego ziarna:", pop_a.history == pop_b.history)
print("Koniec (pop_a):", pop_a.n)
pop_a.plot_history()
pop_a.plot_histogram("p_reproduce")

# eksperyment bazowy (10 powtorzen, rozne ziarna)
seeds = list(range(10))
end_prey = []
end_pred = []

for s in seeds:
    random.seed(s)
    pop = Population({Prey: 30, Predator: 70}, p_death=0.1, p_reproduce=0.2)
    for _ in range(100):
        pop.natural_selection()
    last = pop.history[-1]
    end_prey.append(last.get(Prey, 0))
    end_pred.append(last.get(Predator, 0))

prey_ext = sum(1 for x in end_prey if x == 0) / len(seeds) * 100
pred_ext = sum(1 for x in end_pred if x == 0) / len(seeds) * 100
prey_avg = sum(end_prey) / len(end_prey)
pred_avg = sum(end_pred) / len(end_pred)

print(f"Baza -> wymarcie Prey: {prey_ext:.1f}%, wymarcie Predator: {pred_ext:.1f}%")
print(
    f"Baza -> srednia koniec Prey: {prey_avg:.2f}, "
    f"Predator: {pred_avg:.2f}"
)

# analiza wrazliwosci (2 parametry x 3 wartosci = 6 scenariuszy, po 10 powtorzen)
grid = {
    "p_reproduce": [0.1, 0.2, 0.3],
    "p_death": [0.05, 0.1, 0.2],
}

for param, vals in grid.items():
    for v in vals:
        p_prey = []
        p_pred = []
        for s in range(10):
            random.seed(100 + s)
            kw = {"p_death": 0.1, "p_reproduce": 0.2}
            kw[param] = v
            pop = Population({Prey: 30, Predator: 70}, **kw)
            for _ in range(100):
                pop.natural_selection()
            last = pop.history[-1]
            p_prey.append(last.get(Prey, 0))
            p_pred.append(last.get(Predator, 0))

        ext_prey = sum(1 for x in p_prey if x == 0) / 10 * 100
        ext_pred = sum(1 for x in p_pred if x == 0) / 10 * 100
        avg_prey = sum(p_prey) / 10
        avg_pred = sum(p_pred) / 10
        print(
            f"{param}={v} | ext Prey: {ext_prey:.0f}%, ext Pred: {ext_pred:.0f}% | "
            f"avg Prey: {avg_prey:.2f}, "
            f"avg Pred: {avg_pred:.2f}"
        )