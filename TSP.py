import random
routes = {
    "CH,CAI"  : 6129,
    "CH,BA"   : 5598,
    "CH,BE"   : 4405,
    "CH,CT"   : 8494,
    "CH,CAL"  : 7980,
    "CH,CAR"  : 2501,
    "CAR,CH"  : 2501,
    "CAR,BA"  : 3168,
    "CAR,CAI" : 6338,
    "CAR,BE"  : 5247,
    "CAR,CAL" : 9605,
    "CAR,CT"  : 6365,
    "BA,CAR"  : 3168,    
    "BA,CAI"  : 7345,    
    "BA,CH"   : 5598,    
    "BA,CT"   : 4269,    
    "BA,CAL"  : 10265,    
    "BA,BE"   : 7402,    
    "CT,BA"   : 4269,    
    "CT,BE"   : 5981,    
    "CT,CAR"  : 6365,    
    "CT,CAI"  : 4500,    
    "CT,CH"   : 8494,    
    "CT,CAL"  : 6024,    
    "CAI,CT"  : 4500,    
    "CAI,CAR" : 6338,    
    "CAI,CH"  : 6129,    
    "CAI,BA"  : 7345,    
    "CAI,BE"  : 1795,    
    "CAI,CAL" : 3539,    
    "CAL,CAI" : 3539,    
    "CAL,CT"  : 6024,    
    "CAL,CAR" : 9605,    
    "CAL,CH"  : 7980,    
    "CAL,BA"  : 10265,    
    "CAL,BE"  : 4368,    
    "BE,CAL"  : 4368,    
    "BE,CT"   : 5981,    
    "BE,BA"   : 7402,    
    "BE,CAI"  : 1795,    
    "BE,CAR"  : 5247,    
    "BE,CH"   : 4405,    
}

route = ["CAR","BA","CT","CAI","CAL","BE"]


def generateIndividual(route):    
    individual = ["CH"]
    for p in random.sample(route,len(route)):
        individual.append(p)
    individual.append("CH") 
    return individual

def generatePopulation(amount,route):
    population = []    
    for i in range(amount):        
        population.append(generateIndividual(route))
    return population


def fitness(population,routes):
    individualsDistances = []       

    for individual in population:                        
        total = 0
        for i in range(len(individual)-1):
            total += routes[individual[i]+","+individual[i+1]]                
        individualsDistances.append((total,individual))
    individualsDistances.sort()    
    return individualsDistances


def wheel(individualsDistances,amount):
    selected = []    
    options = []
    while len(options)<6:
        n = random.randint(0,100)        
        if n>=0 and n<=70:
            index = random.randint(0,3)
        elif n>70 and n<=95:
            index = random.randint(0,10)
        else:
            index = random.randint(0,amount-1)

        if options.count(index)==0:
                options.append(index)    

    for i in range(6):
        selected.append(individualsDistances[options[i]])        
    return selected

def combination(selected):
    parent = random.sample(selected,2)    
    r = random.randint(2,len(parent[0][1])-2)
    newIndividual = []        
    for i in range(r):
        newIndividual.append(parent[0][1][i])
    
    while len(newIndividual)<len(parent[0][1]):
        index = parent[1][1].index(newIndividual[len(newIndividual)-1])
        if newIndividual.count(parent[1][1][index+1])==0:
            newIndividual.append(parent[1][1][index+1])
        elif len(newIndividual)==(len(parent[0][1])-1):
            newIndividual.append(parent[1][1][len(parent[0][1])-1])
        else:
            bandera = True                        
            while bandera:
                if newIndividual.count(parent[0][1][r])==0:
                    newIndividual.append(parent[0][1][r])
                    bandera=False
                r += 1                
    return newIndividual

def mutate(newIndividual,possibility):
    mutatedIndividual = []
    if possibility > random.random():
        mutation = []
        if (random.randint(0,1))==1:                
            for i in range(3):
                mutatedIndividual.append(newIndividual[i])
            for i in range(3,len(newIndividual)-1):
                mutation.append(newIndividual[i])
            random.shuffle(mutation)
            for m in mutation:
                mutatedIndividual.append(m)
            mutatedIndividual.append("CH")
        else:                      
            mutatedIndividual.append("CH")
            for i in range(1,5):
                mutation.append(newIndividual[i])
            random.shuffle(mutation)
            for m in mutation:
                mutatedIndividual.append(m)            
            for i in range(5,len(newIndividual)):
                mutatedIndividual.append(newIndividual[i])                            
    else:
        mutatedIndividual = newIndividual        
    return mutatedIndividual

def newGeneration(amount,route,routes,possibility):
    population = generatePopulation(amount,route)
    individualsDistances = fitness(population,routes)
    selected = wheel(individualsDistances,amount)
    newIndividuals = []

    b = True
    cont=0
    while b:
        cont+=1
        for i in range(amount):
            newIndividuals.append(mutate(combination(selected),possibility))                
        individualsDistances = fitness(newIndividuals,routes)
        selected = wheel(individualsDistances,amount)              
        print("Generation "+str(cont)+":")
        for individual in selected:
            print(individual)
        print("e to exit, any other key to continue")  
        keyboard = input()
        if keyboard == "e":
            b = False
        else:
            newIndividuals = []
    
newGeneration(50,route,routes,0.2)
