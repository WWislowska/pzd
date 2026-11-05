from .population import Population

population = Population(
    100,
    p_death=0.2,
    p_reproduce=0.3
)

for _ in range(20):
    population.natural_selection()

print("Population size:", population.n)
print("History:", population.history)

population.plot_history()