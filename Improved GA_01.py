
__author__ = 'amritansh'


import numpy as np
import math
import random
import os
import xml.etree.ElementTree as ET

initial=0
new_data=[]

gen_num = input("Enter The number of generations for GA: ")


# Base address and paths Change as per required.
phrase='tags_collected, time_in_minutes, random_seed'

configfile='/nfs/student/s/spawar/Documents/iAnt-ARGoS/experiments/homemade.argos'
basedatafile='/nfs/student/s/spawar/Documents/iAnt-ARGoS/iAntTagData.txt'
myfile='/nfs/student/s/spawar/Documents/iAnt-ARGoS/iAntData.txt'
gen_file='/nfs/student/s/spawar/Documents/iAnt-ARGoS/iAnt_gen_Data.txt'

# parsing the xml (.argos)

tree = ET.parse(configfile)

# Intializing random parameters

def random_parameters():
    pheromoneRate=20*random.random()
    pheromoneDecayRate=random.random()
    travelGiveupProbability=.9
    siteFidelityRate= 20*random.random()
    informedSearchDecay=random.random()
    searchRadius=random.random()*2
    searchGiveupProbability=random.random()*.01
    return pheromoneRate,pheromoneDecayRate,travelGiveupProbability,siteFidelityRate,informedSearchDecay,searchRadius,searchGiveupProbability


root = tree.getroot()


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
        x=[pheromoneRate,pheromoneDecayRate,travelGiveupProbability,siteFidelityRate,informedSearchDecay,searchRadius,searchGiveupProbability]

    total.append(x)

# runing ARGoS simulator vie python terminal

    for i in range(0,5):
        tree.write(configfile)
        os.chdir("/nfs/student/s/spawar/Documents/iAnt-ARGoS")

        # os.system("pwd")
        os.system("argos3 -c experiments/homemade.argos")


print total

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
    x=x.reshape(25,5)
    # print x.shape
    x=(np.average(x, axis=1))

    return x



def efficiency():
        gen_temp=readLogFile()
        a=np.array(total)

        gen_temp=gen_temp.reshape((25, 1))

        return np.append(a,gen_temp,axis=1)

bad_ass=efficiency()

print bad_ass
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

    # temp_arr=np.append(elite,z,axis=1)
    # with open(gen_file, "a") as myfile:
    #     np.savetxt(myfile,temp_arr, delimiter=',')
    return elite
elite_data=elites(sorted_values)

# def mutation(elite_data):
#     random_number = (random.random() * 2 - 1)*0.2
#     i= random.randint(0,4)
#     j= random.randint(0,6)
#     elite_data[i:j]=elite_data[i:j] * (1+random_number)
#     return elite_data

# mutated_value=mutation(elite_data)


def crossover(elite_data):
    # print mutated_value[:,0:6]
    new_values=elite_data[:,0:7].tolist()

    new_population=[]
    temp_list=[]

    for l in new_values:
        new_population.append(l)

    for i in range(0,20):

        temp_list=[new_values[random.randint(0,4)][j] for j in range(0, 7)]

        new_population.append(temp_list)
    return new_population
new_data=crossover(elite_data)
initial=1

while(initial<=gen_num):
    print " Start of Generation : " ,initial
    a = np.array(new_data)
    print a
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




        for i in range(0,5):
          tree.write(configfile)
          os.chdir("/nfs/student/s/spawar/Documents/iAnt-ARGoS")

          #os.system("pwd")
          os.system("argos3 -c experiments/homemade.argos")



    with open(basedatafile,"r") as input:
        with open(myfile,"wb") as output:
            for line in input:
                if line!=phrase+"\n":
                    output.write(line)
    os.remove(basedatafile)

    output.close()
    def readLogFile():
        data=np.loadtxt(myfile, delimiter=',')

        print data.shape
        x=(data[:,0])
        x=x.reshape(25,5)
        # print x.shape
        x=(np.average(x, axis=1))
        return x

    def efficiency():
        gen_temp=readLogFile()

        # print gen_temp
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