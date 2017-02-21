import numpy as np
from matplotlib import pyplot as plt

rain = np.matrix('0.7 0.3;0.3 0.7')   #matrix with forward for rain form [rain(1 and 2) rain(only 2);rain(only 1) rain(no)]
seeUmbrella = np.matrix('0.9 0.0;0.0 0.2')  #Umbrella
noUmbrella = np.matrix('0.1 0.0;0.0 0.8')   #No Umbrella

#Lists
forward = [0 for x in range(6)]
backward = [0 for x in range(6)]
forwardBackward = [0 for x in range(6)]

#Initializing
forward[0] = [0.5,0.5]
backward[5] = [1.0,1.0]

#Forward part of the algorithm
def forwardPart(List):
    for i in range(1,6):
        lastDay = np.rot90([forward[i-1]],-1)     #using rot90 to make it possible to do dot product on the matrix
        if(List[i-1] == 0):
            obsMatrix = noUmbrella
        elif(List[i-1] == 1):
            obsMatrix = seeUmbrella
        else:
            print("Obs, you can only enter 0 or 1 here, you entered", List[i-1], ".")
        newDay = np.dot(obsMatrix,np.dot(rain,lastDay))
        forward[i] = np.round(np.rot90(np.power(np.sum(newDay),-1)*newDay,1),3).tolist()[0]
    printForwardBackward("Forward", forward)

#Backward part of the algorithm
def backwardPart(List):
    for i in range(4,-1,-1):
        nextDay = np.rot90([backward[i+1]],-1)     #using rot90 to make it possible to do dot product on the matrix
        if(List[i] == 0):
            obsMatrix = noUmbrella
        elif(List[i] == 1):
            obsMatrix = seeUmbrella
        else:
            print("Obs, you can only enter 0 or 1 here, you entered", List[i-1], ".")
        newDay = np.dot(rain,np.dot(obsMatrix,nextDay))
        backward[i] = np.round(np.rot90(np.power(np.sum(newDay),-1)*newDay,1),3).tolist()[0]
    printForwardBackward("Backward",backward)

#Combining forward and backward by multiplying and nomalizing
def forwardBackwardPart():
    for i in range(0,6):
        forwardBackwardToday = np.multiply(forward[i],backward[i])
        forwardBackward[i] = np.round(np.power(np.sum(forwardBackwardToday),-1)*forwardBackwardToday,3).tolist()
    printForwardBackward("ForwardBackward",forwardBackward)

#Lists for viterbi
viterbi = [0 for x in range(0,5)]
pointer = ['' for x in range(5)]

#A bit long, implementation of the viterbi algorithm which gives the most likly sequnce given a set of observations
def viterbiAlgortihm(List):
    viterbi[0] = forward[1]
    for i in range (1,len(forward)-1):
        probRain = 0
        probNoRain = 0
        if(List[i] == 0):
            rainUmb = 0.1
            noRainUmb = 0.8
        elif(List[i] == 1):
            rainUmb = 0.9
            noRainUmb = 0.2
        else:
            print("Obs, you can only enter 0 or 1 here, you entered", List[i-1], ".")

        counter = 0;
        for x in range(len(viterbi[i-1])):
            rainProb = rain[0].tolist()[0]
            rainTemp = viterbi[i-1][x]*rainUmb*rainProb[x]
            noRainTemp = viterbi[i-1][x]*noRainUmb*(1-rainProb[x])

            if(rainTemp > probRain):
                probRain = rainTemp
                if(counter == 0):
                    parentOfRain = "Rain"
                else:
                    parentOfRain = "No Rain"
            if(noRainTemp > probNoRain):
                probNoRain = noRainTemp
                if(counter == 0):
                    parentOfNoRain = 'Rain'
                else:
                    parentOfNoRain = "No Rain"
            counter += 1

        viterbi[i] = [probRain, probNoRain]
        pointer[i-1] = [parentOfRain, parentOfNoRain]
    viterbiPrint("Viterbi",viterbi,pointer)

#Print function for the lists in forwardbackward
def printForwardBackward(name,List):
    counter = 0
    print(name, "Form: [rain, not rain]")
    print("------------")
    for i in List:
        print("Day" , counter, ":" , i)
        counter += 1
    print("\n")


#Printing the results from the viterbi algorithm
def viterbiPrint(name,List,Pointers):
    print(name)
    print("------------")
    #Printing the last day based on the most likely result that day
    if(List[-1][0] >= List[-1][1]):
        printFirst = "Rain"
        probability = np.round(List[-1][0],3)
    else:
        printFirst = "No Rain"
        probability = np.round(List[-1][1],3)
    print("Day", len(List), ":", printFirst,". Probability: ", probability)
    #Printing the rest of the sequence based on the pointers from the viterbiAlgorithm
    for i in range(len(List)-1,0,-1):
        if(List[i][0] >= List[i][1]):
            printFirst = Pointers[i-1][0]
        else:
            printFirst = Pointers[i-1][1]

        if(List[i-1][0] >= List[i-1][1]):
            probability = np.round(List[i-1][0],3)
        else:
            probability = np.round(List[i-1][1],3)

        print("Day", i, ":", printFirst,". Probability: ", probability)
    print("\n")

#Plotting function, plots the forward, backward and forwardbackward development from day to day
def plot():
    forwardRain = [prob[0] for prob in forward]
    backwardRain = [prob[0] for prob in backward]
    forwardBackwardRain = [prob[0] for prob in forwardBackward]

    x = np.linspace(0,len(forwardBackward),len(forwardBackward))

    #plt.plot(forwardRain, x, backwardRain, x, forwardBackwardRain, x)
    plt.plot(x, forwardRain, label = 'Forward')
    plt.plot(x, backwardRain, label = 'Backward')
    plt.plot(x, forwardBackwardRain, label = 'Forward-Backward')
    plt.legend(loc='best')
    plt.show()

def main():
    List = [1,1,0,1,1]
    print("\nThe umbrella observation sequence is : ", List)
    forwardPart(List)
    backwardPart(List)
    forwardBackwardPart()

    #plot()
    viterbiAlgortihm(List)

main()
