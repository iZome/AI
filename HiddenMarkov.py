import numpy as np
import array
from matplotlib import pyplot as plt

rain = np.matrix('0.7 0.3;0.3 0.7')   #matrix with forward for rain form [rain(1 and 2) rain(only 2);rain(only 1) rain(no)]

seeUmbrella = np.matrix('0.9 0.0;0.0 0.2')

noUmbrella = np.matrix('0.1 0.0;0.0 0.8')

forward = [0 for x in range(5)]
forwardWithUmb = [0 for x in range(5)]

backward = [0 for x in range(5)]
backwardWithUmb = [0 for x in range(5)]

forwardBackwardResult = [0 for x in range(6)]

forward0 = [0.5,0.5]
backward5 = [1.0,1.0]


dayControl = -1


def forwardFromLastDay():
    if(dayControl == -1):
        lastDay = [forward0] #get result from last day
    else:
        lastDay = np.array([forwardWithUmb[dayControl]])
    updateDayControl()                              #+1 on day-counting varible
    lastDayFlipped = np.rot90(lastDay,-1)           #rotate vector to the right To do: figure out how last thing works
    toDay = np.dot(rain,lastDayFlipped)             #get chance for rain/not rain based on last day

    forward[dayControl] = np.round(np.rot90(toDay,1),3).tolist()[0]   #add the new probabily to the probability list

def forwardUmbrellaObservation(guardObs):
    obsMatrix = 0                                   #matrix for observation
    toDay = np.array([forward[dayControl]])   #get chance for rain and not rain based on last day
    toDayFlipped = np.rot90(toDay,-1)

    #choose the right matrix based on input
    if(guardObs == 0):
        obsMatrix = noUmbrella
    elif(guardObs == 1):
        obsMatrix = seeUmbrella
    else:
        print("Obs, you can only enter 0 or 1 here, you entered", guardObs, ".")

    withObs = np.dot(obsMatrix, toDayFlipped)       #multiply the guards observation-matrix with the todays rain probs
    withObs = np.power(np.sum(withObs),-1)*withObs

    forwardWithUmb[dayControl] = np.round(np.rot90(withObs,1),3).tolist()[0]

def backwardNextDay(guardObs):
    if(dayControl == 0):
        nextDay = [backward5] #get result from last day
    else:
        nextDay = np.array([backwardWithUmb[5-dayControl]])

    #choose the right matrix based on input
    if(guardObs == 0):
        obsMatrix = noUmbrella
    elif(guardObs == 1):
        obsMatrix = seeUmbrella
    else:
        print("Obs, you can only enter 0 or 1 here, you entered", guardObs, ".")

    nextDayFlipped = np.rot90(nextDay,-1)

    withObs = np.dot(obsMatrix, nextDayFlipped)       #multiply the guards observation-matrix with the todays rain probs
    withObs = np.power(np.sum(withObs),-1)*withObs


    backward[4-dayControl] = np.round(np.rot90(withObs,1),3).tolist()[0]   #add the new probabily to the probability list

def backwardUmbrellaObservation():
    obsMatrix = 0                                   #matrix for observation
    nextDay = np.array([backward[4-dayControl]])   #get chance for rain and not rain based on last day

    nextDayFlipped = np.rot90(nextDay,-1)         #rotate vector to the right To do: figure out how last thing works
    toDay = np.dot(rain,nextDayFlipped)             #get chance for rain/not rain based on last day

    backwardWithUmb[4-dayControl] = np.round(np.rot90(toDay,1),3).tolist()[0]

def forwardBackward():
    for i in range(1,5):
        forward = forwardWithUmb[i-1]
        backward = backwardWithUmb[i]

        forwardBackwardDay = np.multiply(forward,backward)
        forwardBackwardResult[i] = np.round(np.power(np.sum(forwardBackwardDay),-1)*forwardBackwardDay,3).tolist()
    backwardStart = np.multiply(backwardWithUmb[0],forward0)
    forwardEnd = np.multiply(forwardWithUmb[4],backward5)

    forwardBackwardResult[0] = np.round(np.power(np.sum(backwardStart),-1)*backwardStart,3).tolist()
    forwardBackwardResult[5] = np.round(np.power(np.sum(forwardEnd),-1)*forwardEnd  ,3).tolist()

def calculate(observationList):
    for obs in observationList:
        forwardFromLastDay()
        forwardUmbrellaObservation(obs)
        backwardNextDay(obs)
        backwardUmbrellaObservation()
    forwardBackward()

def updateDayControl():
    global dayControl
    dayControl +=1

def plot(list1,list2):
    print("Martin")


#computeFromLastDay()
#computeUmbrellaObservation(1)
calculate([1,1,0,1,1])
print(forward)
print(forwardWithUmb)
print(backward)
print(backwardWithUmb)
print(forwardBackwardResult)
