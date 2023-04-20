from jmetal.algorithm.singleobjective.genetic_algorithm import GeneticAlgorithm
from jmetal.operator import BinaryTournamentSelection
from jmetal.operator.crossover import PMXCrossover
from jmetal.operator.mutation import PermutationSwapMutation
from jmetal.problem.singleobjective.tsp import TSP
from jmetal.util.comparator import MultiComparator
from jmetal.util.density_estimator import CrowdingDistance
from jmetal.util.ranking import FastNonDominatedRanking
from jmetal.util.termination_criterion import StoppingByEvaluations

import argparse
import sys

if __name__ == "__main__":
   # print(10)
   # exit()
    


    parser = argparse.ArgumentParser()
    parser.add_argument('-i')
    parser.add_argument('-p')
    parser.add_argument('-o')
    parser.add_argument('-c')
    args = parser.parse_args()
    
    instance = args.i
    population = int(args.p)
    offspring = int(args.o)
    crossover = float(args.c)
    

    problem = TSP(instance)    

    algorithm = GeneticAlgorithm(
        problem=problem,
        population_size=population,
        offspring_population_size=offspring,
        mutation=PermutationSwapMutation(1.0 / problem.number_of_variables()),
        crossover=PMXCrossover(crossover),
        selection=BinaryTournamentSelection(
            MultiComparator([FastNonDominatedRanking.get_comparator(), CrowdingDistance.get_comparator()])
        ),
        termination_criterion=StoppingByEvaluations(max_evaluations=2500000),
    )

    algorithm.run()
    result = algorithm.get_result()
    
    print(result.objectives[0])
