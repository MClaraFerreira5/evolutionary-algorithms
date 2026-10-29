from collections import Counter
import json
import math
import os
import random
from random import sample

class TerritoryDesign:

  def __init__(self, json_filename="q4_territorios.json"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, json_filename)

    with open(json_path, "r", encoding="utf-8") as f:
      data = json.load(f)

    self.bairros = data["bairros"]
    self.size_bairros = len(self.bairros)  
    self.num_equipes = data.get("equipes", 4)
    self.bairros_por_equipe = self.size_bairros // self.num_equipes  

    self.size_population = 100
    self.generation = 150
    self.crossing_rate = 0.9
    self.mutation_rate = 0.3
    self.torneio = 3

    self.base_ind = []
    for equipe in range(self.num_equipes):
      self.base_ind.extend([equipe] * self.bairros_por_equipe)

  def distance(self, bairro1, bairro2):
    x1, y1 = bairro1
    x2, y2 = bairro2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

  def fitness(self, individual):
    custo_total = 0.0
    for i in range(self.size_bairros):
      for j in range(i + 1, self.size_bairros):
        if individual[i] == individual[j]:
          d = self.distance(self.bairros[i], self.bairros[j])
          custo_total += d

    return custo_total

  def iniciate_population(self):
    self.population = []
    for _ in range(self.size_population):
      ind = self.base_ind[:]
      random.shuffle(ind)
      self.population.append(ind)

  def select_parents(self):
    cand1 = random.sample(self.population, k=self.torneio)
    cand2 = random.sample(self.population, k=self.torneio)

    father = min(cand1, key=self.fitness)
    mother = min(cand2, key=self.fitness)
    return father, mother

  def repair(self, child):
    counts = Counter(child)
    excesso = []
    falta = []

    for eq in range(self.num_equipes):
      qtd = counts[eq]
      if qtd > self.bairros_por_equipe:
        excesso.extend([eq] * (qtd - self.bairros_por_equipe))
      elif qtd < self.bairros_por_equipe:
        falta.extend([eq] * (self.bairros_por_equipe - qtd))

    if not falta:
      return child

    random.shuffle(falta)
    repaired = child[:]
    for i in range(self.size_bairros):
      if repaired[i] in excesso:
        excesso.remove(repaired[i])
        repaired[i] = falta.pop()

    return repaired

  def crossing_over(self, father, mother):
    if random.random() > self.crossing_rate:
      return father[:], mother[:]

    child1 = []
    child2 = []
    for i in range(self.size_bairros):
      if random.random() < 0.5:
        child1.append(father[i])
        child2.append(mother[i])
      else:
        child1.append(mother[i])
        child2.append(father[i])

    return self.repair(child1), self.repair(child2)

  def mutation(self, individual):
    mutated = individual[:]
    if random.random() <= self.mutation_rate:

      idx1, idx2 = random.sample(range(self.size_bairros), 2)
      while mutated[idx1] == mutated[idx2]:
        idx1, idx2 = random.sample(range(self.size_bairros), 2)

      mutated[idx1], mutated[idx2] = mutated[idx2], mutated[idx1]

    return mutated

  def select_survivals(self, children):
    survivals = self.population + children
    survivals.sort(key=self.fitness)
    self.population = survivals[: self.size_population]

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

    print(f"Melhor indivíduo (equipes dos bairros): {best_individual}")
    print(f"Distância total intra-equipes (Fitness): {self.fitness(best_individual):.4f}")

    for eq in range(self.num_equipes):
      bairros_eq = [i + 1 for i, val in enumerate(best_individual) if val == eq]
      print(f"Equipe {eq + 1}: {bairros_eq}")


test = TerritoryDesign()
test.evolution()