N = int(7.5*(10**9)) - 2# total population alive at the beginning
gammaAbs = 3 # lifetime of a zombie
beta = 0.9 # the probability of an infection upon an encounter
rhoAbs = 0 # time of incubation
if rhoAbs == 0:
    rhoZero = True
else:
    rhoZero = False
global D
D = []
global S
S = []
global I
if rhoZero:
    I = [0]
else:
    I = []
global Z
Z = []
global incubatedAdditionals
incubatedAdditionals = [0] * rhoAbs
global zombieAdditionals
zombieAdditionals = [0] * gammaAbs
incubatedAdditional = 0
diedAdditional = 0
zombieAdditional = 0

def createValues(day, value):
    for d in range(0, day+1):
        #DEBUG print("day = ", d)
        D.append(numOfD(d))
        if numOfPeopleAlive(d) == 0:
            Z.append(0)
            I.append(0)
            S.append(0)
            break
        Z.append(numOfZ(d))
        zombieAdditionals.append(zombieAdditional)
        zombieAdditionals.pop(0)
        if not rhoZero:
            I.append(numOfI(d))
            incubatedAdditionals.append(incubatedAdditional)
            incubatedAdditionals.pop(0)
        S.append(numOfS(d))

        
        if value == "D":
            print(D[-1])
        if value == "Z":
            print(Z[-1])
        if value == "I":
            print(I[-1])
        if value == "S":
            print(S[-1])
        if Z[-1] == 0 and I[-1] == 0 and d >= 20:
            break

def numOfD(day): # returns num of died people
    global diedAdditional
    if day == 0:
        return 0
    elif day == 1:
        return 0
    previous = D[-1]
    return previous + zombieAdditionals[-1 * gammaAbs]

def numOfZ(day): # returns num of zombies
    global zombieAdditional
    if day == 0:
        return 0
    elif day == 1:
        zombieAdditional = 2
        return 2
    previous = Z[-1]
    if rhoZero:
        probabilityOfAnEncounter = S[-1] * Z[-1] / numOfPeopleAlive(day)
        zombieAdditional = int(probabilityOfAnEncounter * beta)
    else:
        zombieAdditional = incubatedAdditionals[-1 * rhoAbs]
    return previous + zombieAdditional - zombieAdditionals[-1 * gammaAbs]
    """num of zombies at the previous day + probability of incubated people becoming zombies * num of incubated peoble at the
    previous day - (difference between the num of dead people at this day and at the previous day)"""

def numOfI(day): # returns num of incubated people
    global incubatedAdditional
    if day == 1:
        return 0 # no one is incubated/infected at the beginning of the zombie epidemic
    if day == 0:
        return 0
    probabilityOfAnEncounter = S[-1] * Z[-2] / numOfPeopleAlive(day)
    incubatedAdditional = int(probabilityOfAnEncounter * beta)
    previous = I[-1]
    #DEBUG print("numOfPeopleAlive = ", numOfPeopleAlive(day))
    #DEBUG print("incubatedAdditional = ", incubatedAdditional)
    #DEBUG print("zombieAdditional ", zombieAdditional)
    return previous + incubatedAdditional - zombieAdditional

def numOfS(day): # returns num of suscepted people
    if day == 0:
        return N + 2
    if day == 1:
        return N
    if rhoZero:
        return N - D[-1] - Z[-1] + 2
    return N - D[-1] - I[-1] - Z[-1] + 2


def numOfPeopleAlive(day): # returns num of people alive
    return N + 2 - D[day-1]#the subtraction of the population before the zombie epidemic and the died people after the beginning