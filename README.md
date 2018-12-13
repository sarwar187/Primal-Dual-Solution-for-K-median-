# Primal-Dual-Solution-for-K-median-
This repository contains Primal Dual Solution for the K-median Problem. There are two files that are required: weight.txt and facility.txt. The first line of the first file should contain four parameters separated by spaces: number of facilities, number of clients, k and epsilon. The subsequent lines would containt all the facility client distances in the form of (facility, client, weight) tuples. The values are separated by spaces. All weights, facility id's and client id's in this program are integer values. 

Once the files are ready, simply run the following k-median.py file. For the input configuration given in the sample weight.txt and facility.txt file the output looks like below:

Output:
Best Case: found 3 sets without combining solutions
---------------------------------------------------
facility list -> [4, 6, 5]

if we change the epsilon to a very high value like 10000 in the weights file, it would not be possible to get a specific k at the first shot. We will have to compute two different solutions for two different lambdas and combine them. Then the output will be: 

Could not find k sets by bisection search and we have to combine solutions S1 and S2
------------------------------------------------------------------------------------
facility list -> [5, 1, 2]


