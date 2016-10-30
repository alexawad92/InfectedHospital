#!/usr/bin/env python3
#Ahmad Awad
#The goal of this script is to create  a Monte Carlo simulator of
#the spread of an infectious disease in a hospital ward.  assume that the ward always contains 100 patients,
#arranged in a 10x10 (n=10) grid with equal distances between neighboring patients.
#We also Assume that the infectious
#disease in this model always lasts exactly k days (meaning, every patient who gets it will recover after k days)
##In this model, three conditions must be met in order for a patient to become infected:
##Patient is currently susceptible (matrix cell value is zero)
##Patient has at least one infected neighbor. Having more than one infected neighbor should increase the probability of infection spread 
##A random number generated by numpy.random.rand() is less than the infection spread rate tau.
#####################################################################################################
##The simulation should terminate once all patients have recovered. In terms of the values of the matrix,
##this means that the simulation should terminate when the matrix no longer contains any positive, non-zero values.
##Throughout the simulation, a patient may be in one of four states: susceptible to infection, infected (in the ith day of infection; 1 <= i <= k), recovered, or vaccinated.
##We Let these states be represented by 0,i,-1,-2, respectively

##USER WILL BE ASKED TO ENTER THE FOLLOWING VALUES
##RecoverDays (K)
##Infection spread rate(tau)
##Vaccination rate (nu)
##Number of threads
##IF the user would like to see the visualization (y for yes, n for no)
##
##at the end of the simulation, the average will calculated for each of the
#three lists, Total_infection, Total_vaccination, Total_recover

from numpy import *
import numpy as np
from random import randint #will be used to get a random number
import matplotlib as mpl #will be used for visualization
from matplotlib import pyplot 
import matplotlib.pyplot as plt
from time import sleep
from threading import Thread
import itertools

class ThreadTest(Thread):

# Define any args you will be passing to the thread here:
     def __init__(self, n, k) :
           Thread.__init__(self)
           self.n = n
           self.k = k
           self.returnday = -1
           self.returninfected = -1
           self.returnvaccin = -1
           self.returnrecover = -1
# The code that the thread executes goes here:
     def run(self) :
          n = self.n
          k = self.k
          infected, vaccinated, recovered,day = DoIt(recoverDays,tau, nu)
          self.returnday = day
          self.returninfected = infected
          self.returnvaccin = vaccinated
          self.returnrecover  = recovered
#########################################################


#this function will will decide if the person gets infected or not
#It will check to see if any of the 4 persons around that person is infected
#then he might get infected.
#if he does get infected then it returns -3
#otherwise it will return 0
def infect(Pop,i,j,tau):
    t = 0 
    p = 0
    #we can check for North
    if (i > 0):
        if (Pop[i-1, j] > 0):# north is infected 
            t = (random.rand() < tau)

        if (t == True):
            p = -3
            return p
         
    if( i < 9): # we can check for southern 
        if (Pop[i+1, j] > 0): #south is infected
            t = (random.rand() < tau)
        if ( t == True):
            p = -3
            return p

    if ( j > 0): # we can check west
        if (Pop[i, j-1] > 0): #west is infected 
            t = (random.rand() < tau)
        if (t == True):
            p = -3
            return p
    if (j < 9): # we can check east
        if (Pop[i, j+1] > 0):
            t = (random.rand() < tau)
        if (t == True):
            p = -3
            return p
    return p


#This Function will be called to see if a person get to be
#vaccinated or not
#if the person gets vaccinated it returns -2, otherwise it returns 0

def vaccinat(Pop, i, j, nu):
    t = 0
    t = (random.rand() < nu)
    if (t == True):
        return -2
    return 0

#this function will loop through the matrix 
#and it will call the infect function first to see if that person
#will get infected, if the value stays 0 after calling the infect function
#then it will call the vaccination function to see if the person gets vaccinated 
def DoIt(recoverDays,tau, nu):
    inf = 0 #will hold the number of infected people in the matrix in each day
    vac = 0 ##will hold the number of vaccinated  people in the matrix in each day
    rec = 0  #will hold the number of recvoced people in the matrix in each day
    Days = 0 #counter for days
    day = [0] #the Graph in blackboard, starts at day 0 and the value of infected people at that day is 1,
    Pop = zeros((10,10)) #10 by 10 matrix with all zeros
    infected = [] #List will hold number of infected ppl in each 
    vaccinated = []#list will hold number of vaccination in each day
    recovered = [] #list will hold number of recovered in each day
    #three counters
##    #******************************************
    #generate random numner, choose two values random each between 0 and 9

    x = random.randint(0,9)
    y = random.randint(0,9)
     ##infect that random cell, make its value 1
    Pop[x,y] = 1
    inf += 1
    infected.append(inf)
    vaccinated.append(vac)
    recovered.append(rec)
    
    Exist_one = True #it means there is at least one person who is infected 
     #it will keep looping till there are no one in the matrix who is infected 
    while (Exist_one): 
        Exist_one = False
        for row in range (10):
            for col in range (10):
                if (Pop[row,col] > 0):
                    Pop[row,col] +=1
                if (Pop[row,col] == recoverDays):
                    Pop[row,col] = -1
                    rec += 1 ##num of recoved ppl are incremented by one
                    inf -= 1 ##num of infected ppl is less by one
                if (Pop[row, col] == 0 ): #this CELL can be infected 
                    Pop [row, col] = infect(Pop, row, col, tau)
                    if (Pop[row,col] == -3): #he got infected, new patient
                        inf += 1
                if (Pop[row,col] == 0): #if he still not infected 
                    Pop[row,col] = vaccinat(Pop, row,col, nu)
                    if (Pop[row,col] == -2): #some one got vaccinated
                        vac += 1
                if (Pop[row,col] > 0 or Pop[row,col] == -3 ):
                    Exist_one = True
        for row in range(10):
            for col in range (10):
                if (Pop[row,col] == -3):
                    Pop[row,col] = 1
                    
        infected.append(inf)
        vaccinated.append(vac)
        recovered.append(rec)
        Days += 1
        day.append(Days)

    return infected, vaccinated, recovered, day
###############################################
###CODE STARTS######
##The user will be prompted for the following information
recoverDays = int(input("Please Enter number of Days to recover after being infected( > 0 ):"))
tau = float(input("Please Enter the infection spread rate _tau_ value(float [0,1)):"))
nu = float(input("Please Enter the vaccination rate _nu_ value(float [0,1)):"))
NumOfTH = int(input("Please Enter number of threads( > 0): "))
#x = input("Do you like to visualize the first thread, (y,n)?")
x = 'n'
SimNum = NumOfTH
##print("Disease is speading...")
##sleep(1)
visual = False
if (x == 'y'):
     visual = True
##recoverDays = 10
##tau = 0.8
##nu = 0.1
#NumOfTH = 3
total_day = []
total_inf = []
total_vac = []
total_rec = []
plt.ion()
#if the user decide to see the first thread visualized then, the first the following will run the
#the first thread and visualize it.
#the following code is the same as the DoIt function except it has some
#extra lines for the visualization
if (visual):
     NumOfTH -= 1
     Pop = zeros((10,10))
     infected = []
     vaccinated = []
     recovered = []
     #three counters
     inf = 0
     vac = 0
     rec = 0
     Days = 0
     day = [0]
     #******************************************
     #generate random numner, choose two values random each between 0 and 9

     x = random.randint(0,9)
     y = random.randint(0,9)
     ##print("before call infect, one person ONYL is infected")
     ##print(Pop)
     Pop[x,y] = 1
     inf += 1
     infected.append(inf)
     vaccinated.append(vac)
     recovered.append(rec)
     #the colors will range depends on the status of the patient,
     #white means the person can get sick, never got sick, not vaccianted, and not recoverd
     #orange means that the person is recoverd after having being sick for k days
     #reyalblue means the person got vaccinated
     #colors range from lightpink to darkblue, each color represents a day 
     cmap = mpl.colors.ListedColormap(['orange', 'royalblue', 'white','lightpink','pink', 'hotpink','deeppink','mediumvioletred','m','darkmagenta','purple','indigo','darkblue'])
     bounds = [-3,-1.5,-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,recoverDays]
     norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
     img = pyplot.imshow(Pop,interpolation='nearest',
                         cmap = cmap,norm=norm)
     pyplot.colorbar(img,cmap=cmap,norm=norm,boundaries=bounds,ticks=[-2,0,recoverDays], label = '   VAC REC INFCT BGN ...................................................Will REC')
     pyplot.ion()
     pyplot.show()
     sleep(0.05)
     #**************************************************************************
     #we have array, draw it
     #The matrix will show up on the screen, one element
     #will be colored light pink, that is the random cell that was chosen
     #to be the first infected
     #the window might not pop up on the screen
     #TRY TO MINIMIZE the code screen and put the graph window
     #side to side with  the code screen and then press ENTER
     #to see the disease spreading
     #***************************************************************************
     con = input("Press enter To Start the Visual Simulation....")
     Exist_one = True
     while (Exist_one):
         Exist_one = False
         for row in range (10):
             for col in range (10):
                 if (Pop[row,col] > 0):
                     Pop[row,col] +=1
                 if (Pop[row,col] == recoverDays):
                     Pop[row,col] = -1
                     rec += 1 ##num of recoved ppl are incremented by one
                     inf -= 1 ##num of infected ppl is less by one
                 if (Pop[row, col] == 0 ): #this CELL can be infected 
                     Pop [row, col] = infect(Pop, row, col, tau)
                     if (Pop[row,col] == -3): #he got infected, new patient
                         inf += 1
                 if (Pop[row,col] == 0): #if he still not infected 
                     Pop[row,col] = vaccinat(Pop, row,col, nu)
                     if (Pop[row,col] == -2): #some one got vaccinated
                         vac += 1
                 if (Pop[row,col] > 0 or Pop[row,col] == -3 ):
                     Exist_one = True
         for row in range(10):
             for col in range (10):
                 if (Pop[row,col] == -3):
                     Pop[row,col] = 1
                     
         infected.append(inf)
         vaccinated.append(vac)
         recovered.append(rec)
         Days += 1
         day.append(Days)
         img = pyplot.imshow(Pop,interpolation='nearest',
                         cmap = cmap,norm=norm)
         
         pyplot.draw() #update the graph
         sleep(0.05)
     key = input("press enter to continue...")
     pyplot.close()
     total_day.append(day)
     total_inf.append(infected)
     total_vac.append(vaccinated)
     total_rec.append(recovered)

#the following code is will loop number of threads times,
#it will keep appending the result to the each total list which is
#a list of lists 
for i in range(0,NumOfTH) :
     current = ThreadTest(NumOfTH,i)
     current.start()
     current.join()
     total_day.append(current.returnday)
     total_inf.append(current.returninfected)
     total_vac.append(current.returnvaccin)
     total_rec.append(current.returnrecover)


#the following code will
#return how many elements in the longest
Maxlen_day = max(map(len,total_day))
Maxlen_inf = max(map(len,total_inf))
Maxlen_vac = max(map(len,total_vac))
Maxlen_rec = max(map(len,total_rec))

#Next it will loop in each list of lists and
#make all lists the same length
#by keep extending the last value in the shortest lists
for row in total_day:
     while (len(row) < Maxlen_day):
          row.extend([row[len(row)-1]])
for row in total_inf:
     while (len(row) < Maxlen_inf):
          row.extend([row[len(row)-1]])
for row in total_vac:
     while (len(row) < Maxlen_vac):
          row.extend([row[len(row)-1]])
for row in total_rec:
     while (len(row) < Maxlen_rec):
          row.extend([row[len(row)-1]])

#this will take a list of lists for each data and calculate the average
#and put that in a list. so each list of lists will be a list of averages 
avg_inf = np.mean(total_inf, axis=0)
avg_vac = np.mean(total_vac, axis =0)
avg_rec = np.mean(total_rec, axis = 0)
day_array  = arange(Maxlen_day)

#the following is for ploting the graph with the proper
#values and information, and trying to make it look
#like the one on black board
plt.axis([0,Maxlen_day,0,100])
x = array(day_array)
y = array(avg_inf)
z = array(avg_vac)
w = array(avg_rec)
plt.plot(x, y, 'r-', label = 'Infected')
plt.plot (x, z,'yo-',  label = 'Vaccinated')
plt.plot (x, w, 'b--', label = 'Recovered')
plt.title('Infection spread Model(sim. trial = %s ) \n Rates: infection = %s, Vaccination = %s, Recovery: after %s days'%(SimNum, tau, nu, recoverDays))
legend = plt.legend(loc='upper right', shadow = True)
plt.show()

stop = input("Press Any Key To EXIT...")

