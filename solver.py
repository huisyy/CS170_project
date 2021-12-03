from numpy.core.fromnumeric import choose
from parse import read_input_file, write_output_file
import os
import math
import numpy as np
import helperFunctions as hF

# solves
def solve(tasks):
    """
    Args:
        tasks [list of task Objects]: list[Task], list of igloos to polish 
    Returns:
        output: list of igloos in order of polishing  
    """
    # initializes global task ID to object dictionary
    hF.initIDToObject(tasks)
    
    finalProfit, taskList = helper(0, tasks, [], 0)

    return [task.task_id for task in taskList]

# helper
def helper(currTime, potentialTasks, currTasks, currProfit):
    """
    Args:
        currTime[int] 
        potentialTasks[list of task objects]
        currTasks[list of task objects]
        currProfit[integer]
    Returns:
        final profit, list of task objects  
    """
    if currTime == 1440:
        return currProfit, currTasks
    idToProb = scorer(currTime, potentialTasks)
    #chooseTasks returns a dictionary of ids to probabilities
    potentialTasks = hF.chooseTasks(idToProb)
    if not potentialTasks: # if no potential tasks are available
        return currProfit, currTasks
    
    maxProfit = -math.inf
    chosenTasks = None
    #chooseTasks returns a dictionary of ids to probabilities
    for potentialTask in potentialTasks:
        tasks_copy = tasks.copy()
        tasks_copy.remove(potentialTask) 
        potentialTaskProfit = hF.decayCalculator(potentialTask.perfect_benefit, potentialTask.duration + currTime - potentialTask.deadline)
        newProfit, newTasks = helper(currTime + potentialTask.duration, tasks_copy, currTasks + [potentialTask], currProfit + potentialTaskProfit)
        if newProfit > maxProfit:
            maxProfit = newProfit
            chosenTasks = newTasks

    # returns profit, task
    return maxProfit, currTasks + chosenTasks




#Reupdates the score for every task. Takes in the current time and possible tasks.

def by_value(item):
    return item[1]


def scorer(time, tasks):
    """
    Args:
        time[int]: the current time
        tasks: list of Task objects
    Returns:
        dictionary mapping task IDs to their normalized score   
    """
    scores = {}
    for task in tasks:
        if time + task.duration > 1440:
            continue
        if time + task.duration > task.deadline:
            score = task.perfect_benefit * (math.e ** (-.017*(time + task.duration - task.deadline)))
        else:
            score = task.perfect_benefit
        
        score = (score/task.duration) 
        scores[task.task_id] = score
    
    if not scores: # if there are no possible tasks
        return None
    
    #normalize the vector
    normalized = hF.normalizeVector(scores)
    sortedTasks = sorted(normalized.items(), key=by_value)
    
    return sortedTasks
    

# return a dictionary




# Calculates the profits if tasks are done in this order



# run_folders = ['large', 'medium', 'small']
run_folders = ['small']

if __name__ == '__main__':
    for folder in run_folders:
        # for i in range(1, 301):
        for i in range(1, 2):
            if folder == 'small' and i == 184:
                continue
            output_path = 'outputs/' + folder + '/' + folder + '-' + str(i) + '.out'
            tasks = read_input_file('inputs/' + folder + '/' + folder + '-' + str(i) + '.in')
            output = solve(tasks)
            write_output_file(output_path, output)

