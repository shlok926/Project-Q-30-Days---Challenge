from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

simulator = AerSimulator()
qc = QuantumCircuit(1,1)
qc.h(0)
qc.measure(0,0)

job = simulator.run(qc, shots=1000)
result = job.result()
counts = result.get_counts()

print("Quantum Random Numbers")
print(counts)
