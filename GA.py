__author__ = 'amritansh'


# Project 3 Q.2
# Amritansh
# Sunil Pawar

# Starting few necessary imports

import numpy as np
from threading import Thread
from time import sleep
import random
import os
import xml.etree.ElementTree as ET
import collections
initial=0
new_data=[]

gen_num = input("Enter The number of generations for GA: ")


# Base address and paths
phrase='tags_collected, time_in_minutes, random_seed'

configfile='/nfs/student/s/spawar/Downloads/iAnt-ARGoS-master/experiments/iAnt_linux_02.argos'
basedatafile='/nfs/student/s/spawar/Downloads/iAnt-ARGoS-master/iAntTagData.txt'
myfile='/nfs/student/s/spawar/Downloads/iAnt-ARGoS-master/iAntData.txt'
gen_file='/nfs/student/s/spawar/Downloads/iAnt-ARGoS-master/iAnt_gen_Data_01.txt'

# parsing the xml (.argos)

tree = ET.parse(configfile)

# Intializing random parameters

def random_parameters():
    pheromoneRate=20*random.random()
    pheromoneDecayRate=random.random()
    travelGiveupProbability=.9
    siteFidelityRate= 20*random.random()
    informedSearchDecay=random.random()
    searchRadius=random.random()
    searchGiveupProbability=random.random()*.01
    return pheromoneRate,pheromoneDecayRate,travelGiveupProbability,siteFidelityRate,informedSearchDecay,searchRadius,searchGiveupProbability


root = tree.getroot()
print root.tag

# changing the values for CPFA parameters
total=[]
for i in range(0,25):

    for node in root.iter('CPFA'):

        pheromoneRate,pheromoneDecayRate,travelGiveupProbability,siteFidelityRate,informedSearchDecay,searchRadius,searchGiveupProbability=random_parameters()

        node.attrib['pheromoneRate']=str(pheromoneRate)
        node.attrib['pheromoneDecayRate']=str(pheromoneDecayRate)
        node.attrib['travelGiveupProbability']=str(travelGiveupProbability)
        node.attrib['siteFidelityRate']=str(siteFidelityRate)
        node.attrib['informedSearchDecay']=str(informedSearchDecay)
        node.attrib['searchRadius']=str(searchRadius)
        node.attrib['searchGiveupProbability']=str(searchGiveupProbability)
        print node.attrib
        a=[pheromoneRate,pheromoneDecayRate,travelGiveupProbability,siteFidelityRate,informedSearchDecay,searchRadius,searchGiveupProbability]

    total.append(a)

# runing ARGoS simulator vie python terminal

    for i in range(0,5):
        tree.write(configfile)
        os.chdir("/nfs/student/s/spawar/Downloads/iAnt-ARGoS-master")


        os.system("argos3 -c experiments/iAnt_linux_02.argos")


print total


# writing our data in a custom file which will be used in evaluation of fitness


with open(basedatafile,"r") as input:
    with open(myfile,"wb") as output:
        for line in input:
            if line!=phrase+"\n":
                output.write(line)
os.remove(basedatafile)

output.close()

# Reading the custom log file

def readLogFile():
    data=np.loadtxt(myfile, delimiter=',')


    x=(data[:,0])
    return x

# calculating efficency of each rule set
def efficiency(total):
    tags_collected=readLogFile()
    print tags_collected
    value_pair=  {tags_collected[n]: total[n] for n in range(25)}


    return value_pair
records=efficiency(total)

# sorting the data value
def sorting(records):
    od = collections.OrderedDict(sorted(records.items()))
    list=[]
    print od
    for v in od.iteritems():

        list.append(v[1])
    print list



    return list



sorted_values=sorting(records)

# choosing elites from our data
def elites(sorted_values):
    n=len(sorted_values)
    # print n
    # for l in sorted_values:
    #   print l
    elite=[]
    for i in range(0,5):
        elite.append(sorted_values[n-i-1])
    return elite

def mutation():
    i =random.randint(0.5)

elite_values=elites(sorted_values)

# Using crossover to generate new rules

def crossover(elite_values):
    new_population=[]
    temp_list=[]

    print elite_values[2][5]
    for l in elite_values:
        print l
        new_population.append(l)

    for i in range(0,20):

        temp_list=[elite_values[random.randint(0,4)][j] for j in range(0, 7)]
        print temp_list
        new_population.append(temp_list)



    return new_population


new_data=crossover(elite_values)
initial=1



while(initial<=gen_num):
    print " Start of Generation : " ,initial
    a = np.array(new_data)

    # else:
    root = tree.getroot()
    print root.tag

    def parameters(a):
    # for i in range(0,25):
        pheromoneRate=a[:,0]

        pheromoneDecayRate=a[:,1]
        travelGiveupProbability=a[:,2]
        siteFidelityRate= a[:,3]
        informedSearchDecay=a[:,4]
        searchRadius=a[:,5]
        searchGiveupProbability=a[:,6]
        return pheromoneRate,pheromoneDecayRate,travelGiveupProbability,siteFidelityRate,informedSearchDecay,searchRadius,searchGiveupProbability


    total=[]
    pheromoneRate_ga,pheromoneDecayRate_ga,travelGiveupProbability_ga,siteFidelityRate_ga,informedSearchDecay_ga,searchRadius_ga,searchGiveupProbability_ga=parameters(a)

    for i in range(0,25):
        for node in root.iter('CPFA'):



            node.attrib['pheromoneRate']=str(pheromoneRate_ga[i])
            node.attrib['pheromoneDecayRate']=str(pheromoneDecayRate_ga[i])
            node.attrib['travelGiveupProbability']=str(travelGiveupProbability_ga[i])
            node.attrib['siteFidelityRate']=str(siteFidelityRate_ga[i])
            node.attrib['informedSearchDecay']=str(informedSearchDecay_ga[i])
            node.attrib['searchRadius']=str(searchRadius_ga[i])
            node.attrib['searchGiveupProbability']=str(searchGiveupProbability_ga[i])
            print node.attrib





        tree.write(configfile)
        os.chdir("/nfs/student/s/spawar/Downloads/iAnt-ARGoS-master")


        os.system("argos3 -c experiments/iAnt_linux_02.argos'")



    with open(basedatafile,"r") as input:
        with open(myfile,"wb") as output:
            for line in input:
                if line!=phrase+"\n":
                    output.write(line)
    os.remove(basedatafile)

    output.close()
    def readLogFile():
        data=np.loadtxt(myfile, delimiter=',')


        x=(data[:,0])
        return x
    def efficiency():
        gen_temp=readLogFile()

        print gen_temp
        gen_temp=gen_temp.reshape((25, 1))

        return np.append(a,gen_temp,axis=1)

    bad_ass=efficiency()


    def sorting(bad_ass):
        sorted_data=bad_ass[bad_ass[:,7].argsort()]
        # print "Sorted data" ,sorted_data
        #
        # return list
        return sorted_data
    sorted_values=sorting(bad_ass)

    def elites(sorted_values):
        z=[]
        def myfunc(n):
            for i in range(0,5):
                yield n

        z = np.fromiter(myfunc(initial), dtype=int)
        z= z.reshape((5,1))


        elite=sorted_values[[24,23,22,21,20], :]

        temp_arr=np.append(elite,z,axis=1)
        with open(gen_file, "a") as myfile:
            np.savetxt(myfile,temp_arr, delimiter=',')
        return elite
    elite_data=elites(sorted_values)

    def mutation(elite_data):
        random_number = (random.random() * 2 - 1)*0.2
        i= random.randint(0,4)
        j= random.randint(0,6)
        elite_data[i:j]=elite_data[i:j] * (1+random_number)
        return elite_data

    mutated_value=mutation(elite_data)


    def crossover(mutated_value):
        # print mutated_value[:,0:6]
        new_values=mutated_value[:,0:7].tolist()

        new_population=[]
        temp_list=[]

        for l in new_values:
            new_population.append(l)

        for i in range(0,20):

            temp_list=[new_values[random.randint(0,4)][j] for j in range(0, 7)]

            new_population.append(temp_list)
        return new_population
    new_data=crossover(mutated_value)



    initial+=1
print "End of Program Execution"