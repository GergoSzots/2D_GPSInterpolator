import numpy as np
import matplotlib.pyplot as plt
#read in the text file which contains electr.num and its coordinates
#TODO: 1. filepath megcsinálni, 2. beolvasni a nyers adatot, vesszős, 3. van h méterben van az elektróda...
#TODO ...van hogy elektródaszámmal van jelezve, ezt lekezelni.
#TODO: topo filet is nyomja ki egyben a prosyshez
#TODO: ha a file EOVben van x-y megcserélni
line_nr = "13" #ÁTÍRNI A MEGFELELŐ NÉVRE
electrode_distance = 1
"""filepath = r'D:\Gergo\Projektek\2022_002_TokajIP\ip_' + line_nr + r'\mad_ip_' + \
            line_nr + r'_gps_input.txt'
"""

filepath = r'D:\Gergo\Projektek\2022_003_Tokaj1m\ert_7\mad_1m_07_gps_input.txt'

data_in = np.loadtxt(filepath,skiprows=0)
data_in = data_in[np.argsort(data_in[:,0])]
np.set_printoptions(suppress=True)
print(data_in)

A_interpolalt = []

for i in range(0,len(data_in)-1):
    #print("ciklusss" + str(i))
    A_temp = np.zeros((int(data_in[i + 1, 0] - data_in[i, 0]), 4))
    for j in range(0,(int(data_in[i+1,0]-data_in[i,0]))):
        if j == 0:
            A_temp[0,:] = data_in[i,:]
        else:
            A_temp[j,:] = A_temp[j-1,:] + (data_in[i+1,:] - data_in[i,:]) / int(data_in[i+1,0]-data_in[i,0])
    A_interpolalt = np.append(A_interpolalt,A_temp)

A_interpolalt = np.append(A_interpolalt,data_in[-1,:])
A_interpolalt = np.resize(A_interpolalt,(int(data_in[-1,0]),4))

print(A_interpolalt)
"""
out_name = r'D:\Gergo\Projektek\2022_002_TokajIP\ip_' + line_nr + r'\mad_ip_' + \
            line_nr + r'_gps_interpol.txt'
"""
out_name = r'D:\Gergo\Projektek\2022_003_Tokaj1m\ert_7\ert_07_gps_interpolalt.txt'
np.savetxt(out_name, A_interpolalt,
           delimiter='\t', fmt='%.2f', header='#\tX\tY\tZ', comments='')

#ha nem kell y korrekció, de topo file attól ég kell, ezt a mátrixot használjuk:
A_topo = np.zeros((len(A_interpolalt),4))
A_topo[:,0] = A_interpolalt[:,0]
A_topo[:,3] = A_interpolalt[:,3]
for i in range(0,len(A_topo)):
    A_topo[i,1] = (A_topo[i,0]-1) * electrode_distance


"""
out_name2 = r'D:\Gergo\Projektek\2022_002_TokajIP\ip_' + line_nr + r'\mad_ip_' + \
            line_nr + r'_topo.txt'
"""

out_name2 = r'D:\Gergo\Projektek\2022_003_Tokaj1m\ert_7\ert07_topo.txt'
np.savetxt(out_name2, A_topo,
           delimiter='', fmt='%.0f,%.2f,%.2f,%.2f', header='#,X,Y,Z', comments='')


fig, ax = plt.subplots()
ax.plot(A_interpolalt[:,2],A_interpolalt[:,1], linewidth=3)
ax.set_title("Interpolált koords", fontsize=14)
ax.set_xlabel("X coord", fontsize=14)
ax.set_ylabel("Y coord", fontsize=14)
ax.tick_params(axis='both', labelsize=4)

ax.scatter(data_in[:,2], data_in[:,1], c='red', s=30)
plt.show()
