import random
from functools import reduce
import numpy as np
from deap import base, creator, tools
import argparse
from OptimizationTestFunctions import Rastrigin

'''
FUNCTIONS
'''

STARTING_ENERGY = 100
BREED_ENERGY = 150
FIGHT_ENERGY = 5
TO_CHILD_ENERGY = 50
POPULATION_SIZE = 1000
MUTATION_PROB = 0.05
# not an iRace parameters
DIMENSIONS = 4
NUM_OF_GENERATION = 100000
LOW, HIGH = -6, 6

f = Rastrigin(DIMENSIONS)

def evaluate(individual):
    # individual is a list (gene)
    return f(np.array(individual)),


def mutate(individual, lower_bound=LOW, upper_bound=HIGH, indpb=MUTATION_PROB):
    for i in range(DIMENSIONS):
        if random.random() < indpb:
            individual[i] = random.uniform(lower_bound, upper_bound)
    return individual


def crossover(ind1, ind2):
    crossover_point = random.randint(1, DIMENSIONS-1)
    child = toolbox.individual()
    for i in range(0, crossover_point):
        child[i] = ind1[i]
    for i in range(crossover_point, DIMENSIONS):
        child[i] = ind2[i]

    child.energy = 2 * TO_CHILD_ENERGY
    ind1.energy -= TO_CHILD_ENERGY
    ind2.energy -= TO_CHILD_ENERGY
    return child

def crossover2(ind1, ind2):
    child = toolbox.individual()
    for i in range(0, DIMENSIONS):
        if bool(random.getrandbits(1)):
            child[i] = ind1[i]
        else:
            child[i] = ind2[i]
    child.energy = 2 * TO_CHILD_ENERGY
    ind1.energy -= TO_CHILD_ENERGY
    ind2.energy -= TO_CHILD_ENERGY
    return child

def interact(ind1, ind2):
    eval_1 = evaluate(ind1)
    eval_2 = evaluate(ind2)
    if eval_1 > eval_2:
        ind1.energy -= FIGHT_ENERGY
        ind2.energy += FIGHT_ENERGY
    elif eval_1 < eval_2:
        ind1.energy += FIGHT_ENERGY
        ind2.energy -= FIGHT_ENERGY
    return ind1, ind2


def arrange_meetings(population):
    random.shuffle(population)
    for i in range(0, len(population) // 2, 2):
        interact(population[i], population[i + 1])


def wipe_dead(population):
    return list(filter(lambda x: x.energy > 0, population))


def new_generation(population: list):
    good_candidates = list(filter(lambda x: x.energy >= BREED_ENERGY, population))
    random.shuffle(good_candidates)
    if len(good_candidates) % 2 != 0:
        good_candidates.pop()
    for i in range(0, len(good_candidates), 2):
        child = crossover2(good_candidates[i], good_candidates[i + 1])
        mutate(child)
        population.append(child)

'''
INPUT PARSING
'''
# parser = argparse.ArgumentParser()
# parser.add_argument('-i')
# parser.add_argument('-p')
# parser.add_argument('-o')
# parser.add_argument('-c')
# args = parser.parse_args()


'''
PREPARATION OF GEN ALG
'''

creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax, energy=100)

toolbox = base.Toolbox()

# Register the genetic operators
toolbox.register("attr_float", random.uniform, LOW, HIGH)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=DIMENSIONS)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", crossover2)
toolbox.register("mutate", mutate, lower_bound=LOW, upper_bound=HIGH, indpb=MUTATION_PROB)
toolbox.register("interact", interact)
toolbox.register("arrange_meetings", arrange_meetings)
toolbox.register("wipe_dead", wipe_dead)
toolbox.register("new_generation", new_generation)
# Create the initial population
population = toolbox.population(n=POPULATION_SIZE)

'''
MAIN LOOP
1.  Interakcje aka fight
2.  Usuń martwych
3.  Rozmnóż
'''
for gen in range(NUM_OF_GENERATION):  # Number of generations
    toolbox.arrange_meetings(population)
    population = toolbox.wipe_dead(population)
    toolbox.new_generation(population)

    if gen % 1000 == 0:
        best_ind = tools.selBest(population, 1)[0]
        print(evaluate(best_ind))
        sum_energy = reduce(lambda a, b: a + b, map(lambda a: a.energy, population))
        print(sum_energy)
# Print the best individual found
best_ind = tools.selBest(population, 1)[0]
print(best_ind)
print(best_ind.energy)
print(evaluate(best_ind))
