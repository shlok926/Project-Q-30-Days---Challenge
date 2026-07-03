from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

simulator = AerSimulator()
qc = QuantumCircuit(1,1)
qc.h(0)
qc.measure(0,0)

job = simulator.run(qc, shots=1000)
result = job.result()
counts = result.get_counts()

zeros = counts.get("0", 0)
ones = counts.get("1", 0)

print("Zeros:", zeros)
print("Ones:", ones)
print("Mean:", np.mean([zeros,ones]))
print("Standard Deviation:", np.std([zeros,ones]))
