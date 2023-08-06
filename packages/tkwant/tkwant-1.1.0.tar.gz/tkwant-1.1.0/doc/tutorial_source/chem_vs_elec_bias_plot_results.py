# Script 2/2 to produce the figure in Tkwant's "DC current through a 1D chain" tutorial.
#
# Step 1: run the simulation (chem_vs_elec_bias_run_computation.py)
# Step 2: plot the data (chem_vs_elec_bias_plot_results.py)
#
# This is the script for step 2 to plot the result.
# Make sure that the file containing the result data
# (chem_vs_elec_bias_result_data.npy, produced by running the script for step 1)
# is placed in the same directory as this script.

import matplotlib.pyplot as plt
import pickle
import pylab
import numpy as np

# --- plot settings
markersize = 14

fac = 6
pylab.rcParams['figure.figsize'] = (fac * np.sqrt(2), fac)

plt.rcParams.update({'font.size': 15})
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# --- load data
data = pickle.load(open('./chem_vs_elec_bias_result_data.npy', 'rb'))

# --- plot and store figure
fig, (ax1, ax2) = plt.subplots(2)

for v, res in data.items():
    for ax in [ax1, ax2]:
        ax.plot(v, res['I_vc_sc'], 'x', color='#4e79a7')
        ax.plot(v, res['I_vc_wf'], '+', color='#4e79a7')
        ax.plot(v, res['I_ve_sc'], 'x', color='#f28e2b')
        ax.plot(v, res['I_ve_wf'], '+', color='#f28e2b')
        ax.plot(v, res['I_ve_wf_tr'], '.', color='#f28e2b')

for ax in [ax1, ax2]:
    ax.plot(v, res['I_vc_sc'], 'x', color='#4e79a7', label='(Ia) chem drop, scat')
    ax.plot(v, res['I_vc_wf'], '+', color='#4e79a7', label='(Ib) chem drop, wf')
    ax.plot(v, res['I_ve_sc'], 'x', color='#f28e2b', label='(IIa) el drop, scat')
    ax.plot(v, res['I_ve_wf'], '+', color='#f28e2b', label='(IIb) el drop, wf')
    ax.plot(v, res['I_ve_wf_tr'], '.', color='#f28e2b', label='(IIc) el drop, wf gauge')

    ax.set_ylabel(r'$I (e \gamma / h)$')
    ax.legend(loc=5)

ax2.set_xlabel(r'$V (\gamma)$')

ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xlim([5e-7, 1.5e-1])
ax1.set_ylim([5e-7, 1.5e-1])

plt.savefig("chem_vs_elec_bias_current.png", bbox_inches='tight')

plt.show()
