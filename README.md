# Evolutionary Computation - Genetic Algorithms

Implementation of Genetic Algorithms in Python for practical Evolutionary Computation exercises. Solutions developed for three classic optimization problems: 0/1 Knapsack, N-Queens, and Bin Packing. This repository demonstrates in practice the modeling of individuals and the application of fitness, selection, crossover, and mutation functions.

## Addressed Problems

1. **0/1 Knapsack Problem**: Constrained optimization where the goal is to maximize the collected freight by choosing lots for a truck that makes a single trip and carries a maximum of 20 tons.
2. **N-Queens Problem**: Constraint satisfaction problem focused on finding a layout of eight queens on an eight-by-eight board where none attacks another. The individual is modeled as a permutation of the eight rows, eliminating row and column conflicts by construction.
3. **Bin Packing Problem**: Constrained optimization to minimize the number of dispatched boxes. Twelve packages must be distributed in boxes that hold 10 kilograms each, without any exceeding this limit.

## Applied Concepts

- **Individual Modeling**: Different approaches to chromosome representation (binary lists, permutations without repetition, and allocation lists) adapted to the specific rules of each problem.
- **Fitness Function**: Evaluation of solution quality, including counting conflicts for the queens and applying mathematical penalties for loads or boxes that exceed the weight limit.
- **Selection**: Tournament selection method to choose the fittest parents.
- **Genetic Operators**: Customized crossover and mutation algorithms (such as swap for permutations and bit inversion for binary lists) that ensure population evolution while maintaining rule integrity.

## Technologies and Requirements

- **Language**: Python 3.x
- **Libraries**: No external dependencies. Uses only the native `random` library (`randint`, `sample`, `random`).

## How to Run

Clone the repository and run the scripts individually in your terminal.

```bash
git clone https://github.com/YOUR_USER/REPOSITORY_NAME.git
cd REPOSITORY_NAME

# To run the N-Queens problem:
python n-queens.py
```
