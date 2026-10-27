
class SurveillancePlacement:
    def __init__(self):
        self.size_population = 30
        self.individual_size = 10
        self.generation = 40
        self. population = []

        self.crossing_rate = 0.9
        self.mutation = 0.2
        self.pair = [[1, 2], [2, 3], [3, 4], [5, 6], [6, 7], [7, 8], [9, 10], [1, 5], 
                     [2, 6], [3, 7], [4, 8], [6, 9], [7, 10], [5, 9], [8, 10]]
        self.tornament = 2

        def fitness(self, individual):
            