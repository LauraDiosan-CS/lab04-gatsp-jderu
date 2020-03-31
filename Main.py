from collections import defaultdict

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from Chromosome import Chromosome
from GA import GA


def readFile(file):
    f = open(file, "r")
    n = int(f.readline())

    g = nx.MultiDiGraph(weight=0)
    for i in range(n):
        weights = [int(ii) for ii in f.readline().strip().split(',')]
        for j in range(len(weights)):
            g.add_edge(i, j, weight=weights[j])

    return g


file_names = ['easy_01_4', 'easy_02_4', 'easy_01_tsp', 'hard_00_26', 'hard_01_662', 'hard_01_tsp', 'hard_02_52',
              'medium_00_8', 'medium_01_131', 'medium_01_tsp', 'medium_02_237', 'medium_03_379']


def run():
    file_name = file_names[0]
    pop_size = 150
    no_gen = 1000
    generation_type = 'steady'  # normal/elitism/steady

    run_test(file_name, generation_type, pop_size, no_gen)


def modularity(repres, param):
    cost_value = param['mat'][repres[0]][repres[-1]][0]['weight']
    current = repres[0]
    for i in range(1, len(repres)):
        cost_value += param['mat'][current][repres[i]][0]['weight']
        current = repres[i]
    return cost_value


def run_test(file_name, generation_type, pop_size, no_gen):
    G = readFile("inputFiles/" + file_name + ".txt")

    params = {
        'noNodes': G.number_of_nodes(),
        'mat': G,
        'degrees': [x[1] for x in G.degree()],
        'noEdges': G.number_of_edges(),
        'popSize': pop_size,
        'function': modularity,
        'noGen': no_gen,
        'chromosome': Chromosome,
        'maxCommunities': G.number_of_nodes()
    }

    ga = GA(params)
    ga.initialisation()
    ga.evaluation()
    best_chromosome = ga.bestChromosome()
    last_fitness = 0
    same_fitness = 1
    i = 0
    while True:
        best_chromosome = ga.bestChromosome()
        if last_fitness == best_chromosome.fitness:
            if same_fitness == 500:
                break
            else:
                same_fitness += 1
        else:
            same_fitness = 1
            last_fitness = best_chromosome.fitness

        print('Best chromosome of generation:' + str(i + 1) + ' has a fitness of ' + str(best_chromosome.fitness))
        if generation_type == 'normal':
            ga.oneGeneration()
        elif generation_type == 'elitism':
            ga.oneGenerationElitism()
        elif generation_type == 'steady':
            ga.oneGenerationSteadyState()
        i += 1

    writeSolutionToFile(file_name, best_chromosome)
    # draw_result(file_name, best_chromosome, params)


def writeSolutionToFile(file_name, best_chromosome):
    with open('outputFile/' + file_name + '_result.txt', 'w') as fout:
        fout.write('Fitness of best chromosome:' + str(best_chromosome.fitness) + '\n')

        for i in range(len(best_chromosome.repres)):
            fout.write(str(i) + ': ' + str(best_chromosome.repres[i]) + '\n')


def draw_result(file_name, best_chromosome, params):
    A = np.matrix(params['mat'])
    G = nx.from_numpy_matrix(A)
    pos = nx.spring_layout(G)  # compute graph layout
    plt.figure(figsize=(10, 10))  # image is 8 x 8 inches
    nx.draw_networkx_nodes(G, pos, node_size=600, node_color=best_chromosome.repres)
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    plt.savefig('outputFile/' + file_name + '_plot.png')
    plt.clf()


run()
