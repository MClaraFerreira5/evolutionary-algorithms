import os
import json
import math
from random import randint, sample
import random

# Individuo = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1] -> 0 = turno manha e 1 = turno da tarde
class MaximunCut:
    def __init__(self, json_filename="q2_turnos.json"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, json_filename)

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.schools = data["escolas"]
        self.size_schools = len(self.schools)

        self.size_population = 80
        self.generation = 100
        self.crossing_rate = 0.9
        self.mutation_rate = 0.2
        self.torneio = 3
        
    def distance(self, school1, school2):
        x1, y1 = school1
        x2, y2 = school2
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def fitness(self, individual):
        congestion = 0.0
        for i in range(self.size_schools):
            for j in range(i + 1, self.size_schools):
                if individual[i] == individual[j]:
                    d = self.distance(self.schools[i], self.schools[j])
                    congestion += 1/d

        return congestion

    def iniciate_population(self):
        self.population = [
            [randint(0, 1) for _ in range(self.size_schools)]
            for _ in range(self.size_population)
        ]

    def select_parents(self):
        cand1 = random.sample(self.population, k=self.torneio)
        cand2 = random.sample(self.population, k=self.torneio) 

        father = min(cand1, key=self.fitness)
        mother = min(cand2, key=self.fitness)
        return father, mother

    def crossing_over(self, father, mother):
        if random.random() > self.crossing_rate:
            return father[:], mother[:]

        child1 = []
        child2 = []
        for i in range(self.size_schools):
            if random.random() < 0.5:
                child1.append(father[i])
                child2.append(mother[i])
            else:
                child1.append(mother[i])
                child2.append(father[i])

        return child1, child2

    def mutation(self, individual):
        mutated = individual[:]
        if random.random() <= self.mutation_rate:
            idx = random.randrange(self.size_schools)
            mutated[idx] = 1 - mutated[idx]

        return mutated

    def select_survivals(self, children):
        survivals = self.population + children
        survivals.sort(key=self.fitness)
        self.population = survivals[:self.size_population]

    def reproduction(self):
        children = []
        for _ in range(self.size_population // 2):
            father, mother = self.select_parents()
            child1, child2 = self.crossing_over(father, mother)
            child1 = self.mutation(child1)
            child2 = self.mutation(child2)
            children.append(child1)
            children.append(child2)

        return children


    def evolution(self):
        self.iniciate_population()
        for _ in range(self.generation):
            children = self.reproduction()
            self.select_survivals(children)

        best_individual = min(self.population, key=self.fitness)

        print(f"Melhor indivíduo (turnos): {best_individual}")
        print(f"Congestionamento total (Fitness): {self.fitness(best_individual):.4f}")

        

test = MaximunCut()
test.evolution()





