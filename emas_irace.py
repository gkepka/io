import random
from functools import reduce
import numpy as np
from deap import base, creator, tools
import argparse
from OptimizationTestFunctions import Rastrigin

import argparse
import sys
import itertools
import statistics

import igraph as ig

g = ig.Graph.Full(3)

def crossover_one_point(ind1, ind2):
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


def crossover_uniform(ind1, ind2):
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


def crossover_blend(ind1, ind2):
    child = toolbox.individual()
    u = random.uniform(0, 1)
    gamma = (1 + 2*ALPHA)*u - ALPHA
    for i in range(0, DIMENSIONS):
        if ind1[i] < ind2[i]:
            child[i] = (1 - gamma)*ind1[i] + gamma*ind2[i]
        else:
            child[i] = (1 - gamma)*ind2[i] + gamma*ind1[i]
    child.energy = 2 * TO_CHILD_ENERGY
    ind1.energy -= TO_CHILD_ENERGY
    ind2.energy -= TO_CHILD_ENERGY
    return child


def crossover_sbx(ind1, ind2):
    ind1_clone = toolbox.clone(ind1)
    ind2_clone = toolbox.clone(ind2)
    tools.cxSimulatedBinary(ind1_clone, ind2_clone, ETA)
    child = ind1_clone
    child.energy = 2 * TO_CHILD_ENERGY
    ind1.energy -= TO_CHILD_ENERGY
    ind2.energy -= TO_CHILD_ENERGY
    return child

def get_crossover(name):
    if name == 'one_point':
        return crossover_one_point
    elif name == 'uniform':
        return crossover_uniform
    elif name == 'blend':
        return crossover_blend
    elif name == 'sbx':
        return crossover_sbx
    else:
        raise Exception("Unknown crossover type")

parser = argparse.ArgumentParser()
parser.add_argument('-b')
parser.add_argument('-f')
parser.add_argument('-m')
parser.add_argument('-a')
parser.add_argument('-e')
parser.add_argument('-c')
args = parser.parse_args()

BREED_ENERGY = int(args.b)
FIGHT_ENERGY = int(args.f)
MUTATION_PROB = float(args.m)
CROSSOVER = get_crossover(args.c)
if args.a is not None:
    ALPHA = float(args.a) # used in crossover_blend - between 0 and 1
if args.e is not None:
    ETA = int(args.e) # used in crossover_sbx - between 1 and 20

# not an iRace parameters
STARTING_ENERGY  = 100
TO_CHILD_ENERGY  = 50
POPULATION_SIZE  = 100
DIMENSIONS = 100
NUM_OF_GENERATION = 10000
LOW, HIGH = -6, 6

MIGRATION_ENERGY = 150
MIGRATION_COST = 10
MIGRATION_PROB = 0.01

f = Rastrigin(DIMENSIONS)

'''
FUNCTIONS
'''

def evaluate(individual):
    # individual is a list (gene)
    return f(np.array(individual)),


def mutate(individual, lower_bound=LOW, upper_bound=HIGH, indpb=MUTATION_PROB):
    for i in range(DIMENSIONS):
        if random.random() < indpb:
            individual[i] = random.uniform(lower_bound, upper_bound)
    return individual


def migrate(population):
    for ind in population:
        if (ind.energy >= MIGRATION_ENERGY and random.random() <= MUTATION_PROB):
            new_island = random.choice(g.neighbors(ind.island))
            ind.island = new_island
            ind.energy -= MIGRATION_COST
            recipients = population.copy()
            recipients.remove(ind)
            random.shuffle(recipients)
            for i in range(0, min(MIGRATION_COST, len(recipients))):
                recipients[i].energy += 1
            if MIGRATION_COST > len(recipients):
                recipients[0].energy += MIGRATION_COST - len(recipients)

def interact(ind1, ind2):
    eval_1 = evaluate(ind1)
    eval_2 = evaluate(ind2)
    if eval_1 > eval_2:
        if ind1.energy < FIGHT_ENERGY:
            tmp = ind1.energy
            ind2.energy += tmp
            ind1.energy = 0
        else:
            ind1.energy -= FIGHT_ENERGY
            ind2.energy += FIGHT_ENERGY
    elif eval_1 < eval_2:
        if ind2.energy < FIGHT_ENERGY:
            tmp = ind2.energy
            ind1.energy += tmp
            ind2.energy = 0
        else:
            ind1.energy += FIGHT_ENERGY
            ind2.energy -= FIGHT_ENERGY
    return ind1, ind2


def arrange_meetings(population):
    for island, individuals in itertools.groupby(population, lambda x: x.island):
        individuals = list(individuals)
        #individuals = population
        random.shuffle(individuals)
        for i in range(0, len(individuals) // 2, 2):
            interact(individuals[i], individuals[i + 1])


def wipe_dead(population):
    return list(filter(lambda x: x.energy > 0, population))


def new_generation(population: list):
    for island, individuals in itertools.groupby(population, lambda x: x.island):
        individuals = list(individuals)
        #individuals = population
        good_candidates = list(filter(lambda x: x.energy >= BREED_ENERGY, individuals))
        random.shuffle(good_candidates)
        if len(good_candidates) % 2 != 0:
            good_candidates.pop()
        for i in range(0, len(good_candidates), 2):
            child = toolbox.mate(good_candidates[i], good_candidates[i + 1])
            mutate(child)
            population.append(child)

#def get_genetic_diversity(population):
    

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
creator.create("Individual", list, fitness=creator.FitnessMax, energy=100, island=0)

toolbox = base.Toolbox()

# Register the genetic operators
toolbox.register("attr_float", random.uniform, LOW, HIGH)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=DIMENSIONS)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", CROSSOVER)
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
    migrate(population)
    toolbox.arrange_meetings(population)
    population = toolbox.wipe_dead(population)
    toolbox.new_generation(population)

# Print the best individual found
best_ind = tools.selBest(population, 1)[0]
print(evaluate(best_ind)[0])
#print(best_ind)
#def get_energy_sum(population):
    #tmp = map(lambda x: x.energy, population)
    #s = 0
    #for x in tmp:
        #s += x
    #return s
    
#print(get_energy_sum(population))
