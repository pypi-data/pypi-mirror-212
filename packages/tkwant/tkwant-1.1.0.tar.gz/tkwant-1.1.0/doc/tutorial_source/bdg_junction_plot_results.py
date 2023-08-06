# Script 2/2 to produce the figure in Tkwant's tutorial
# "Self-consistent Tkwant: a generic solver for time-dependent mean field calculations"
# in the section on Microscopic Bogoliubov-deGennes equations.
#
# Step 1: run the script bdg_junction_run_computation.py (preferably on a cluster using MPI parallelization)
# Step 2: run this script to plot the results
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

data = pickle.load(open('self_consistent_bdg_data.npy', 'rb'))

times = data['times']
vj = data['v0t'] - data['v']
delta = data['delta']

times *= delta
vj *= 1 / delta

plt.plot(times, vj)

plt.xlabel(r"$t\ \mathrm{[\hbar/\Delta]}$", fontsize=fontsize)
plt.ylabel(r"$V_J \ \mathrm{[\Delta/e]}$", fontsize=fontsize)

plt.savefig("bdg_junction_vj_vs_time.png", bbox_inches='tight')

plt.show()
