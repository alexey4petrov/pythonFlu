import solver

class pySolver(solver.cSolver):
	def init(self):
		print "py_init()"
	def step(self):
		print "py_step()"	

a_solver = solver.cSolver()
a_visu = solver.visualizator()
a_solver.solve( a_visu )
print "\n \n \n IN PYTHON \n"
a_pysolver=pySolver()
a_pysolver.solve( a_visu )
