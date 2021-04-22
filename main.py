''''
Peer review es.1
In the regional health care system there are m intensive care units. In each unit j there are aj beds equipped with a ventilator. Currently, bj of those beds are occupied.

In a given day n new infected patients must be hospitalized in intensive care units. For each patient i we denote by Ri⊆{1, . . . , m} the subset of intensive care units that can be reached in a feasible time.

The control room of the emergency calls must assign patients to intensive care units trying to balance the load.

The objective is to maximize the minimum difference between the available beds (aj) and the free ones over all intensive care units j.

Formulate the patient assignment problem with a linear optimization model.
'''

import mip
import random


#   @@@@@ PARAMETERS AND SETS @@@@@
# for the sake of this solution with Python, I am going to generate random data to test my algorithm consistently.

# intensive care units
m = 6

# random list with the number of beds equipped with a ventilator per unit
a = random.sample(range(10, 25), m)
print(f"beds with ventilator in each care unit: \t {a}")

# randomly creating the number of beds already occupied in each unit
b = []
for h in range(0, m): 
    s = random.randint(0, a[h])
    b.append(s)
print(f"occupied beds in each care unit: \t\t\t {b} \n")

# new intensive care cases for today
n = 4

# the subset of intensive care units that can be reached in a feasible time
# (every row is one of the 4 new cases)
R = [[0, 1, 3, 4, 5], 
     [0, 1, 2, 3, 4],  
     [1, 2, 5], 
     [2, 4, 5]]

# new patients and in which care units they can go.
# this is a rappresentation of the matrix R with binary classes.
t = [y for y in range(0, m)]
i = [[1 if t[j] in r else 0 for j in range(m)] for r in R]


# create the optimization model
model = mip.Model()


#   @@@@@ VARIABLES @@@@@
# indicate the indices and their range, the meaning of the variables and their nature (binary, integer...):

# create a variable wich contains the number of beds occupied and set it as "b" at the beginning of the day
bj= [model.add_var(var_type=mip.INTEGER) for i in range(m)]
bj = b

# variable that holds an array for every patient containing the bed where he has been placed (from 1 to m units possible).
x = [[model.add_var(var_type=mip.BINARY) for i in range(m)] for i in range(n)]

# create a support auxiliary variable to complete the min-max objective
d = model.add_var(var_type=mip.INTEGER)


#   @@@@@ CONSTRAINTS @@@@@

# intensive unit “capacity” constraints:
model.add_constr(b[0] + mip.xsum([row[0] for row in x]) <= a[0])
model.add_constr(b[1] + mip.xsum([row[1] for row in x]) <= a[1])
model.add_constr(b[2] + mip.xsum([row[2] for row in x]) <= a[2])
model.add_constr(b[3] + mip.xsum([row[3] for row in x]) <= a[3])
model.add_constr(b[4] + mip.xsum([row[4] for row in x]) <= a[4])
model.add_constr(b[5] + mip.xsum([row[5] for row in x]) <= a[5])

# patients can only stay in the feasable care units
model.add_constr(mip.xsum(i[0][s] * x[0][s] for s in range(m)) == 1)
model.add_constr(mip.xsum(i[1][s] * x[1][s] for s in range(m)) == 1)
model.add_constr(mip.xsum(i[2][s] * x[2][s] for s in range(m)) == 1)
model.add_constr(mip.xsum(i[3][s] * x[3][s] for s in range(m)) == 1)

# other constraints:
# patients can only occupy one bed
model.add_constr(mip.xsum(x[0]) == 1)
model.add_constr(mip.xsum(x[1]) == 1)
model.add_constr(mip.xsum(x[2]) == 1)
model.add_constr(mip.xsum(x[3]) == 1)

# auxiliary minimization variable constraints
model.add_constr(d >= 0)
model.add_constr(d <= min(bj))


#   @@@@@ OBJECTIVE FUNCTION @@@@@
# maximize the minimum difference between the available beds (aj) and the free ones (aj-bj) over all intensivecare units j

# minimum difference: min(aj-(aj-bj))= min(bj)
# using the auxiliary optimization variable "d" defined above
model.objective = mip.maximize(d)

# solve the optimization
model.optimize()


#   @@@@@ RESULTS @@@@@

print("Solution Found:")
for g in range(n):
    for s in range(m):
      print(int(x[g][s].x), end='  ')      
    print("\t")
print("\nd: ",d.x, "\n")