# SAT solver
**[Python3]** SAT solver with DPLL algorithm implementation

## Abstract
  ### Input  
  Logical Function written in CNF (Conjunctive Normal Form)  
  Example: `[[1,-2],[3,-4,-5],[6]]`  
	It means `(A+B*)(C+D*+E*)F` (* means NOT).  
	Each number represents a corresponding logical variable.  
	Minus signifies the negation of its logical variable.  
  
  ### Output
  Judgement Result  
  Satisfiable pattern (if possible)   
  Example: `Satisfiable! [-2, -5, 6]`   
	This result is the output to the above example of Input.  
	In this case, `(A,B,C,D,E,F)=(-,0,-,-,0,1)` is one of
	conditions that make logical function True (- means Don't care).



