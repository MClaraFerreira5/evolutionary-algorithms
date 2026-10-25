import json
import math
import os
import random
from itertools import combinations

class MaximumDiversity:
    def __init__(self, json_filename="q1_vacinacao.json"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        json_path = os.path.join(base_dir, json_filename)
        
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        self.k = data.get("pontos_a_escolher", 10)  
        self.locais = data["locais"]               
        self.total_locais = len(self.locais)       
        
        self.size_population = 50
        self.generation = 100
        self.crossing_rate = 0.9
        self.mutation_rate = 0.2
        self.tornament = 3
        
        self.dist_matrix = [[0.0] * self.total_locais for _ in range(self.total_locais)]
        for i in range(self.total_locais):
            for j in range(i + 1, self.total_locais):
                d = math.dist(self.locais[i], self.locais[j])
                self.dist_matrix[i][j] = d
                self.dist_matrix[j][i] = d

    def fitness(self, individual):
        total_dist = 0.0
        for i, j in combinations(individual, 2):
            total_dist += self.dist_matrix[i][j]
        return total_dist

    def iniciate_population(self):
        self.population = [
            random.sample(range(self.total_locais), self.k)
            for _ in range(self.size_population)
        ]

    def select_parents(self):
        cand1 = random.sample(self.population, k=self.tornament)
        cand2 = random.sample(self.population, k=self.tornament)
        
        father = max(cand1, key=self.fitness)
        mother = max(cand2, key=self.fitness)
        return father, mother

    def crossing_over(self, father, mother):
        if random.random() > self.crossing_rate:
            return father[:], mother[:]

        pool = list(set(father + mother))
        
        child1 = random.sample(pool, self.k)
        child2 = random.sample(pool, self.k)
        return child1, child2

    def mutation(self, individual):
        mutated = individual[:]
        if random.random() <= self.mutation_rate:
            disponiveis = list(set(range(self.total_locais)) - set(mutated))
            
            idx_remover = random.randrange(self.k)
            novo_ponto = random.choice(disponiveis)
            
            mutated[idx_remover] = novo_ponto
            
        return mutated

    def select_survivals(self, children):
        survivals = self.population + children
        survivals.sort(key=self.fitness, reverse=True)  
        self.population = survivals[:self.size_population]

    def reproduction(self):
        children = []
        for _ in range(self.size_population // 2):
            father, mother = self.select_parents()
            c1, c2 = self.crossing_over(father, mother)
            
            c1 = self.mutation(c1)
            c2 = self.mutation(c2)
            
            children.append(c1)
            children.append(c2)
        return children

    def evolution(self):
        self.iniciate_population()

        for g in range(self.generation):
            children = self.reproduction()
            self.select_survivals(children)

        best = max(self.population, key=self.fitness)
        best_fitness = self.fitness(best)
        
        print(f"Locais escolhidos (índices 1-indexados): {[idx + 1 for idx in sorted(best)]}")
        print(f"Soma máxima das distâncias: {best_fitness:.2f} km")

teste = MaximumDiversity()
teste.evolution()