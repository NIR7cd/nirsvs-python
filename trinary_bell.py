from trinary import StateVector as tsv
from trinary import tri
import math

shots = 100

def circuit(sv):
    '''Put qutrit 0 in a mixed state and then entangle it with qutrit 1'''
    sv.rz(0, math.pi/4)
    sv.rx(0, math.pi/4)
    sv.cpermute(0, 1, [0,1,2], [1, 2, 0], [2, 0, 1])

sv = tsv(2)
circuit(sv)
sv.print_state()
sv.print_probs()

shot_counts = {tri(i, width=2):0 for i in range(9)}
for i in range(shots):
    sv.set_state(0)
    circuit(sv)
    state = ""
    for j in range(2):
        state = str(sv.measure(j)) + state
    shot_counts[state] += 1

print(shot_counts)
