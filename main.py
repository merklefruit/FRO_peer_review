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

'''
  PARAMETERS AND SETS
'''

#intensive care units
m = 6

#generate a random list wich contains the number of beds equipped with a ventilator per units
a = random.sample(range(10, 25), m)
print(f"beds with ventilator in each care unit: \t {a}")

b = []
for h in range(0, m): #I'm now randomly creating the number of beds already occupied in each unit
    s = random.randint(0, a[h])
    b.append(s)
print(f"occupied beds in each care unit: \t\t\t {b}")

#new intensive care cases of today
n = 4

#let's create the subset of intensive care units that can be reached in a feasible time
R = [[0, 1, 3, 4, 5], 
     [0, 1, 2, 3, 4],  #every row is one of the 4 new cases
     [1, 2, 5], 
     [2, 4, 5]]


## Solution

#we create an optimization model
model = mip.Model()


''''
  VARIABLES
  Indicate the indices and their range, the meaning of the variables and their nature (binary, integer...):
'''

bj= [model.add_var(var_type=mip.INTEGER) for i in range(m)]
#bj = model.add_var(var_type=mip.INTEGER) #we create a variable wich contain the number of bed occupied and set it as "b" at the beginning of the day
bj = b

# new patients and in which care units they can go
i = [[1, 1, 0, 1, 1, 1],
     [1, 1, 1, 1, 1, 0],
     [0, 1, 1, 0, 0, 1],
     [0, 0, 1, 0, 1, 1]
    ]


x = [[model.add_var(var_type=mip.BINARY) for i in range(m)] for i in range(n)]
d = model.add_var(var_type=mip.INTEGER)

# auxiliary variable for minimization
model.add_constr(d >= 0)
model.add_constr(d <= min(bj))



'''
  CONSTRAINTS
'''

# patient assignment constraints:
# max of n cases can be placed 
# model.add_constr(sum(bj) - sum(b) <= n)

#Intensive unit “capacity” constraints:
model.add_constr(b[0] + mip.xsum([row[0] for row in x]) <= a[0])
model.add_constr(b[1] + mip.xsum([row[1] for row in x]) <= a[1])
model.add_constr(b[2] + mip.xsum([row[2] for row in x]) <= a[2])
model.add_constr(b[3] + mip.xsum([row[3] for row in x]) <= a[3])
model.add_constr(b[4] + mip.xsum([row[4] for row in x]) <= a[4])
model.add_constr(b[5] + mip.xsum([row[5] for row in x]) <= a[5])

# other constraints:
# patients can only occupy one bed
model.add_constr(mip.xsum(x[0]) == 1)
model.add_constr(mip.xsum(x[1]) == 1)
model.add_constr(mip.xsum(x[2]) == 1)
model.add_constr(mip.xsum(x[3]) == 1)

# patients can only stay in the feasable care units
model.add_constr(mip.xsum(i[0][s] * x[0][s] for s in range(m)) == 1)
model.add_constr(mip.xsum(i[1][s] * x[1][s] for s in range(m)) == 1)
model.add_constr(mip.xsum(i[2][s] * x[2][s] for s in range(m)) == 1)
model.add_constr(mip.xsum(i[3][s] * x[3][s] for s in range(m)) == 1)



'''
  OBJECTIVE
'''

#maximize the minimum difference between the available beds (aj) and the free ones (aj-bj) over all intensivecare units j

#minimum difference: min(aj-(aj-bj))= min(bj)
model.objective = mip.maximize(d)



model.optimize()

print("Optimal Solution:")
for g in range(n):
    for s in range(m):
      print(int(x[g][s].x), end='  ')
    print("\t")

print("\nd: ",d.x)
