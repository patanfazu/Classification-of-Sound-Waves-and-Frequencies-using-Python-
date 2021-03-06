
# Classification of Sound waves and frequencies
## Data Web Mining Project By BSc Students

# AP18211050005 Patan Fazulullah
# AP18211050007 Junapudi Scotti Deva
# AP18211050009 SVS Harsha
# AP18211050001 Desu Harshitha
# AP18211050006 Peddi Sree Deepthi
# AP18211050003 Shaik Abdul Rehman

from tempfile import TemporaryFile
import os

from python_speech_features import mfcc
import scipy.io.wavfile as wavefile
import numpy as np
import math
import numpy as np
from collections import defaultdict
import pickle
import random 
import operator
# imported all required packages.
ds = []
def loaddset(filename):
    with open("my.dat" , 'rb') as f:
        while True:
            try:
                ds.append(pickle.load(f))
            except EOFError:
                f.close()
                break

loaddset("my.dat")
#calculating distance b/w two wavesof an audio file
def dis(instance1 , instance2 , k ):
    dis =0 
    mm1 = instance1[0] 
    cm1 = instance1[1]
    mm2 = instance2[0]
    cm2 = instance2[1]
    dis = np.trace(np.dot(np.linalg.inv(cm2), cm1)) 
    dis+=(np.dot(np.dot((mm2-mm1).transpose() , np.linalg.inv(cm2)) , mm2-mm1 )) 
    dis+= np.log(np.linalg.det(cm2)) - np.log(np.linalg.det(cm1))
    dis-= k
    return dis

def getNeighbors(trainingSet , instance , k):
    distances =[]
    for x in range (len(trainingSet)):
        dist = dis(trainingSet[x], instance, k )+ dis(instance, trainingSet[x], k)
        distances.append((trainingSet[x][2], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors  

def nearestClass(neighbors):
    classVote ={}
    for x in range(len(neighbors)):
        response = neighbors[x]
        if response in classVote:
            classVote[response]+=1 
        else:
            classVote[response]=1 
    sorter = sorted(classVote.items(), key = operator.itemgetter(1), reverse=True)
    return sorter[0][0]


results=defaultdict(int)
#data set of 1.26 gb consists of 10 genres of 100 wave files each 
i=1
for folder in os.listdir("./data/genres/"):
    results[i]=folder
    i+=1
#testing with different files
(rate,sig)=wavefile.read("starWars60.wav")
mfcc_feat=mfcc(sig,rate,winlen=0.020,appendEnergy=False)
covariance = np.cov(np.matrix.transpose(mfcc_feat))
mean_matrix = mfcc_feat.mean(0)
feature=(mean_matrix,covariance,0)
pred=nearestClass(getNeighbors(ds ,feature , 5))
print(results[pred])
