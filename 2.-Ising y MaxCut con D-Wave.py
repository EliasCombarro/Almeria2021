import numpy as np
import dimod
import dwave.inspector

# Especificar los coeficientes del problema que queremos resolver es muy fácil
# Empezaremos con un caso muy sencillo

J = {(0,1):1}

h = {}
model = dimod.BinaryQuadraticModel(h, J, 0.0, dimod.SPIN)

print("El modelo que vamos a resolver es")
print(model)
print()

# Podemos resolver el modelo de forma exacta


from dimod.reference.samplers import ExactSolver
sampler = ExactSolver()
solution = sampler.sample(model)
print("La solucion exacta es")
print(solution)
print()


# O con *simulated annealing* (un método heurístico de optimización para ordenadores clásicos)


sampler = dimod.SimulatedAnnealingSampler()
response = sampler.sample(model, num_reads=10)
print("La solucion con simulated annealing es")
print(response)
print()


# Y, por supuesto, con el ordenador cuántico de D-Wave 

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
sampler = EmbeddingComposite(DWaveSampler())
sampler_name = sampler.properties['child_properties']['chip_id']
print("Estamos usando el ordenador de D-Wave llamado", sampler_name)
response = sampler.sample(model, num_reads=100)
print("La solucion con el quantum annealer de D-Wave es")
print(response)
print()

print()
print()
print()


# Veamos ahora un caso un poco más complicado

J = {(0,1):1,(0,2):1,(1,2):1,(1,3):1,(2,4):1,(3,4):1}
h = {}
model = dimod.BinaryQuadraticModel(h, J, 0.0, dimod.SPIN)
print("El modelo que vamos a resolver es")
print(model)
print()


# Primero lo resolvemos de forma exacta

sampler = ExactSolver()
solution = sampler.sample(model)
print("La solucion exacta es")
print(solution)
print()


# Ahora, con *simulated annealing*

sampler = dimod.SimulatedAnnealingSampler()
response = sampler.sample(model, num_reads=10)
print("La solucion con simulated annealing es")
print(response)
print()


# Finalmente, lo resolvemos nuevamente con el *quantum annealer*


sampler = EmbeddingComposite(DWaveSampler(solver='Advantage_system1.1'))
sampler_name = sampler.properties['child_properties']['chip_id']
print("Estamos usando el ordenador de D-Wave llamado", sampler_name)
response = sampler.sample(model, num_reads=100)
print("La solucion con el quantum annealer de D-Wave es")
print(response)
print()

dwave.inspector.show(response)

