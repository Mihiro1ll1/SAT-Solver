# SAT Solver
SAT solver and some related utilities:

- *dpll()* .. SAT solver with DPLL algorithm
- *tseitin()* .. simplest DNF to CNF conversion with Tseitin algorithm
- *qm()* .. any DNF to simplest DNF conversion with Quine-McCluskey algorithm

## Input/Output Format

Logical function written in list of integers. Each number is Boolean variables, and minus represents NOT.

Examples:

- For DNF, `[[1], [-1, -2, 3], [-1, 3]]` represents `A+A'B'C+A'C`
- For CNF, `[[-1, -2 , 4], [1, -4], [2,-4]]` represents `(A'+B'+D)(A+D')(B+D')`

(`'` is NOT)

## Usage

Try:

```
$ pip3 install -r requirements.txt
$ chmod +x satsolver.py
$ ./satsolver.py
```

