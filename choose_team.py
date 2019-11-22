#!/usr/local/bin/python3
#
# choose_team.py : Choose a team of maximum skill under a fixed budget
#
# Code by: Amogh Batwal(abatwal), Anuj Godase(abgodase), Sanket Pandilwar(spandilw)
#
# Based on skeleton code by D. Crandall, September 2019
#
import sys
import time
import queue

def load_people(filename):
    people={}
    with open(filename, "r") as file:
        for line in file:
            l = line.split()
            people[l[0]] = [ float(i) for i in l[1:] ] 
    return people
 
#https://stackoverflow.com/questions/22310474/python-knapsack-branch-and-bound -referred creation of node with given fields from this website
class Node: #created this class node to store multiple values and traced path each time
    def __init__(self, level, skill, rate, bound,items):
         self.level = level
         self.skill = skill
         self.rate = rate
         self.bound = bound
         self.items=items
     
#calculates upper bound for the given node
def bound(node,n,budget,data):
    if (node.rate >= budget): 
        return 0
    skill_bound=node.skill
    level_index=node.level+1
    total_rate=node.rate
    
    while((level_index<n) and (total_rate+data[level_index][1][1] <= budget)):
        total_rate +=data[level_index][1][1]
        skill_bound +=data[level_index][1][0]
        level_index+=1
        
    if(level_index<n):
        skill_bound+=(budget-total_rate) * data[level_index][1][0] / data[level_index][1][1]
        
    return skill_bound
    

#https://www.geeksforgeeks.org/implementation-of-0-1-knapsack-using-branch-and-bound/ - referred the pseudo code of knapsack using bb from geeksforgeeks
#implemented a standard 0/1 knapsack problem with branch and bound method
def approx_solve_branch_and_bound(people, budget):

    data=sorted(people.items(), key=lambda x: x[1][0]/x[1][1], reverse=True) #sorting rates and skills by decreasing order of skill/rate ratio
    solution=()
    n=len(data) #no of people/items
    
    q=queue.Queue() #queue is used for BFS traversal of all the nodes
    u=Node(-1,0.0,0.0,0.0,[]) #initilizing starting point 
    q.put(u); 
    actual_trace=[] # to store the best traversal path which maximizes skills with given budget and rate constraint
    
#   for each node, compute skills of every child of a node in the queue and update maxskills
    maxSkill=0
    while not q.empty():
        u=q.get()   
        v=Node(None,None,None,None,[])      
        v.level=u.level+1
        v.rate=u.rate+data[v.level][1][1] #gives rate correspoding to the name available at given level index
        v.skill=u.skill+data[v.level][1][0]#gives skill correspoding to the name available at given level index
        v.items=list(u.items)
        v.items.append(u.level)
              
        if (v.rate <= budget and v.skill > maxSkill): #if current rate is less than budget and current skill is greater than maxskill then update maxskill
            maxSkill = v.skill 
            actual_trace=v.items #storing traversal of by far the best path which maximizes skill with given budget
            
        v.bound = bound(v, n, budget, data) #calculating upper bound
        if (v.bound > maxSkill) : #if upper_bound in greater then update maxskill and push the node to the queue
            q.put(v)
        
        v = Node(level=None , skill = 0.0, rate = 0.0, bound = 0.0, items=[])
        v.level=u.level+1
        v.rate = u.rate; 
        v.skill = u.skill;
        v.bound = bound(v, n, budget, data)
        v.items=list(u.items)
        if (v.bound > maxSkill):
            q.put(v)
    
#    print(maxSkill)
#    print(actual_trace)
    for index in actual_trace: #adding the group of people which maximizes skills in given budget and rate to the solution tuple
        solution += ( ( data[index+1][0], 1), )
    return solution


if __name__ == "__main__":
    start_time=time.time();
    if(len(sys.argv) != 3):
        raise Exception('Error: expected 2 command line arguments')
    budget = float(sys.argv[2])
    people = load_people(sys.argv[1])
    solution=approx_solve_branch_and_bound(people,budget)
#    print(solution)
    print("Found a group with %d people costing %f with total skill %f" % \
               ( len(solution), sum(people[p][1]*f for p,f in solution), sum(people[p][0]*f for p,f in solution)))
    for s in solution:
        print("%s %d" % s)    
#    print("seconds:", time.time()-start_time)

