from collections import Counter
import json
import os
import random
from random import sample


# Indivíduo = lista de tamanho 28 (alunos de 0 a 27)
# Valores de 0 a 3 (4 grupos), com exatamente 7 alunos por grupo.
class GraphPartitioning:

  def __init__(self, json_filename="q5_grupos.json"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, json_filename)

    with open(json_path, "r", encoding="utf-8") as f:
      data = json.load(f)

    self.total_alunos = data.get("alunos", 28)
    self.num_grupos = data.get("grupos", 4)
    self.alunos_por_grupo = self.total_alunos // self.num_grupos  # 7 por grupo

    # Ajusta para 0-indexado caso os alunos venham numerados de 1 a 28 no JSON
    self.amizades = [
        (min(u - 1, v - 1), max(u - 1, v - 1)) for u, v in data["amizades"]
    ]

    self.size_population = 100
    self.generation = 150
    self.crossing_rate = 0.9
    self.mutation_rate = 0.3
    self.torneio = 3

    # Vetor base balanceado: 7 zeros, 7 uns, 7 dois, 7 três
    self.base_ind = []
    for grupo in range(self.num_grupos):
      self.base_ind.extend([grupo] * self.alunos_por_grupo)

  def fitness(self, individual):
    # Minimizar o número de pares de amigos que ficaram em grupos separados
    amigos_separados = 0
    for u, v in self.amizades:
      if individual[u] != individual[v]:
        amigos_separados += 1

    return amigos_separados

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
    # Garante que cada grupo continue com exatamente 7 alunos
    counts = Counter(child)
    excesso = []
    falta = []

    for grp in range(self.num_grupos):
      qtd = counts[grp]
      if qtd > self.alunos_por_grupo:
        excesso.extend([grp] * (qtd - self.alunos_por_grupo))
      elif qtd < self.alunos_por_grupo:
        falta.extend([grp] * (self.alunos_por_grupo - qtd))

    if not falta:
      return child

    random.shuffle(falta)
    repaired = child[:]
    for i in range(self.total_alunos):
      if repaired[i] in excesso:
        excesso.remove(repaired[i])
        repaired[i] = falta.pop()

    return repaired

  def crossing_over(self, father, mother):
    if random.random() > self.crossing_rate:
      return father[:], mother[:]

    child1 = []
    child2 = []
    for i in range(self.total_alunos):
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
      # Swap mutation entre dois alunos de grupos diferentes
      # Mantém os grupos perfeitamente balanceados (7 em cada)
      idx1, idx2 = random.sample(range(self.total_alunos), 2)
      while mutated[idx1] == mutated[idx2]:
        idx1, idx2 = random.sample(range(self.total_alunos), 2)

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
    amigos_separados = self.fitness(best_individual)
    total_amizades = len(self.amizades)
    amigos_juntos = total_amizades - amigos_separados

    print(f"Melhor indivíduo (grupos dos alunos): {best_individual}")
    print(f"Total de pares de amigos separados (Fitness): {amigos_separados}")
    print(f"Total de pares de amigos mantidos juntos: {amigos_juntos} de {total_amizades}")

    # Exibe a composição de cada grupo (alunos numerados de 1 a 28)
    for grp in range(self.num_grupos):
      alunos_grupo = [i + 1 for i, val in enumerate(best_individual) if val == grp]
      print(f"Grupo {grp + 1} ({len(alunos_grupo)} alunos): {alunos_grupo}")


test = GraphPartitioning()
test.evolution()