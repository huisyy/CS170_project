import numpy as np
import sys
from numpy.core.fromnumeric import choose
from parse import read_input_file, write_output_file
import os
import math
import helperFunctions as hF

END_TIME = 1440
BRANCH_END = 0
NUM_LEVELS_BRANCH = 3 #13
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
        best_tasks = getBestTasks(currTime, potentialTasks, 3) # add num of tasks
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

    #linear combination:
    # decay(perfect_benefit) + perfect_benefit/duration + deadline incentive
    for task in potentialTasks:
        #if there's no way you could complete the task before 1440 minutes
        if currTime + task.duration > 1440:
            continue

        score = .5 * hF.decayCalculator(task.perfect_benefit, currTime + task.duration - task.deadline)
        score += 2 * task.perfect_benefit/task.duration
        #score = 2 * (score/task.duration)
        if task.deadline - currTime == 0:
            deadlineIncentive = 0.1
        else:
            #the farther away your deadline is the less incentive you have
            deadlineIncentive = 47 * (.8/(task.deadline - currTime))
        score += deadlineIncentive
        task_obj = hF.IDToObject(task.task_id)
        scores.append([task_obj, score])
        
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    sorted_scores = list(map(lambda x: x[0], sorted_scores))
    if len(sorted_scores) < 1:
        return []
    return sorted_scores[:min(len(sorted_scores), numTasks)]





def main(folder, start_idx, end_idx):
    # for i in range(start_idx, min(300, end_idx) + 1):
    #     if folder == 'small' and i == 184:
    #         continue
    #     output_path = 'outputs/' + folder + '/' + folder + '-' + str(i) + '.out'
    #     tasks = read_input_file('inputs/' + folder + '/' + folder + '-' + str(i) + '.in')
    #     output = solve(tasks)
    #     write_output_file(output_path, output)
        
    # print("avg profit", SUM_PROFITS/899)
    for folder in ['small', 'medium', 'large']:
        for i in range(1, 301):
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
    main("dummy", 1, 300)
    # folder = sys.argv[1]
    # start_idx = int(sys.argv[2])
    # end_idx = int(sys.argv[3])
    # main(folder, start_idx, end_idx)
            

