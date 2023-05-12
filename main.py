import numpy as np
import matplotlib.pyplot as plt
#read in the text file which contains electr.num and its coordinates
#TODO: 1. filepath megcsinálni, 2. beolvasni a nyers adatot, vesszős, 3. van h méterben van az elektróda...
#TODO ...van hogy elektródaszámmal van jelezve, ezt lekezelni.

line_nr = "01" #the name of the ERT line
electrode_distance = 1 #electrode distance used in the measurement

location = "D:\Gergo\Python\gpsInterpolator\\" #folder's location that contains the gps input files

filepath = location + r'ert_line_' + line_nr + r'_gps_input.txt'

data_in = np.loadtxt(filepath,skiprows=0)
data_in = data_in[np.argsort(data_in[:,0])]
np.set_printoptions(suppress=True)
#print(data_in) checking the input if needed

A_interpol = [] #This matrix will hold the interpolated coordinates

for i in range(0,len(data_in)-1):
    A_temp = np.zeros((int(data_in[i + 1, 0] - data_in[i, 0]), 4))
    for j in range(0,(int(data_in[i+1,0]-data_in[i,0]))):
        if j == 0:
            A_temp[0,:] = data_in[i,:]
        else:
            A_temp[j,:] = A_temp[j-1,:] + (data_in[i+1,:] - data_in[i,:]) / int(data_in[i+1,0]-data_in[i,0])
    A_interpol = np.append(A_interpol, A_temp)

A_interpol = np.append(A_interpol, data_in[-1, :])
A_interpol = np.resize(A_interpol, (int(data_in[-1, 0]), 4))

#print(A_interpol)

out_name = location + r'ert_line_' + line_nr + r'_gps_interpol.txt' #this will be your interpolated coordinates

np.savetxt(out_name, A_interpol,
           delimiter='\t', fmt='%.2f', header='#\tX\tY\tZ', comments='')

#This will be the topography file for Prosys III
A_topo = np.zeros((len(A_interpol), 4))
A_topo[:,0] = A_interpol[:, 0]
A_topo[:,3] = A_interpol[:, 3]
for i in range(0,len(A_topo)):
    A_topo[i,1] = (A_topo[i,0]-1) * electrode_distance



out_name = location + r'ert_line_' + line_nr + r'_topo.txt'



np.savetxt(out_name, A_topo,
           delimiter='', fmt='%.0f,%.2f,%.2f,%.2f', header='#,X,Y,Z', comments='')


fig, ax = plt.subplots()
ax.plot(A_interpol[:, 2], A_interpol[:, 1], linewidth=3)
ax.set_title("Interpolált koords", fontsize=14)
ax.set_xlabel("X coord", fontsize=14)
ax.set_ylabel("Y coord", fontsize=14)
ax.tick_params(axis='both', labelsize=4)

ax.scatter(data_in[:,2], data_in[:,1], c='red', s=30)
plt.show()
