import random

import numpy as np
from deap import base, creator, tools
import argparse
from OptimizationTestFunctions import Rastrigin

'''
FUNCTIONS
'''

f = Rastrigin(3)

STARTING_ENERGY = 100
BREED_ENERGY = 150
FIGHT_ENERGY = 5
TO_CHILD_ENERGY = 50
POPULATION_SIZE = 100
MUTATION_PROB = 0.1
# not an iRace parameters
INDIVIDUAL_SIZE = 2  # x, y, energy
NUM_OF_GENERATION = 100000
LOW, HIGH = -6, 6


def evaluate(individual):
    # individual is a list (gene)
    return f(np.array(individual)),


def mutate(individual, lower_bound=LOW, upper_bound=HIGH, indpb=MUTATION_PROB):
    for i in range(len(individual)):
        if random.random() < indpb:
            individual[i] = individual[i] + random.uniform(-1, 1)
    return individual


def crossover(ind1, ind2):
    size = min(len(ind1), len(ind2))
    crossover_point = random.randint(0, size)
    child = toolbox.individual()
    child[0] = ind1[0]
    child[1] = ind2[1]
    child.energy = 2 * TO_CHILD_ENERGY
    ind1.energy -= TO_CHILD_ENERGY
    ind2.energy -= TO_CHILD_ENERGY
    return child


def interact(ind1, ind2):
    n = len(ind1)
    eval_1 = evaluate(ind1)
    eval_2 = evaluate(ind2)
    if eval_1 > eval_2:
        ind2.energy += FIGHT_ENERGY
        ind1.energy -= FIGHT_ENERGY
    elif eval_1 < eval_2:
        ind2.energy -= FIGHT_ENERGY
        ind1.energy += FIGHT_ENERGY
    # else:
    #     # print("ASDASDASDADSs")
    return ind1, ind2


def arrange_meetings(population):
    random.shuffle(population)
    for i in range(0, len(population) // 2, 2):
        interact(population[i], population[i + 1])


def wipe_dead(population):
    return list(filter(lambda x: x.energy > 0, population))


def get_parents_pairs(population: list):
    good_candidates = list(filter(lambda x: x.energy > BREED_ENERGY, population))
    random.shuffle(good_candidates)
    for i in range(0, len(good_candidates) // 2, 2):
        child = crossover(good_candidates[i], good_candidates[i + 1])
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
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=INDIVIDUAL_SIZE)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", crossover)
toolbox.register("mutate", mutate, lower_bound=LOW, upper_bound=HIGH, indpb=MUTATION_PROB)
toolbox.register("interact", interact)
toolbox.register("arrange_meetings", arrange_meetings)
toolbox.register("wipe_dead", wipe_dead)
toolbox.register("get_parents_pairs", get_parents_pairs)
# Create the initial population
population = toolbox.population(n=POPULATION_SIZE)

# Evaluate the entire population

'''
MAIN LOOP
'''

'''

1.  Interakcje aka fight
2.  Usuń martwych
3.  Rozmnóż
'''
for gen in range(NUM_OF_GENERATION):  # Number of generations
    toolbox.arrange_meetings(population)
    population = toolbox.wipe_dead(population)
    toolbox.get_parents_pairs(population)


    if gen % 1000 == 0:
        best_ind = tools.selBest(population, 1)[0]
        print(evaluate(best_ind))
        #print(population)
# Print the best individual found
best_ind = tools.selBest(population, 1)[0]
print(best_ind)
print(population)
