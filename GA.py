from random import randint


class GA:
    def __init__(self, params=None):
        self.__params = params
        self.__population = []

    @property
    def population(self):
        return self.__population

    def initialisation(self):
        for _ in range(0, self.__params['popSize']):
            c = self.__params['chromosome'](self.__params)
            self.__population.append(c)

    def evaluation(self):
        for c in self.__population:
            c.fitness = self.__params['function'](c.repres, self.__params)

    def bestChromosome(self):
        best = self.__population[0]
        for c in self.__population:
            if c.fitness < best.fitness:
                best = c
        return best

    def worstChromosome(self):
        worst = self.__population[0]
        for c in self.__population:
            if c.fitness > worst.fitness:
                worst = c
        return worst

    def selection(self):
        pos1 = randint(0, self.__params['popSize'] - 1)
        pos2 = randint(0, self.__params['popSize'] - 1)
        if self.__population[pos1].fitness < self.__population[pos2].fitness:
            return pos1
        else:
            return pos2

    def oneGeneration(self):
        newPop = []
        for _ in range(self.__params['popSize']):
            p1 = self.__population[self.selection()]
            p2 = self.__population[self.selection()]
            off = p1.crossover(p2)
            off.mutate()
            newPop.append(off)
        self.__population = newPop
        self.evaluation()

    def oneGenerationElitism(self):
        newPop = [self.bestChromosome()]
        for _ in range(self.__params['popSize'] - 1):
            p1 = self.__population[self.selection()]
            p2 = self.__population[self.selection()]
            off = p1.crossover(p2)
            off.mutate()
            newPop.append(off)
        self.__population = newPop
        self.evaluation()

    def oneGenerationSteadyState(self):
        self.__population = sorted(self.__population, key=lambda x: x.fitness)
        for _ in range(self.__params['popSize']):
            p1 = self.__population[self.selection()]
            p2 = self.__population[self.selection()]
            off = p1.crossover(p2)
            off.mutate()
            off.fitness = self.__params['function'](off.repres, self.__params)
            if off.fitness < self.__population[-1].fitness:
                self.__population[-1] = off
        self.evaluation()
