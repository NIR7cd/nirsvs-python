import math
import random

epsilon = 0.000001
max_qubits = 30

def insert(n, bit, place):
    '''Interpreting n as a string of 1s and 0s, insert bit (which should be 1
    or 0) at index place in that string.

    Example:

    insert(4, 1, 1) -> 10

    or to clarify in binary

    insert(100, 1, 1) -> 1010
    '''
    if not (bit == 0 or bit == 1):
        raise ValueError("`bit` must be 0 or 1")
    mask = 2**place - 1
    back = n & mask
    front = n & (~mask)
    return back + bit * 2**place + (front << 1)

def unitary(matrix):
    # TODO actually implement
    return True

class StateVector:
    def __init__(self, qubits):
        '''Initialize a circuit with `qubits` qubits'''
        if qubits > max_qubits:
            raise ValueError(f"Too many qubits; qubits must be <= {max_qubits}")
        self.n = qubits
        self.state_vector = [0+0j for _ in range(2**self.n)]
        self.state_vector[0] = 1+0j

    def set_state(self, state):
        self.state_vector = [0+0j for _ in range(2**self.n)]
        self.state_vector[state] = 1+0j

    def single_qubit_gate(self, qubit, matrix):
        if not unitary(matrix):
            raise ValueError("Matrix is not unitary")
        for i in range(2**(self.n - 1)):
            p = insert(i, 0, qubit)
            q = insert(i, 1, qubit)
            old0 = self.state_vector[p]
            old1 = self.state_vector[q]
            self.state_vector[p] = matrix[0][0]*old0 + matrix[0][1]*old1
            self.state_vector[q] = matrix[1][0]*old0 + matrix[1][1]*old1

    def two_qubit_gate(self, q0, q1, matrix):
        if not unitary(matrix):
            raise ValueError("Matrix is not unitary")
        for i in range(2**(self.n - 2)):
            template = insert(insert(i, 0, min(q0, q1)), 0, max(q0, q1))
            p0 = template
            p1 = template + 2**q1
            p2 = template + 2**q0
            p3 = template + 2**q0 + 2**q1
            old = [self.state_vector[j] for j in (p0, p1, p2, p3)]
            self.state_vector[p0] = matrix[0][0]*old[0] + matrix[0][1]*old[1] + matrix[0][2]*old[2] + matrix[0][3]*old[3]
            self.state_vector[p1] = matrix[1][0]*old[0] + matrix[1][1]*old[1] + matrix[1][2]*old[2] + matrix[1][3]*old[3]
            self.state_vector[p2] = matrix[2][0]*old[0] + matrix[2][1]*old[1] + matrix[2][2]*old[2] + matrix[2][3]*old[3]
            self.state_vector[p3] = matrix[3][0]*old[0] + matrix[3][1]*old[1] + matrix[3][2]*old[2] + matrix[3][3]*old[3]

    def x(self, qubit):
        self.single_qubit_gate(qubit, [[0, 1], [1, 0]])

    def y(self, qubit):
        self.single_qubit_gate(qubit, [[0, -1j], [1j, 0]])

    def z(self, qubit):
        self.single_qubit_gate(qubit, [[1, 0], [0, -1]])

    def h(self, qubit):
        self.single_qubit_gate(qubit, [[1/math.sqrt(2), 1/math.sqrt(2)], [1/math.sqrt(2), -1/math.sqrt(2)]])

    def rot(self, qubit, theta):
        matrix = [
            [math.cos(theta), -math.sin(theta)],
            [math.sin(theta),  math.cos(theta)],
        ]
        self.single_qubit_gate(qubit, matrix)

    def cnot(self, q0, q1):
        matrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0],
        ]
        self.two_qubit_gate(q0, q1, matrix)

    def write(self, qubit, value):
        if not (value == 0 or value == 1):
            raise ValueError("value must be 0 or 1")
        state = self.measure(qubit)
        if state != value:
            self.x(qubit)

    def measure(self, qubit):
        prob0 = 0
        for i in range(2**(self.n-1)):
            p = insert(i, 0, qubit)
            prob0 += self.state_vector[p] * self.state_vector[p].conjugate()
        prob0 = prob0.real
        if prob0 == 0.:
            return 1
        r = random.random()
        state = 0 if r <= prob0 else 1
        for i in range(2**(self.n-1)):
            p = insert(i, 1-state, qubit)
            q = insert(i, state, qubit)
            self.state_vector[p] = 0+0j
            self.state_vector[q] *= math.sqrt(1/prob0)
        return state

    def print_state(self):
        format_string = "{:0%db}:" % self.n
        print("-")
        print("State")
        for i in range(2**self.n):
            print(format_string.format(i), self.state_vector[i])
        print("-")

    def get_probs(self):
        return [self.state_vector[i]*self.state_vector[i].conjugate() for i in range(2**self.n)]

    def print_probs(self):
        format_string = "{:0%db}:" % self.n
        print("-")
        print("Probabilities")
        for i in range(2**self.n):
            z = self.state_vector[i]
            print(format_string.format(i), (z * z.conjugate()).real)
        print("-")
