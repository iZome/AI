import numpy as np
import array

rain = np.matrix('0.7 0.3;0.3 0.7')   #matix with probabilities for rain form [rain(1 and 2) rain(only 2);rain(only 1) rain(no)]

seeUmbrella = np.matrix('0.9 0.0;0.0 0.2')

noUmbrella = np.matrix('0.1 0.0;0.0 0.8')

probabilities = [0 for x in range(6)]
probabilitiesWithUmb = [0 for x in range(5)]
probabilities[0] = [0.5,0.5]
hi = [0.5,0.5]
print(hi)

dayControl = 0


def computeFromLastDay():
    if(dayControl == 0):
        lastDay = np.array([probabilities[dayControl]]) #get result from last day
    else:
        lastDay = np.array([probabilitiesWithUmb[dayControl-1]])
    lastDayFlipped = np.rot90(lastDay,-1)           #rotate vector to the right To do: figure out how last thing works
    toDay = np.dot(rain,lastDayFlipped)             #get chance for rain/not rain based on last day

    updateDayControl()                              #+1 on day-counting varible

    probabilities[dayControl] = np.round(np.rot90(toDay,1),3).tolist()[0]   #add the new probabily to the probability list

def computeUmbrellaObservation(guardObs):
    obsMatrix = 0                                   #matrix for observation
    toDay = np.array([probabilities[dayControl]])   #get chance for rain and not rain based on last day
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


    probabilitiesWithUmb[dayControl-1] = np.round(np.rot90(withObs,1),3).tolist()[0]

def calculate(observationList):
    for obs in observationList:
        computeFromLastDay()
        computeUmbrellaObservation(obs)


def updateDayControl():
    global dayControl
    dayControl +=1


#computeFromLastDay()
#computeUmbrellaObservation(1)
calculate([1,1,0,1,1])
print(probabilities)
print(probabilitiesWithUmb)
