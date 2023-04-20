import random
from deap import base, creator, tools


def evaluate(individual):
    # individual is a list (gene)
    return sum(x**2 for x in individual),


def mutate(individual, mu, sigma, indpb):
    return tools.mutGaussian(individual, mu, sigma, indpb)


def mate():
    #   this is crossover
    return


'''
Jak zaimplementować śmierć w ramach energii?
Cechy naszego agenta:
    -> gen;
    -> poziom energii = 0-100;
evaluate określa jak dobry jest nasz agent (fitness(agent.gen))

Inicjalizujemy populacje, każdy ma 100% energii.
n = wielkosc calej populacji
Jak będzie wyglądać pętla:
    -> wybieramy pary losow agentow, lepszy zabiera gorszemu Y energii.31
    -> wybierz x najlepszych agentów;
    -> rozmnażanie (crossover) + mutacje
    -> zabijamy agentów z 0 poziomem energii TODO
'''

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

IND_SIZE = 10
POPULATION_SIZE = 10
NUM_OF_GENERATION = 100
LOW, HIGH = 0, 10

# Register the genetic operators
toolbox.register("attr_float", random.uniform(LOW, HIGH))
toolbox.register("individual", tools.initRepeat,
                 creator.Individual, toolbox.attr_float, n=IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mutate, mu=0, sigma=1, indpb=0.1)

toolbox.register("select", tools.selTournament, tournsize=3)

# Create the initial population
population = toolbox.population(n=POPULATION_SIZE)

# Evaluate the entire population
fitnesses = map(toolbox.evaluate, population)
for ind, fit in zip(population, fitnesses):
    ind.fitness.values = fit

# Genetic algorithm loop
for gen in range(NUM_OF_GENERATION):  # Number of generations

    # Select the next generation of individuals
    offspring = toolbox.select(population, len(population))

    # Clone the selected individuals
    offspring = list(map(toolbox.clone, offspring))

    # Apply crossover and mutation on the offspring
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        toolbox.mate(child1, child2)
        del child1.fitness.values
        del child2.fitness.values

    for mutant in offspring:
        toolbox.mutate(mutant)
        del mutant.fitness.values

    # Evaluate offspring fitness
    fitnesses = map(toolbox.evaluate, offspring)
    for ind, fit in zip(offspring, fitnesses):
        ind.fitness.values = fit

    # Replace the old population with the offspring
    population[:] = offspring

# Print the best individual found
best_ind = tools.selBest(population, 1)[0]
print("Best individual: ", best_ind)
print("Best fitness value: ", best_ind.fitness.values[0])