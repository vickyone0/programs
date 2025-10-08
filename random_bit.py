from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

# Step 1: Create circuit with 3 qubits and 3 classical bits
qc = QuantumCircuit(3, 3)

# Step 2: Apply Hadamard gate on all 3 qubits
qc.h([0, 1, 2])

# Step 3: Measure all qubits
qc.measure([0, 1, 2], [0, 1, 2])

# Step 4: Run simulation
sim = Aer.get_backend('qasm_simulator')
compiled_circuit = transpile(qc, sim)
result = sim.run(compiled_circuit, shots=10).result()

# Step 5: Get counts
counts = result.get_counts()

print("Random 3-bit outputs distribution:", counts)

# Optional: pick one random result
random_bitstring = list(counts.keys())[0]
print("One random 3-bit string:", random_bitstring)
