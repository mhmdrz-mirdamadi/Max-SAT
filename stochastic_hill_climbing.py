from SAT_model import SAT


mySat = SAT()
mySat.read_input('Max-Sat_20_80.txt')

print(mySat.clause_number)
print(mySat.variable_number)
print(mySat.clauses)
