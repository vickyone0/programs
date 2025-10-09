from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.circuit.library import MCXGate

n = 9  # 9 qubits = 3x3 Sudoku

# --- Define Sudoku-like constraint ---
def is_valid(bits):
    # Rows not all equal
    for i in range(0, 9, 3):
        row = bits[i:i+3]
        if len(set(row)) == 1:  # all same
            return False
    # Columns not all equal
    for c in range(3):
        col = bits[c::3]
        if len(set(col)) == 1:
            return False
    return True

# --- Find all valid 9-bit states ---
valid_states = []
for i in range(2**n):
    bits = [(i >> j) & 1 for j in range(n-1, -1, -1)]
    if is_valid(bits):
        valid_states.append(''.join(map(str, bits)))

print("Valid Sudoku states:", len(valid_states))

# --- Build circuit ---
qc = QuantumCircuit(n, n)
qc.h(range(n))  # Superposition

# --- Oracle: mark valid states ---
oracle = QuantumCircuit(n, name='oracle')
for s in valid_states:
    zeros = [i for i, bit in enumerate(s) if bit == '0']
    for i in zeros:
        oracle.x(i)
    oracle.h(n-1)
    oracle.append(MCXGate(n-1), list(range(n)))
    oracle.h(n-1)
    for i in zeros:
        oracle.x(i)

# --- Diffuser ---
diffuser = QuantumCircuit(n, name='diffuser')
diffuser.h(range(n))
diffuser.x(range(n))
diffuser.h(n-1)
diffuser.append(MCXGate(n-1), list(range(n)))
diffuser.h(n-1)
diffuser.x(range(n))
diffuser.h(range(n))

# --- One Grover iteration ---
qc.append(oracle.to_gate(), range(n))
qc.append(diffuser.to_gate(), range(n))

qc.measure(range(n), range(n))

# --- Simulate ---
sim = Aer.get_backend('qasm_simulator')
compiled = transpile(qc, sim)
result = sim.run(compiled, shots=512).result()
counts = result.get_counts()

print("\nMeasurement results (top 10):")
for k, v in sorted(counts.items(), key=lambda x: -x[1])[:10]:
    print(f"{k}: {v}")
