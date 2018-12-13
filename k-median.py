import sys
import copy
import numpy as np

#no fractional weight is supported
unit = 1

#parameters

cij_file=open("weight.txt","r")
facility_file=open("facility.txt","r")

D=[]
F=[]

#From this file we at first read four values (number of facilities, number of cients, k, epsilon)
line = cij_file.readline()
line = line.strip()
line = line.split()
number_of_facilities = int(line[0])
number_of_clients = int(line[1])
k = int(line[2])
eps = float(line[3])


cij={}
for line in cij_file:
	line=line.strip()
	line=line.split()
	cij[(int(line[0]),int(line[1]))]=float(line[-1])
	if int(line[1])not in D:
		D.append(int(line[1]))

#From this file we read the distance between a pair of facilities
fij = {}
for line in facility_file:
	line=line.strip()
	line=line.split()
	fij[(int(line[0]),int(line[1]))] = float(line[-1])
	fij[(int(line[1]),int(line[0]))] = float(line[-1])


"""
This function checks if it is at all possible to increase vj
"""
def check_vj_first_constraint(cij_res, j, F, T, S):
    #is_first_constraint_violated
    #we have to check if j has become a neighbor of any facility whose cost is exhausted
    #those facilities are stored in T
    #in that case we can not increase vj
    for i in F:
        if cij_res[(i,j)] == 0:
            if i in T:
                S[j] = 0
                #cij_res.pop((i,j))
                return -1
    return 1

"""
This function checks the second constraint and keeps track of which facilities are full. 
If a facility is full then it disconnects all the neighbors connected to the facility. 
"""
def check_vj_second_constraint(cij_res, fi_res, T, S):
    #is_first_constraint_violated
    #we have to check if j has become a neighbor of any facility whose cost is exhausted
    #those facilities are stored in T
    #in that case we can not increase vj
    # is the second constraint violated
    flag = 0
    for key in fi_res:
        # taking action for the second constraint
        if fi_res[key] == 0.0:
            T.append(key)
            for j in S:
                if cij_res[(key, j)] == 0.0:
                    S[j] = 0
    for element in T:
        fi_res.pop(element, None)

"""
This function increases vj
"""
def increase_vj(cij_res, fi_res, j, F, w, v):
    #to every facility connected to vj
    for i in F:
        #if we can spend 1 travel cost we would and reduce cij_res values
        v.setdefault(j, 0)
        if cij_res[(i, j)] > 0:
            cij_res[(i, j)]-=unit
        #if we cannot then we check if it is possible to add facility cost
        else:
            fi_res[i]-=unit
            w.setdefault((i,j), 0)
            w[(i,j)]+= 1
    v.setdefault(j, 0)
    v[j]+=1

"""
F is the list of facilities
fi is the dictionary of cost of facilities 
"""
def facility_problem(cij,fi,D,F):
    cij_res = copy.deepcopy(cij)
    fi_res = copy.deepcopy(fi)
    S = {}
    for client in D:
        S[client] = 1
    v = {}
    w = {}
    T = []

    while True:
        for j in S.keys():
            if S[j] == 1:
                if check_vj_first_constraint(cij_res, j, F, T, S) == 1:
                    check_vj_second_constraint(cij_res, fi_res, T, S)
                    if S[j] == 1:
                        increase_vj(cij_res, fi_res, j, F, w, v)

        if all(value == 0 for value in S.values()) == True:
            break
    #print T
    T1 = []
    while len(T) > 0:
        curr = T[0]
        T1.append(T[0])
        del T[0]
        for j in D:
            if (curr, j) in w and w[(curr, j)] > 0:
                for h in F:
                    if h == curr:
                        continue
                    if (h, j) in w and h in T:
                        T.remove(h)
    return T1, v, w

def run_facility(lambda_value):
    fi = {}
    F = []
    for facility in np.arange(number_of_facilities):
        fi[facility + 1] = lambda_value
        F.append(facility + 1)
    T1, v, w =  facility_problem(cij, fi, D, F)
    return T1, v, w


cmin = min(cij.values())
lambda_upper = sum(cij.values())
lambda_lower = 0
k_uppper = len(run_facility(lambda_upper))
k_lower = len(run_facility(lambda_lower))

combine_solution = 0 #if we need to combine two solutions

while True:
    lambda_middle = (lambda_lower + lambda_upper)/2
    facility_list, v, w = run_facility(int(lambda_middle))
    val = len(facility_list)
    if val == k:
        print "Best Case: Found " + str(k) + " sets without combining solutions"
        print "---------------------------------------------------"
        print "facility list -> " + str(facility_list)
        break
    elif val > k:
        lambda_lower = lambda_middle
    else:
        lambda_upper = lambda_middle

    if lambda_upper - lambda_lower <= (cmin * eps / number_of_facilities):
        combine_solution = 1
        break

if combine_solution == 1:
    print "could not find k sets by bisection search and we have to combine solutions S1 and S2"
    print "------------------------------------------------------------------------------------"
    S1, v1, w1 = run_facility(int(lambda_lower))
    S2, v2, w2 = run_facility(int(lambda_upper))

    alpha1 = (1.0 * k - len(S2)) / (len(S1) - len(S2))
    alpha2 = (len(S1) - k * 1.0) / (len(S1) - len(S2))

    v = {}
    w = {}
    for key in v1:
        v.setdefault(key, v1[key] * alpha1 + v2[key] * alpha2)

    for key in cij:
        w1val = 0
        w2val = 0
        if key in w1:
            w1val = w1[key]

        if key in w2:
            w2val = w2[key]

        w.setdefault(key, (w1val * alpha1 + w2val * alpha2))

    if alpha1 >= 0.5:
        print "facility list -> " + str(S2)
    else:
        closest_set = set()
        for i in S2:
            min = float('inf')
            closest = -1
            for j in S1:
                if fij[(i,j)] < min:
                    min = fij[(i,j)]
                    closest = j
            closest_set.add(closest)

        if len(closest_set) < len(S2):
            for i in S1:
                if len(closest_set)<len(S2):
                    closest_set.add(i)
        residual = set(S1) - closest_set
        for item in residual:
            if len(S2) < k:
                S2.append(item)
        print "facility list -> " + str(S2)
