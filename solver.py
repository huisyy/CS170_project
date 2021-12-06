import numpy as np
from numpy.core.fromnumeric import choose
from parse import read_input_file, write_output_file
import os
import math
import helperFunctions as hF

END_TIME = 1440
BRANCH_END = 0
NUM_LEVELS_BRANCH = 13
SUM_PROFITS = 0

def solve(tasks):
    """
    Args:
        tasks [list of task Objects]: list[Task], list of igloos to polish 
    Returns:
        output: list of igloos in order of polishing  
    """
    global BRANCH_END, SUM_PROFITS
    BRANCH_END = len(tasks) - NUM_LEVELS_BRANCH
    # initializes global task ID to object dictionary
    hF.initIDToObject(tasks)
    
    finalProfit, chosenTasks = helper(0, tasks)
    print("final Profit!", finalProfit)
    
    # keeping track of avg profit
    SUM_PROFITS += finalProfit
    return [task.task_id for task in chosenTasks]

def helper(currTime, potentialTasks):
    # print("current time", currTime)
    # print("potential tasks", len(potentialTasks))
    if currTime >= END_TIME or len(potentialTasks) == 0:
        return 0, []

    currMaxProfit = -math.inf
    currChosenTasks = None

    if len(potentialTasks) > BRANCH_END:
        best_tasks = getBestTasks(currTime, potentialTasks, 2) # add num of tasks
    else:
        best_tasks = getBestTasks(currTime, potentialTasks)
    # numTasks = max(1, int((1440-currTime)/1440 * 2.5))
    # print(numTasks)
    # best_tasks = getBestTasks(currTime, potentialTasks, numTasks) # add num of tasks

    if not best_tasks:
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

# returns a list of task objects
def getBestTasks(currTime, potentialTasks, numTasks=1):
    scores = []
    for task in potentialTasks:
        if currTime + task.duration > 1440:
            continue
        score = hF.decayCalculator(task.perfect_benefit, currTime + task.duration - task.deadline)
        score = (score/task.duration)
        if task.deadline - currTime == 0:
            deadlineIncentive = 0
        else:
            deadlineIncentive = .8/(task.deadline - currTime)
        score += deadlineIncentive
        task_obj = hF.IDToObject(task.task_id)
        scores.append([task_obj, score])
        
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    # import ipdb;ipdb.set_trace()
    sorted_scores = list(map(lambda x: x[0], sorted_scores))
    if len(sorted_scores) < 1:
        return []
    return sorted_scores[:min(len(sorted_scores), numTasks)]





def main(folder, start_idx, end_idx):
    for i in range(start_idx, min(300, end_idx) + 1):
        if folder == 'small' and i == 184:
            continue
        output_path = 'outputs/' + folder + '/' + folder + '-' + str(i) + '.out'
        tasks = read_input_file('inputs/' + folder + '/' + folder + '-' + str(i) + '.in')
        output = solve(tasks)
        write_output_file(output_path, output)
        
    print("avg profit", SUM_PROFITS/899)


# run_folders = ['large', 'medium', 'small']
run_folders = ['large']

if __name__ == '__main__':
    folder = sys.argv[1]
    start_idx = sys.argv[2]
    end_idx = sys.argv[3]
    main(folder, start_idx, end_idx)
            

