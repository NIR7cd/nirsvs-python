import nirsvs

sv = nirsvs.StateVector(2)
print("Initial state:")
sv.print_state()
sv.h(0)
print("H[0]")
sv.print_state()
sv.cnot(0,1)
print("CNOT[0,1]")
sv.print_state()
sv.measure(0)
print("MEASURE[0]")
sv.print_state()
