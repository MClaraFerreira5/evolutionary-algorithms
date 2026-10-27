from collections import Counter
import json
import os
from itertools import combinations
from random import choice, randint, random, sample


# Individuo = [1, 5, 3, 1] Tamanho da lista 50 comissoes; indices, horarios.
class GraphColouring:
    def __init__(self, json_filename="q3_comissoes.json"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, json_filename)

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)


        self.comissions = data["professores"]
        self.size_comissions = data.get("comissoes", 50)
        self.max_times = 10
        self.size_population = 250
        self.generation = 400

        self.crossing_rate = 0.9
        self.mutation_rate = 0.2
        self.tournment = 3
        conflitos = set()
        for prof_comissoes in data["professores"]:
            for c1, c2 in combinations(prof_comissoes, 2):
                u, v = min(c1 - 1, c2 - 1), max(c1 - 1, c2 - 1)
                conflitos.add((u, v))

        self.conflitos = list(conflitos)

    def count_conflicts(self, individual):
        conflitos = 0
        for a, b in self.conflitos:
            if individual[a] == individual[b]:
                conflitos += 1
        return conflitos

    def fitness(self, individual):
        times = len(set(individual))
        penalidade = 1000
        conflitos = 0

        for a, b in self.conflitos:
            if individual[a] == individual[b]:
                conflitos += 1

        return(times + (conflitos * penalidade))

    def iniciate_population(self):
        self.population = [
            [randint(1, self.max_times) for _ in range(self.size_comissions)]
            for _ in range(self.size_population)
        ]

    def select_parents(self):
        cand1 = sample(self.population, k=self.tournment)
        cand2 = sample(self.population, k=self.tournment) 

        father = min(cand1, key=self.fitness)
        mother = min(cand2, key=self.fitness)
        return father, mother

    def crossing_over(self, father, mother):
        if random() > self.crossing_rate:
            return father[:], mother[:]

        pt1, pt2 = sorted(sample(range(1, self.size_comissions), 2))

        child1 = father[:pt1] + mother[pt1:pt2] + father[pt2:]
        child2 = mother[:pt1] + father[pt1:pt2] + mother[pt2:]

        return child1, child2

    def mutation(self, individual):
        mutated = individual[:]
        prob_gene = 1.0 / self.size_comissions  

        for i in range(self.size_comissions):
            if random() < prob_gene:
                current_hour = mutated[i]
                available_hours = [h for h in range(1, self.max_times + 1) if h != current_hour]
                mutated[i] = choice(available_hours)

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
        quant_horarios = len(set(best_individual))

        conflitos_finais = self.count_conflicts(best_individual)
        print(f"Melhor indivíduo: {best_individual}")
        print(f"Status: {'VÁLIDA (Sem conflitos)' if conflitos_finais == 0 else 'INVÁLIDA'}")
        print(f"Quantidade de conflitos: {conflitos_finais}")
        print(f"Quantidade de horários: {quant_horarios}")

test = GraphColouring()
test.evolution()
    