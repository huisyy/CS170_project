import solver as sv
import numpy as np
import math

idToObject = {}

def initIDToObject(tasks):
    global idToObject
    for task in tasks:
        idToObject[task.task_id] = task
    
# returns list of Task objects
def chooseTasks(idToProb):
    if not idToProb:
        return None
    ids = []
    probs = []
    for id, prob in idToProb:
        ids.append(id)
        probs.append(prob)
    # for id in idToProb:
    #     ids.append(id)
    # for prob in idToProb:
    #     probs.append(prob)
    tasks = np.random.choice(ids, len(ids)//4, replace = False, p=probs)

    taskObjects = []
    for id in tasks:
        taskObjects.append(idToObject[id])
    return taskObjects #a list of tasks

def normalizeVector(dict):
    normFactor = 1.0/sum(dict.values())
    for key in dict:
        dict[key] = dict[key]*normFactor

    return dict

def profitCalculator(taskObjects, time=0):
    profit = 0
    # time = 0
    for task in taskObjects:
        #if the task will go over the deadline, profit decays
        if task.duration + time > task.deadline:
            minutesLate = task.duration - task.deadline
            profit += decayCalculator(task.perfect_benefit, minutesLate)
            # print("HITS HERE ", task.task_id)
        else:
            profit += task.perfect_benefit
        time += task.duration
    return profit

def decayCalculator(profit, minutesLate):
    if minutesLate <= 0:
        return profit
    return profit * (math.e ** (-0.0170 * minutesLate))

