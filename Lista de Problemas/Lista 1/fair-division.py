from random import randint, random, sample

class fairDivision:
    def __init__(self):
        self.size_population = 30
        self.individual_size = 10
        self.generation = 40
        self.population = [] # 0-filho 1; 1-filho 2;

        self.crossing_rate = 0.9
        self.mutation_rate = 0.2
        self.bens = [31, 10, 20, 19, 4, 3, 6, 25, 14, 8]
        self.tornament = 2

    #? Calculando a diferença entre os bens dos filhos
    def fitness(self, individual):
        child1 = sum(v for i, v in enumerate(self.bens) if individual[i] == 0)
        child2 = sum(v for i, v in enumerate(self.bens) if individual[i] == 1)
        return abs(child1 - child2)

    #? Sorteando se os bens irão pra 0 ou 1
    def iniciate_population(self):
        self.population = []
        for _ in range(self.size_population):
            individual = [randint(0, 1) for _ in range(self.individual_size)]
            self.population.append(individual)

    #? Escolhendo qual gene do pai e mãe vai pros filhos (Uniform Crossover)
    def crossing_over(self, father, mother):
        if random() > self.crossing_rate:
            return father[:], mother[:]
        
        child1, child2 = [], []

        for f_gene, m_gene in zip(father, mother):
            if random() < 0.5:
                child1.append(f_gene)
                child2.append(m_gene)
            else:
                child1.append(m_gene)
                child2.append(f_gene)

        return child1, child2

    #? Tira 1 ou adiciona 1 na mutacao
    def mutation(self, individual):
        mutated = individual[:]
        for i in range(len(mutated)):
            if random() <= self.mutation_rate:
                mutated[i] = 1 - mutated[i]
        return mutated

    #? Seleciona os melhores pais
    def select_parents(self):
        candidate1 = sample(self.population, k = self.tornament)
        candidate2 = sample(self.population, k=self.tornament)

        father = min(candidate1, key=self.fitness)
        mother = min(candidate2, key=self.fitness)

        return mother, father

    #? Junta a populacao com os filhos e ordena por fitness
    def select_survivals(self, children):
        survivals = self.population + children
        survivals.sort(key=self.fitness)
        self.population = survivals[:self.size_population]

    def reproduction(self):
            children = []
            for _ in range(0, self.size_population // 2):
                father, mother = self.select_parents()
                child1 = father[:]
                child2 = mother[:]
    
                self.mutation(child1)
                self.mutation(child2)
    
                children.append(child1)
                children.append(child2)
            return children
    
    def evolution(self):
        self.iniciate_population()

        for i in range(self.generation):
            children = self.reproduction()
            self.select_survivals(children)

            best = min(self.population, key=self.fitness)
            if self.fitness(best) == 0:
                break

        best = min(self.population, key=self.fitness)
        best_fitness = self.fitness(best)

        print(f"Resultado: {best}")
        print(f"Fitness (diferença entre os irmãos): {best_fitness}")

evolucionarios = fairDivision()
evolucionarios.evolution()
