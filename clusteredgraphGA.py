__author__ = 'spawar'
import numpy as np
import matplotlib.pyplot as plt







data=np.loadtxt('/nfs/student/s/spawar/Downloads/iAnt-ARGoS-master/clustered_13.txt', delimiter=',')

print data
x1 = data[:,8]
y1= data[:,7]*1000/256



plt.plot(x1,y1)
plt.xlabel("Generations")
plt.ylabel(" % Efficiency")
plt.title('GA evolution of CPFA parametrs for Clustered Distribution')
plt.show()

