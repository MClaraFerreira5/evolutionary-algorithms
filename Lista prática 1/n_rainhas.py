from random import randint, sample, random


class Queen:
    def __init__(self):
        self.size_population = 20
        self.individual_size = 8
        self.generation = 30
        self.population = []

        self.atacks = 0
        self.crossing_rate = 0.9
        self.mutation_rate = 0.2
        self.tornament = 2

    def fitness(self, individual):
        atacks = 0
        for i in range(len(individual)):
            for j in range(i + 1, len(individual)):
                if (abs(individual[i] - individual[j])) == (abs(i - j)):
                    atacks += 1

        return atacks

    def iniciate_population(self):
        self.population = []

        lines_possibles = [1, 2, 3, 4, 5, 6, 7, 8]
        for _ in range(self.size_population):   
            individual = sample(lines_possibles, k=self.individual_size)       
            self.population.append(individual)         


    def crossing_over(self, father, mother):
        cut = randint(2,6)

        child1 = father[:cut]

        for number in mother:
            if number not in child1:
                child1.append(number)

        child2 = mother[:cut]

        for number in father:
            if number not in child2:
                child2.append(number)

        return child1, child2

    def mutation(self, individual):
        if random() <= self.crossing_rate:
            pos1, pos2 = sample(range(len(individual)), 2)

            individual[pos1], individual[pos2] = individual[pos2], individual[pos1]

        return individual

    def select_parents(self):
        candidate1 = sample(self.population, k=self.tornament)
        candidate2 = sample(self.population, k=self.tornament)

        father = min(candidate1, key=self.fitness)
        mother = min(candidate2, key=self.fitness)

        return mother, father

    def select_survivals(self, children):
        survivals = self.population + children
        survivals.sort(key=self.fitness)
        self.population = survivals[:self.size_population]

    def reproduction(self):
        children = []
        for _ in range(0, self.size_population // 2):
            father, mother = self.select_parents()
            if random() <= self.crossing_rate:
                child1, child2 = self.crossing_over(father, mother)
            else:
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
                print(f"Solução encontrada na geração {i}!")
                break

        best = min(self.population, key=self.fitness)
        
        print("\n=== FINAL RESULT (N-QUEENS) ===")
        print(f"Posição das 8 rainhas: {best}")
        print(f"Contagem de conflitos: {self.fitness(best)}")
        print("\nTabuleiro:")
        self.draw_table(best)

    def draw_table(self, individual):
        print("\nTabuleiro:")
        for linha in range(1, 9): 
            line_text = ""
            for coluna in range(8):
                if individual[coluna] == linha:
                    line_text += " ♛ " 
                else:
                    if (linha + coluna) % 2 == 0:
                        line_text += " ■ " 
                    else:
                        line_text += " □ " 
            print(line_text)


evolucionario = Queen()
evolucionario.evolution()
        