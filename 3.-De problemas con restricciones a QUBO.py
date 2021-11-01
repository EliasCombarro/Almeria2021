# En este ejemplo vamos a ver cómo definir un problema con restricciones, 
# transformalo en una instancia QUBO y resolverlo con distintos métodos

from dimod import *
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import dwave.inspector

# Creamos un Constrained Quadratic Model

qp = CQM()

# Creamos las variables 

x = Binary("x")
y = Binary("y")
z = Binary("z")

# Añadimos una restricción lineal

qp.add_constraint(x + 2*y + 3*z <= 5)

# Añadimos la función objetivo

qp.set_objective(2*x*y -y - 4*z*y)

# El problema que hemos definido tiene las siguientes propiedades

print("El modelo inicial es")
print("")

print("Variables", qp.variables)
print("Objetivo", qp.objective)
print("Restricciones", qp.constraints)
print("")

# Lo convertimos a QUBO

M = 100 # Constante de penalización para las restricciones

qubo, invert = dimod.cqm_to_bqm(qp, lagrange_multiplier = M)

# El nuevo problema tiene las siguientes propiedades

print("El modelo convertido es")
print("")

print("Variables", qubo.variables)
print("Objetivo, parte lineal", qubo.linear)
print("Objetivo, parte cuadrática", qubo.quadratic)
print("")

# Podemos resolver como hacíamos antes

# De forma exacta

sampler = ExactSolver()
solution = sampler.sample(qubo)
print("La solucion exacta es")
print(solution)
print()

# Podemos convertir las soluciones del problema qubo en soluciones del problema original

# La mejor es

print("La mejor solución es", invert(solution.first.sample))
print("")

# Podemos enumerarlas todas

for s in solution.data():
    print(invert(s.sample),qp.objective.energy(s.sample),qp.check_feasible(s.sample))

print("")
    
# Con simulated annealing

sampler = dimod.SimulatedAnnealingSampler()
solution  = sampler.sample(qubo, num_reads=10)
print("La solucion con simulated annealing es")
print("")

for s in solution.data():
    print(invert(s.sample),qp.objective.energy(s.sample),qp.check_feasible(s.sample))
    
print("")

# Con el ordenador cuántico 

sampler = EmbeddingComposite(DWaveSampler())
solution = sampler.sample(qubo, num_reads=100)

print("La solucion con el quantum annealer es")
print("")

for s in solution.data():
    print(invert(s.sample),qp.objective.energy(s.sample),qp.check_feasible(s.sample), s.num_occurrences)
    
dwave.inspector.show(solution)

