import pickle
import pylab

import numpy as np

import matplotlib.pyplot as plt


# --- plot settings
markersize = 14

fac = 8
pylab.rcParams['figure.figsize'] = (fac * np.sqrt(2), fac)

plt.rcParams.update({'font.size': 16})
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

colors = {0: '#e15759', 1: '#f28e2b', 2: '#4e79a7', 3: '#76b7b2', 4: '#59a14f',
          5: '#edc948', 6: '#b07aa1', 7: '#ff9da7', 8: '#9c755f', 9: '#bab0ac'}


# --- read the data
data = pickle.load(open('./siam_sudden_switch_data.npy', 'rb'))

times = data['times']
t0 = data['t0']

gless_tt0_tkwant = data['gless_tt0_tkwant']
gless_tt0_flatband = data['gless_tt0_flatband']
gless_tt0_flatband_num = data['gless_tt0_flatband_num']
gless_tt0_riwar = data['gless_tt0_riwar']
n_eq_tkwant = data['dens_tkwant_equilibrium']

gless_tt_tkwant = data['gless_tt_tkwant']
n_t_tkwant = data['n_t_tkwant']
gless_tt_flatband = data['gless_tt_flatband']
gless_tt_flatband_num = data['gless_tt_flatband_num']
gless_tt_riwar = data['gless_tt_riwar']
n_eq_flatband = data['dens_flatband_equilibrium']


# --- plot figure
fig, ax = plt.subplots(1, 2)
fig.set_size_inches(16, 5)

plt.suptitle(r'check numerical fourier transform vs analytical form $\gamma={}, \epsilon={}, t_0={}$'.
             format(data['gamma'], data['epsilon'], t0), size=22)

ax[0].plot(times, gless_tt0_flatband_num.real, color=colors[0], label=r'$\Re G^<(t, t_0)$ flatband num Fourier')
ax[0].plot(times, gless_tt0_flatband_num.imag, color=colors[1], label=r'$\Im G^<(t, t_0)$ flatband num Fourier')
ax[0].plot(times, gless_tt0_flatband.real, '--', color=colors[2], label=r'$\Re G^<(t, t_0)$ flatband')
ax[0].plot(times, gless_tt0_flatband.imag, '--', color=colors[3], label=r'$\Im G^<(t, t_0)$ flatband')

ax[0].set_xlabel(r'time $t$')
ax[0].set_ylabel(r'$G^<(t, t_0)$')
ax[0].set_xlim(0, times[-1])
ax[0].legend(fontsize=14)

ax[1].plot(times, gless_tt_flatband_num.imag, color=colors[0], label=r'$- i G^<(t, t)$ flatband num Fourier')
ax[1].plot(times, gless_tt_flatband.imag, '--', color=colors[2], label=r'$- i G^<(t, t)$ flatband')
ax[1].plot([0, times[-1]], [n_eq_flatband] * 2, linestyle='dotted', color=colors[1], label=r'$n_{eq}$ flatband')

ax[1].set_xlabel(r'time $t$')
ax[1].set_ylabel(r'$n(t)$')
ax[1].set_xlim(0, times[-1])
ax[1].legend(fontsize=14)

plt.show()

fig, ax = plt.subplots(1, 2)
fig.set_size_inches(16, 5)

plt.suptitle(r'compare result against formula from riwar/schmidt $\gamma={}, \epsilon={}, t_0={}$'.
             format(data['gamma'], data['epsilon'], t0), size=22)

ax[0].plot(times, gless_tt0_riwar.real, color=colors[0], label=r'$\Re G^<(t, t_0)$ flatband riwar')
ax[0].plot(times, gless_tt0_riwar.imag, color=colors[1], label=r'$\Im G^<(t, t_0)$ flatband riwar')
ax[0].plot(times, gless_tt0_flatband.real, '--', color=colors[2], label=r'$\Re G^<(t, t_0)$ flatband')
ax[0].plot(times, gless_tt0_flatband.imag, '--', color=colors[3], label=r'$\Im G^<(t, t_0)$ flatband')

ax[0].set_xlabel(r'time $t$')
ax[0].set_ylabel(r'$G^<(t, t_0)$')
ax[0].set_xlim(0, times[-1])
ax[0].legend(fontsize=14)

ax[1].plot(times, gless_tt_riwar.imag, color=colors[0], label=r'$- i G^<(t, t)$ flatband riwar')
ax[1].plot(times, gless_tt_riwar.imag, '--', color=colors[2], label=r'$- i G^<(t, t)$ flatband')
ax[1].plot([0, times[-1]], [n_eq_flatband] * 2, linestyle='dotted', color=colors[1], label=r'$n_{eq}$ flatband')

ax[1].set_xlabel(r'time $t$')
ax[1].set_ylabel(r'$n(t)$')
ax[1].set_xlim(0, times[-1])
ax[1].legend(fontsize=14)

plt.show()


fig, ax = plt.subplots(1, 2)
fig.set_size_inches(16, 5)

ax[0].plot(times, gless_tt0_tkwant.real, color=colors[0], label=r'$\Re G^<(t, t_0)$ Tkwant')
ax[0].plot(times, gless_tt0_tkwant.imag, color=colors[1], label=r'$\Im G^<(t, t_0)$ Tkwant')
ax[0].plot(times, gless_tt0_flatband.real, linestyle='dotted', lw=3, color=colors[2], label=r'$\Re G^<(t, t_0)$ flatband')
ax[0].plot(times, gless_tt0_flatband.imag, linestyle='dotted', lw=3, color=colors[3], label=r'$\Im G^<(t, t_0)$ flatband')
ax[0].plot(t0, n_eq_tkwant, 'x', markersize=12, color=colors[1], label=r'$n_{eq}$ Tkwant')
ax[0].plot(t0, n_eq_flatband, 'x', markersize=12, color=colors[3], label=r'$n_{eq}$ flatband')

ax[0].set_xlabel(r'time $t$')
ax[0].set_ylabel(r'$G^<(t, t_0)$')
ax[0].set_xlim(0, times[-1])
ax[0].legend(fontsize=14)

ax[1].plot(times, gless_tt_tkwant.imag, color=colors[0], label=r'$- i G^<(t, t)$ Tkwant')
ax[1].plot(times, gless_tt_flatband.imag, color=colors[1], label=r'$- i G^<(t, t)$ flatband')
ax[1].plot(times, n_t_tkwant, linestyle='dotted', lw=3, color=colors[2], label=r'$n(t)$ Tkwant')
ax[1].plot([0, times[-1]], [n_eq_tkwant] * 2, linestyle='dashed', color=colors[2], label=r'$n_{eq}$ Tkwant')
ax[1].plot([0, times[-1]], [n_eq_flatband] * 2, linestyle='dashed', color=colors[1], label=r'$n_{eq}$ flatband')

ax[1].set_xlabel(r'time $t$')
ax[1].set_ylabel(r'$n(t)$')
ax[1].set_xlim(0, times[-1])

ax[1].legend(fontsize=14)

plt.savefig("fig_siam_sudden_switch.png", bbox_inches='tight')
plt.show()
