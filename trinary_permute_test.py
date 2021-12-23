from trinary import StateVector as tsv

sv = tsv(1)
sv.print_state()
sv.permutate(0, [1,0,2])
sv.print_state()
sv.mix(0)
sv.print_state()
sv.print_probs()
