#!/usr/bin/python
#Solving Knapsack Problem with Genetic Algorithms
import math
import pickle
import random
import numpy as np
import pandas as pd
from scipy.stats import norm


def fitness(max_volume, volumes, prices):
    '''
    This returns a scalar which is to be maximized.
    max_volume is the maximum volume that the knapsack can contain.
    volumes is a list containing the volume of each item in the knapsack.
    prices is a list containing the price of each item in the knapsack, 
    which is aligned with 'volumes'.
    '''
    fitness = np.sum(prices)
    volume = np.sum(volumes)
    return (volume, fitness)

           
def reshape1(maxVol, chromosome, volumes, prices):
    '''
    This shapes chromosome whose total volumes > maxVol
    by making iteratively 1s to 0s unitl maxVol >= volume
    '''
    n = len(chromosome)
    volume = np.sum(volumes * chromosome)
    while volume > maxVol:
        i = random.randint(0,(n-1))
        if (chromosome[i] == 1):
            chromosome[i] = 0
            volume = np.sum(volumes * chromosome)
            #print "DBG volume", volume
            if maxVol >= volume:
                fitness = np.sum(prices * chromosome)
                return (chromosome, volume, fitness)
        

def randomSelection(population, fitnesses):
    '''
    This returns a single chromosome from the population. The selection process 
    is random, but with weighted probabilities proportional to the corresponding 
    'fitnesses' values.
    '''
 
    #Roulette-wheel selection
    fsum = np.sum(fitnesses)
    limit = random.randint(0, int(fsum))
    
    n = len(fitnesses)
    curSum = 0
    for i in range(n):
        curSum = curSum + fitnesses[i]
        if curSum >= limit: 
            chosenOne = population[i]
            return chosenOne


def reproduce(mom, dad):
    '''
    This does genetic algorithm crossover. This takes two chromosomes, 
    mom and dad, and returns two chromosomes.
    '''
    s = len(mom)
    pos = random.randint(1, (s-1))
    while (pos < s):
        temp = mom[pos]
        mom[pos] = dad[pos]
        dad[pos] = temp
        pos = pos + 1
    return (mom, dad)


def mutate(child, mbits):
    "This takes a child, produces a mutated child after mutation of mbits."
    for i in range(mbits): 
        k = random.randint(0, (len(child) - 1))
        if child[k] == 1:
            child[k] = 0
        else:
            child[k] = 1
    return child


def compute_fitnesses(world, chromosomes):
    '''
    This takes an instance of the knapsack problem and a list of chromosomes and 
    returns the fitness of these chromosomes, according to your 'fitness' function.
    '''
    return [fitness(world[0], world[1] * chromosome, world[2] * chromosome) for chromosome in chromosomes]


def genetic_algorithm(world, popsize, max_years, mutation_probability):
    '''
    This returns a list of (chromosomes, fitnesses) tuples, where chromosomes 
    is the current population of chromosomes, and fitnesses is
    the list of fitnesses of these chromosomes. 
    '''
    #maxVol is the volume of the Knapsack, volumes = volumes of the items, 
    #prices = values of the items
    maxVol, volumes, prices = world
    #We are given n items, it is the size of the chromosomes
    n = len(volumes)
    #POPULATION
    #Randomly generate population of the popsize
    #Each chromosome is an array of length n, where we have n items
    #chromosomes is a matrix of dimension (popsize X n)
    chromosomes = np.zeros((popsize, n))
    #Now fill up the chromosomes 1 or 0 randomly
    for i in range(popsize):
        for j in range(n):
            chromosomes[i][j] = random.randint(0, 1)

    #Main loop for generations 
    finalOutputList = []
    year = 1
    while (year <= max_years):
        newChromosomes = np.zeros((popsize, n))
        #Compute fitnesses of the initial population
        outputList = compute_fitnesses(world, chromosomes)
        #Shape the list as a matrix
        outputList = np.reshape(outputList, (popsize, 2))
        volumeList = outputList[:,0]
        fitnessList = outputList[:,1]
        
        #Check if the termination condition found
        #Reshape the chromosome whose volume is > maxVol
        for i in range(popsize):
            if volumeList[i] > maxVol:
                (chromosomes[i], volumeList[i], fitnessList[i]) = reshape1(maxVol, chromosomes[i], volumes, prices)

        #SELECTION
        #10% of highest fit chromosome just pass on to next generation 
        count1 = math.ceil(popsize * 0.1)
        #For remaining count2 I will do crossover in pair
        count2 = popsize - count1
        #Make count2 even
        if ((count2 % 2) == 1):
            count2 = count2 - 1
            count1 = count1 + 1
        i = 0
        while (i < popsize):
            if (i < count1):
                #Just pass on to the next generation
                chromosome = randomSelection(chromosomes, fitnessList)
                newChromosomes[i] = chromosome
                i = i + 1
            else:
                #CROSSOVER
                #Do cross over and pass the childs onto next gen
                chromosome1 = randomSelection(chromosomes, fitnessList) 
                #This iteration selects two chromosome and reproduces two
                chromosome2 = randomSelection(chromosomes, fitnessList) 
                #Once we go two chromosome, lets crossover
                (chromosome1, chromosome2) = reproduce(chromosome1, chromosome2) 
                newChromosomes[i] = chromosome1
                i = i+1
                newChromosomes[i] = chromosome2
                i = i+1

        #MUTATION
        #Perform mutation on all the chromosomes at given probability rate
        #At p probability rate n*p bits need to be mutated per chromosome
        p = mutation_probability
        mbits = int(math.ceil(p*n))
        i = 0
        for chromosome in (newChromosomes):
            newChromo = mutate(chromosome, mbits)
            newChromosomes[i] = newChromo

        #After this iteration store the output in a final list
        outputList = compute_fitnesses(world, newChromosomes)
        outputList = np.reshape(outputList, (popsize, 2))
        volumeList = outputList[:,0]
        fitnessList = outputList[:,1]
        
        #Before appending the newChromosomes, recalculate fitnessList
        outputList = compute_fitnesses(world, newChromosomes)
        #Shape the list as a matrix
        outputList = np.reshape(outputList, (popsize, 2))
        newVolumeList = outputList[:,0]
        newFitnessList = outputList[:,1]
        #Once we got new chromosomes reshape them if needed if, vol crosses maxVol
        for i in range(popsize):
            if newVolumeList[i] > maxVol:
                (newChromosomes[i], newVolumeList[i], newFitnessList[i]) = reshape1(maxVol, newChromosomes[i], volumes, prices)
        #print "-----------------------------------------------------------"
        #print "Year: ", year
        #print "newchromosomes:", newChromosomes 
        #print "newvolumelist:", newVolumeList 
        #print "newfitnesslist:", newFitnessList 
        #print "-----------------------------------------------------------"
        finalOutputList.append((newChromosomes, newFitnessList))

        #Set chromosomes for next generation loop
        chromosomes = newChromosomes
        year = year + 1
        #End of main loop

    #Once the main loop is over return the output list
    return finalOutputList
    

def run(popsize,max_years,mutation_probability):
    '''
    This runs genetic_algorithm on various knapsack problem instances and keeps 
    track of tabular information with this schema:
    DIFFICULTY YEAR HIGH_SCORE AVERAGE_SCORE BEST_PLAN
    '''
    table = pd.DataFrame(columns=["DIFFICULTY", "YEAR", "HIGH_SCORE", "AVERAGE_SCORE", "BEST_PLAN"])
    sanity_check = (10, [10, 5, 8], [100,50,80])
    chromosomes = genetic_algorithm(sanity_check,popsize,max_years,mutation_probability)
    for year, data in enumerate(chromosomes):
        year_chromosomes, fitnesses = data
        table = table.append({'DIFFICULTY' : 'sanity_check', 'YEAR' : year, 'HIGH_SCORE' : max(fitnesses),
            'AVERAGE_SCORE' : np.mean(fitnesses), 'BEST_PLAN' : year_chromosomes[np.argmax(fitnesses)]}, ignore_index=True)
    easy = (20, [20, 5, 15, 8, 13], [10, 4, 11, 2, 9] )
    chromosomes = genetic_algorithm(easy,popsize,max_years,mutation_probability)
    for year, data in enumerate(chromosomes):
        year_chromosomes, fitnesses = data
        table = table.append({'DIFFICULTY' : 'easy', 'YEAR' : year, 'HIGH_SCORE' : max(fitnesses),
            'AVERAGE_SCORE' : np.mean(fitnesses), 'BEST_PLAN' : year_chromosomes[np.argmax(fitnesses)]}, ignore_index=True)
    medium = (100, [13, 19, 34, 1, 20, 4, 8, 24, 7, 18, 1, 31, 10, 23, 9, 27, 50, 6, 36, 9, 15],
                   [26, 7, 34, 8, 29, 3, 11, 33, 7, 23, 8, 25, 13, 5, 16, 35, 50, 9, 30, 13, 14])
    chromosomes = genetic_algorithm(medium,popsize,max_years,mutation_probability)
    for year, data in enumerate(chromosomes):
        year_chromosomes, fitnesses = data
        table = table.append({'DIFFICULTY' : 'medium', 'YEAR' : year, 'HIGH_SCORE' : max(fitnesses),
            'AVERAGE_SCORE' : np.mean(fitnesses), 'BEST_PLAN' : year_chromosomes[np.argmax(fitnesses)]}, ignore_index=True)
    hard = (5000, norm.rvs(50,15,size=100), norm.rvs(200,60,size=100))
    chromosomes = genetic_algorithm(hard,popsize,max_years,mutation_probability)
    for year, data in enumerate(chromosomes):
        year_chromosomes, fitnesses = data
        table = table.append({'DIFFICULTY' : 'hard', 'YEAR' : year, 'HIGH_SCORE' : max(fitnesses),
            'AVERAGE_SCORE' : np.mean(fitnesses), 'BEST_PLAN' : year_chromosomes[np.argmax(fitnesses)]}, ignore_index=True)
    for difficulty_group in ['sanity_check','easy','medium','hard']:
        group = table[table['DIFFICULTY'] == difficulty_group]
        bestrow = group.ix[group['HIGH_SCORE'].argmax()]
        print("Best year for difficulty {} is {} with high score {} and chromosome {}".format(difficulty_group,int(bestrow['YEAR']), bestrow['HIGH_SCORE'], bestrow['BEST_PLAN']))
    #saves the performance data.
    table.to_pickle("results.pkl") 


#Run the program
run(100, 1000, 0.1)



