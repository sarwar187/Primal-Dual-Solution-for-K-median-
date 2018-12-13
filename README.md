# Primal-Dual-Solution-for-K-median-
This repository contains Primal Dual Solution for the K-median Problem. There are two files that are required: weight.txt and facility.txt. The first line of the first file should contain four parameters separated by spaces: number of facilities, number of clients, k and epsilon. The subsequent lines would containt all the facility client distances in the form of (facility, client, weight) tuples. The values are separated by spaces. All weights, facility id's and client id's in this program are integer values. 

Once the files are ready, simply run the following k-median.py file. A sample input configuration and output is given here: 

weight.txt file input 

6 3 3 0.00001
1 1 40
1 2 60
1 3 50
2 1 40
2 2 50
2 3 60
3 1 40
3 2 20
3 3 70
4 1 10
4 2 30
4 3 100
5 1 50
5 2 55
5 3 23
6 1 78
6 2 12
6 3 78

facility.txt file input 
1 1 0
1 2 3
1 3 3
1 4 3
1 5 3
1 6 3
2 2 0
2 3 3
2 4 3
2 5 3
2 6 3
3 3 0
3 4 3
3 5 3
3 6 3
4 4 0
4 5 3
4 6 3
5 5 0
5 6 3
6 6 0

output:
Best Case: Found 3 sets without combining solutions
---------------------------------------------------
facility list -> [4, 6, 5]

if we change the epsilon to a very high value like 10000, it would be be possible to get a specific k at the first shot. Then the output will be: 

could not find k sets by bisection search and we have to combine solutions S1 and S2
------------------------------------------------------------------------------------
facility list -> [5, 1, 2]


