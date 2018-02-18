# SAT solver
**[Python3]** SAT solver with DPLL algorithm implementation

## Abstract
  ### Input  
  Logical Function written in CNF (Conjunctive Normal Form)  
  Example: **[[1,-2],[3,-4,-5],[6]]**  
	It means **(A+B')(C+D'+E')F** (' means NOT).  
	Each number represents a corresponding logical variable.  
	Minus signifies the negation of its logical variable.  
  
  ### Output
  Judgement Result (and return satisfiable pattern if possible)   
  Example: **Satisfiable! [-2, -5, 6]**   
	This result is the output to the above example of Input.  
	In this case, **(A,B,C,D,E,F)=(-,0,-,-,0,1)** is one of
	conditions that make logical function True (- means Don't care).
  
  ### Requirement  
  To use this function, you have to install the **networkx** plugin.  
  `pip3 install networkx`  

  ### Usage
  First, place SAT.py in the same directory as the file in which 
  you want to use this function (let's say driver.py).
  Or, you can make SAT.py be your own module.  
  In driver.py,  
  - import SAT.py `import SAT`
  - call DPLL function `ans = SAT.DPLL(cnf)`
  - then, `ans` is `[False]` (when unsatisfiable) or satisfiable pattern (when satisfiable)



