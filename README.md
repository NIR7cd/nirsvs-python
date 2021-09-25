# Basic state vector simulator

The purpose of this project is to make a basic implementation of a state vector
simulator in order to help illustrate basic concepts in quantum computation.
Inspecting this code should give a high-level understanding of what gate-based
quantum computers accomplish at an abstract level, and how state vector
simulators work. It has methods to show the full state or probabilities of the
system, which makes it easy to see what each of the gates does.

This software has no external dependencies, the only imports are `math` and
`random`. The reason for this is to avoid obscuring the basic functionality of
the simulator by delegating that work to code in other libraries.
