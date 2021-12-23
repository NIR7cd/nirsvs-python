import math
import random

def tri(n, width=1):
    '''For now only 0 and positive integers only'''
    digit_string = ""
    while n > 0:
        digit_string = str(n%3) + digit_string
        n = n//3
    if width and len(digit_string) < width:
        padding = "0" * (width - len(digit_string))
        return padding + digit_string
    return digit_string

def insert(i, qutrit, value):
    modulus = 3**qutrit
    back = i % modulus
    front = 3 * (i - back)
    return front + value*modulus + back

def permutation_matrix(permutation_vector):
    matrix = []
    for i in range(3):
        row = [0 for _ in range(3)]
        row[permutation_vector[i]] = 1
        matrix.append(row)
    return matrix

class StateVector:
    def __init__(self, qutrits):
        '''Initialize a circuit with `qubits` qubits'''
        self.n = qutrits
        self.sv = [0+0j for _ in range(3**self.n)]
        self.sv[0] = 1+0j

    def set_state(self, state):
        '''Set the state of the whole system. `state` is an integer.  The system will be
        set to the state where there is a 100% chance of observing the state labeled by
        the trinary representation of `state`.  For example, in a 1 qutrit state vector
        calling set_state(1) would result in a 100% chance of observing |1>'''
        self.sv = [0+0j for _ in range(3**self.n)]
        self.sv[state] = 1+0j

    def single_qutrit_gate(self, qutrit, matrix):
        '''Perform a single qutrit gate defined by the 3x3 unitary matrix `matrix` on
        qutrit `qutrit`'''
        for i in range(3**(self.n - 1)):
            p = insert(i, qutrit, 0)
            q = insert(i, qutrit, 1)
            r = insert(i, qutrit, 2)
            temp = [self.sv[p], self.sv[q], self.sv[r]]
            self.sv[p] = matrix[0][0]*temp[0] + matrix[0][1]*temp[1] + matrix[0][2]*temp[2]
            self.sv[q] = matrix[1][0]*temp[0] + matrix[1][1]*temp[1] + matrix[1][2]*temp[2]
            self.sv[r] = matrix[2][0]*temp[0] + matrix[2][1]*temp[1] + matrix[2][2]*temp[2]

    def two_qutrit_gate(self, q1, q2, matrix):
        '''Perform a two qutrit gate on the qutrits `q1` and `q2` where the gate is
        defined by the 9x9 unitary matrix `matrix`'''
        for i in range(3**(self.n - 2)):
            qmax = max(q1, q2)
            qmin = min(q1, q2)
            template = insert(insert(i, qmin, 0), qmax, 0)
            p = [0 for _ in range(9)]
            temp = [0 for _ in range(9)]
            for j in range(3):
                for k in range(3):
                    p[3*j + k] = template + j*3**q1 + k*3**q2
                    temp[3*j + k] = self.sv[p[3*j + k]]
            for j in range(9):
                self.sv[p[j]] = 0 + 0j
                for k in range(9):
                    self.sv[p[j]] += matrix[j][k]*temp[k]

    def measure(self, qutrit):
        '''Perform a measurement of `qutrit`, and return the measured value (which will
        be a member of the set {0, 1, 2})''' 
        prob0 = 0
        prob1 = 0
        for i in range(3**(self.n - 1)):
            p = insert(i, qutrit, 0)
            q = insert(i, qutrit, 1)
            prob0 += self.sv[p] * self.sv[p].conjugate()
            prob1 += self.sv[q] * self.sv[q].conjugate()
        prob0 = prob0.real
        prob1 = prob1.real
        prob2 = 1 - prob0 - prob1
        if prob0 == 0 and prob1 == 0:
            return 2
        r = random.random()
        if r < prob0:
            state = 0
            prob = prob0
        elif r < prob0 + prob1:
            state = 1
            prob = prob1
        else:
            state = 2
            prob = prob2
        for i in range(3**(self.n - 1)):
            x = insert(i, qutrit, state)
            y = insert(i, qutrit, (state+1)%3)
            z = insert(i, qutrit, (state+2)%3)
            self.sv[x] *= 1/math.sqrt(prob)
            self.sv[y] = 0 + 0j
            self.sv[z] = 0 + 0j
        return state

    def print_state(self):
        print("State")
        print("-----")
        for i in range(3**self.n):
            print(f"{tri(i, self.n)}: {self.sv[i]}")
        print("-----")

    def print_probs(self):
        print("Probabilities")
        print("-------------")
        for i in range(3**self.n):
            prob = self.sv[i] * self.sv[i].conjugate()
            print(f"{tri(i, self.n)}: {prob.real}")
        print("-------------")

    def permute(self, qutrit, vec):
        '''Given a permutation vector swap the probability amplitudes of the states
        |0>, |1>, and |2>.  For example if vec is [1, 2, 0] and the qutrit's initial state
        is alpha|0> + beta|1> + gamma|2> then the resulting state will be
        beta|0> + gamma|1> + alpha|2>'''
        matrix = permutation_matrix(vec)
        self.single_qutrit_gate(qutrit, matrix)

    def rx(self, qutrit, theta):
        '''Perform a rotation in the 3D space spanned by |0>, |1>, and |2>.
        Axis of rotation is the |0> axis.  This is not a rotation on a Bloch spehere.

        Matrix:

        1 0           0
        0 cos(theta) -sin(theta)
        0 sin(theta)  cos(theta)
        '''
        matrix = [
            [1, 0, 0],
            [0, math.cos(theta), -math.sin(theta)],
            [0, math.sin(theta),  math.cos(theta)]
        ]
        self.single_qutrit_gate(qutrit, matrix)

    def ry(self, qutrit, theta):
        '''Perform a rotation in the 3D space spanned by |0>, |1>, and |2>.
        Axis of rotation is the |1> axis.  This is not a rotation on a Bloch spehere.

        Matrix:

         cos(theta)  0 sin(theta)
         0           1 0
        -sin(theta)  0 cos(theta)
        '''
        matrix = [
            [math.cos(theta), 0, math.sin(theta)],
            [0, 1, 0],
            [-math.sin(theta), 0, math.cos(theta)]
        ]
        self.single_qutrit_gate(qutrit, matrix)

    def rz(self, qutrit, theta):
        '''Perform a rotation in the 3D space spanned by |0>, |1>, and |2>.
        Axis of rotation is the |1> axis.  This is not a rotation on a Bloch spehere.

        Matrix:

        cos(theta) -sin(theta) 0
        sin(theta)  cos(theta) 0
        0           0          1
        '''
        matrix = [
            [math.cos(theta), -math.sin(theta), 0],
            [math.sin(theta), math.cos(theta), 0],
            [0, 0, 1]
        ]
        self.single_qutrit_gate(qutrit, matrix)

    def phase(self, qutrit, theta, phi):
        '''Introduce a relative phase of theta between |0> and |1> and a relative phase
        of phi between |0> and |2>
        '''
        matrix = [
            [1, 0, 0],
            [0, math.cos(theta) + 1j*math.sin(theta), 0],
            [0, 0, math.cos(phi) + 1j*math.sin(phi)]
        ]
        self.single_qutrit_gate(qutrit, matrix)

    def cpermute(self, q0, q1, pv0, pv1, pv2):
        '''Controlled permute - perform a permutation using one of pv1, pv2, pv3 as the
        permutation vector.  If the qubit is in state |0> use pv0, |1> use pv1, and |2>
        use pv2'''
        pm0 = permutation_matrix(pv0)
        pm1 = permutation_matrix(pv1)
        pm2 = permutation_matrix(pv2)
        matrix = [[0 for j in range(9)] for i in range(9)]
        for i in range(3):
            for j in range(3):
                matrix[i][j] = pm0[i][j]
                matrix[i+3][j+3] = pm1[i][j]
                matrix[i+6][j+6] = pm2[i][j]
        self.two_qutrit_gate(q0, q1, matrix)

