import numpy as np
from numpy.core.fromnumeric import choose
from parse import read_input_file, write_output_file
import os
import math
import helperFunctions as hF

END_TIME = 1440

def solve(tasks):
    """
    Args:
        tasks [list of task Objects]: list[Task], list of igloos to polish 
    Returns:
        output: list of igloos in order of polishing  
    """
    # initializes global task ID to object dictionary
    hF.initIDToObject(tasks)
    
    finalProfit, chosenTasks = helper(0, tasks)
    print("final Profit!", finalProfit)
    
    return [task.task_id for task in chosenTasks]

def helper(currTime, potentialTasks):
    if currTime >= END_TIME or not potentialTasks:
        return 0, []

    currMaxProfit = -math.inf
    currChosenTasks = None

    # deterministic choice of best task so far (greedy)
    idToProb, best_tasks, best_score = scorer(currTime, potentialTasks)
    # tasks = hF.chooseTasks(idToProb)
    if best_tasks == None:
        return 0, []

    for t in best_tasks:
        newPotentialTasks = get_potential_tasks(t, potentialTasks.copy()) # 
        childTotalProfit, childChosenTasks = helper(currTime + t.duration, newPotentialTasks)
        tTotalProfit = hF.decayCalculator(t.perfect_benefit, currTime + t.duration - t.deadline) + childTotalProfit
        if tTotalProfit > currMaxProfit:
            currMaxProfit = tTotalProfit
            currChosenTasks = [t] + childChosenTasks

    return currMaxProfit, currChosenTasks

# removes task from potentialTasks and returns a new copy
def get_potential_tasks(task, potentialTasks):
    potentialTasksCopy = potentialTasks.copy()
    potentialTasksCopy.remove(task)
    return potentialTasksCopy

def by_value(item):
    return item[1]

#Idea - create multiple scorers and take the max out of all of them
def scorer(time, tasks, numOFTasks=2):
    """
    Args:
        time[int]: the current time
        tasks: list of Task objects
    Returns:
        dictionary mapping task IDs to their normalized score   
    """
    scores = {}
    best_task, best_score, second_best_task, second_score = None, -math.inf, None, -math.inf
    for task in tasks:
        if time + task.duration > 1440:
            continue

        score = hF.decayCalculator(task.perfect_benefit, time + task.duration - task.deadline)
        score = (score/task.duration) 
        scores[task.task_id] = score
    scores = dict(sorted(scores, key=lambda item: item[1]))
        
    if not scores:
        if numOFTasks == 2: # if there are no possible tasks
            return None, [best_task, second_best_task], [best_score, second_score]
        else:
            return None, [best_task], best_score
    
    
    #normalize the vector
    normalized = hF.normalizeVector(scores)
    best_task = scores[0]
    best_score = scores[0][1]
    second_best_task = scores[1]
    second_score = scores[1][0]
    
    return normalized, [best_task, second_best_task], [best_score, second_score]
    






run_folders = ['large', 'medium', 'small']
# run_folders = ['large']

if __name__ == '__main__':
    for folder in run_folders:
        for i in range(1, 301):
        # for i in range(2, 3):
            if folder == 'small' and i == 184:
                continue
            output_path = 'outputs/' + folder + '/' + folder + '-' + str(i) + '.out'
            tasks = read_input_file('inputs/' + folder + '/' + folder + '-' + str(i) + '.in')
            output = solve(tasks)
            write_output_file(output_path, output)

