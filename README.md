# Combinatorial optimization - Identical parallel Machine Scheduling

### Some background:
[Combinatorical Optimization for dummies](https://en.wikipedia.org/wiki/Combinatorial_optimization)

[Google's effort on optimization](https://developers.google.com/optimization/introduction/overview)

[Identical Parallel Machine Scheduling](https://scholar.google.co.il/scholar?q=identical+parallel+machine+scheduling&hl=en&as_sdt=0&as_vis=1&oi=scholart)

### Intro to what's done here:
A partition (or an assignment) of (the elements of) a set (of jobs, or items, or vertices) _Y_ into sets _J1, J2, . . . , Jm_ must satisfy _⋃1≤i≤m Ji = Y_  and for any _1≤i1<i2≤m_ , _Ji1 ∩ Ji2 = ∅_ (every element of _Y_ belongs to exactly one subset). For some problems (such as scheduling), the value m is fixed in advance, and for some problems it is not fixed (for example, bin packing). We will use a partition to describe a schedule (without specifying the exact times allocated to the jobs), where _Ji_ is the set of jobs of machine _i_. 
A different way to define a schedule or assignment for the set of jobs _J_
is a function _A : J → {1, 2, . . . , m}_. In this case we let 
_Ji = {j ∈ J|A(j) = i}_. 
The definitions are similar for bin packing etc.

### The Scheduling problem:
##### Scheduling with five types to minimize the makespan.
**Input**: An integer number of (identical) machines _m≥2_. A set of _n_ jobs _J = {1, 2, . . . , n}_,
where every job _j_ has an integer processing time _pj > 0_ and a type _tj ∈ {1, 2, 3, 4, 5}_.

**Goal**: Find a partition of the jobs of to the machines, _J1, J2, . . . , Jm_, such that every subset has jobs of at most three types (for any i there are two values _k1i , k2i ∈ {1, 2, 3, 4, 5}_, such that if _j∈Ji_, then _tj ̸= k1i, k2i)_.




### Solution
I offer here three different heuristics :

1. Local Search (hill climbing/tabu) (_start.py_)
2. Branch and Bound (_branchandbound.py_)
3. Genetic (_genetic.py_)





