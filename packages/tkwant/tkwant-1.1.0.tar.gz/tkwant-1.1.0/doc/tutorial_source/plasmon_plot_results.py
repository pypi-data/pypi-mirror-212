# Script 3/3 to produce the figure in Tkwant's tutorial
# "Self-consistent Tkwant: a generic solver for time-dependent mean field calculations"
# in the section on Luttinger liquids.
#
# Step 1: run the two simulation (plasmon_u_0_computation.py, plasmon_u_10_computation.py)
#         preferably on a cluster using MPI
# Step 2: plot the data (plasmon_plot_results.py)
#
import matplotlib.pyplot as plt
import numpy as np
import pickle
import pylab


fac = 6
fontsize = 45


pylab.rcParams['figure.figsize'] = (fac * np.sqrt(2), fac)
plt.rcParams.update({'font.size': fontsize})
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


# ----no interactions
data = pickle.load(open('plasmon_u_0_data.npy', 'rb'))

t = np.array(data['times'])
x = np.array(data['sites'])
z = np.array(data['densities'])

for i, (time, density) in enumerate(zip(t, z)):
    plt.plot(x, 280000 * density + time, '--', color='black')

# ---- with interactions
data = pickle.load(open('plasmon_u_10_data.npy', 'rb'))

t = np.array(data['times'])
x = np.array(data['sites'])
z = np.array(data['densities'])

for i, (time, density) in enumerate(zip(t, z)):
    plt.plot(x, 800000 * density + time, color='black')

v0 = np.sqrt(3)
g = 10
v = v0 * np.sqrt(1 + g / (np.pi * v0))

t0 = 350

plt.ylabel(r'time $t$', fontsize=fontsize)
plt.xlabel(r'site $i$', fontsize=fontsize)

xx = x[3000:6000]
plt.plot([0, max(xx)], [t0, t0 + max(xx)/(v0)], '--b')
plt.plot([0, max(xx)], [t0, t0 + max(xx)/(v)], 'b')

axes = plt.gca()
axes.set_xlim([0, 3000])
axes.set_ylim([500, 1300])
axes.set_xticks([0, 1000, 2000, 3000])
axes.set_yticks([500, 700, 900, 1100])
plt.text(1350, 1320, r'$U=0$')
plt.text(2450, 1320, r'$U=10$')

plt.savefig("plasmon_propagation.png", bbox_inches='tight')

plt.show()
