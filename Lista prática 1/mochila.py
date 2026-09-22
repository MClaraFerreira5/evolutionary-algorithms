from random import randint
from random import sample
from random import random

class BinPacking:
    def __init__(self):
        self.tamanho_populacao = 20 
        self.tamanho_individuo = 8  
        self.geracoes = 50
        self.populacao = []
        self.taxa_cruzamento = 0.9
        self.taxa_mutacao = 0.15

        self.limite_peso = 20
        self.peso = [5, 3, 2, 8, 9, 4, 6, 9]
        self.frete = [500, 800, 900, 1900, 1700, 1400, 1300, 1300]

        self.torneio = 2 

    def fitness(self, individuo):
        total_peso = sum([peso for i, peso in enumerate(self.peso) if individuo[i]])
        total_frete = sum([frete for i, frete in enumerate(self.frete) if individuo[i]])

        if total_peso <= self.limite_peso:
            return total_frete

        diferenca = total_peso - self.limite_peso
        penalidade = total_frete * diferenca

        return total_frete - penalidade

    def criar_populacao(self):
        self.populacao = []
        for _ in range(self.tamanho_populacao):
            individuo = []
            for _ in range(self.tamanho_individuo):
                individuo.append(randint(0, 1))
            self.populacao.append(individuo)

    def cruzamento(self, pai, mae):
        corte = randint(2, 6)
        filho1 = pai[:corte] + mae[corte:]
        filho2 = mae[:corte] + pai[corte:]
        return filho1, filho2

    def mutacao(self, individuo):
        for i in range(len(individuo)):
            if random() <= self.taxa_mutacao:
                individuo[i] = 1 - individuo[i]
        return individuo

    def selecao_pais(self):
        candidatos1 = sample(self.populacao, k = self.torneio)
        candidatos2 = sample(self.populacao, k = self.torneio)

        pai = max(candidatos1, key=self.fitness)
        mae = max(candidatos2, key=self.fitness)
        return pai, mae

    def selecao_sobreviventes(self, filhos):
        sobreviventes = self.populacao + filhos
        sobreviventes.sort(key=self.fitness, reverse=True)
        self.populacao = sobreviventes[:self.tamanho_populacao]
        
    def reproducao(self):
        filhos = []
        for _ in range(0, self.tamanho_populacao // 2):
            pai, mae = self.selecao_pais()
            if random() <= self.taxa_cruzamento:
                filho1, filho2 = self.cruzamento(pai, mae)
            else:
                filho1 = pai[:]
                filho2 = mae[:]

            self.mutacao(filho1)
            self.mutacao(filho2)

            filhos.append(filho1)
            filhos.append(filho2)
        return filhos

    def evolucao(self):
        self.criar_populacao()

        for i in range(self.geracoes):
            filhos = self.reproducao()
            self.selecao_sobreviventes(filhos)

        melhor = max(self.populacao, key=self.fitness)
        
        peso_melhor = sum([peso for i, peso in enumerate(self.peso) if melhor[i]])
        frete_melhor = sum([frete for i, frete in enumerate(self.frete) if melhor[i]])
        alvo = 5500
        diferenca_alvo = alvo - frete_melhor
        
        print("\n=== RESULTADO FINAL (MOCHILA 0/1) ===")
        print(f'Carga encontrada: {melhor}')
        print(f'Peso da carga: {peso_melhor} toneladas')
        print(f'Frete arrecadado: R$ {frete_melhor}')
        print(f'Diferença para o alvo: R$ {diferenca_alvo}')

evolucionario = BinPacking()
evolucionario.evolucao()