from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram

# Step 1: Define number of qubits
n = 3  

# Step 2: Create circuit
qc = QuantumCircuit(n, n)

# Step 3: Put all qubits into superposition
qc.h(range(n))

# Step 4: Define Oracle for |101>
oracle = QuantumCircuit(n)
oracle.cz(0, 2)   # Flip phase when qubit 0 = 1 and qubit 2 = 1
oracle.x(1)
oracle.h(2)
oracle.ccx(0, 1, 2)
oracle.h(2)
oracle.x(1)
oracle.cz(0, 2)   # Oracle done

# Step 5: Diffusion Operator
from qiskit.circuit.library import MCXGate

diffuser = QuantumCircuit(n)
diffuser.h(range(n))
diffuser.x(range(n))
diffuser.h(n-1)
diffuser.append(MCXGate(n-1), list(range(n)))
diffuser.h(n-1)
diffuser.x(range(n))
diffuser.h(range(n))


# Step 6: Apply Grover iteration (oracle + diffuser)
qc.append(oracle.to_gate(), range(n))
qc.append(diffuser.to_gate(), range(n))

# Step 7: Measure
qc.measure(range(n), range(n))

# Step 8: Run on simulator
sim = Aer.get_backend('qasm_simulator')
compiled = transpile(qc, sim)
result = sim.run(compiled, shots=1024).result()
counts = result.get_counts()

print("Result distribution:", counts)
plot_histogram(counts).show()
