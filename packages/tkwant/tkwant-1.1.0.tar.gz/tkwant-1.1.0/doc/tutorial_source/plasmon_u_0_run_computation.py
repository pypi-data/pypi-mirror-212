# Script 1/3 to produce the figure in Tkwant's tutorial
# "Self-consistent Tkwant: a generic solver for time-dependent mean field calculations"
# in the section on Luttinger liquids.
#
# Step 1: run the two simulation (plasmon_u_0_computation.py, plasmon_u_10_computation.py)
#         preferably on a cluster using MPI
# Step 2: plot the data (plasmon_plot_results.py)
#
import tkwant
import kwant
import kwantspectrum

import functools
import numpy as np
import scipy
import cmath
import sys
import pickle

import logging
tkwant.logging.level = logging.INFO  # possible levels (increasing verbosity): WARNING, INFO, DEBUG

# --- MPI helper routines


def am_master():
    """Return true for the MPI master rank"""
    return tkwant.mpi.get_communicator().rank == 0


def print_master(*args, **kwargs):
    if am_master():
        print(*args, **kwargs)
    sys.stdout.flush()


# --- Non-interacting Kwant system

def phi(time):
    t0 = 200
    A = 0.1 * np.pi
    sigma = 60.056120439
    return A * (1 + scipy.special.erf((time - t0) / sigma))


# time dependent coupling with gaussian pulse
def gamma_t(site1, site2, time):
    return - cmath.exp(- 1j * phi(time))


def make_system(L=3000):

    # system building
    lat = kwant.lattice.square(a=1, norbs=1)
    syst = kwant.Builder()

    # central scattering region
    syst[(lat(x, 0) for x in range(-L, L))] = 0
    syst[lat.neighbors()] = -1
    syst[lat(0, 0), lat(-1, 0)] = gamma_t

    # add leads
    sym = kwant.TranslationalSymmetry((-1, 0))
    lead_left = kwant.Builder(sym)
    lead_left[lat(0, 0)] = 0
    lead_left[lat.neighbors()] = -1
    syst.attach_lead(lead_left)
    syst.attach_lead(lead_left.reversed())

    return syst


# --- Interaction

class Potential:
    def prepare(self, ft, tmax):
        self._ft = ft

    def evaluate(self, time):
        diag = self._ft(time)
        return scipy.sparse.diags([diag], [0], dtype=complex)


class HartreeOperator:
    """An operator to calculate the Hartree potential Q(t) = U (n(t) - n(0))"""
    def __init__(self, density_operator, interaction_strength, density0):
        self._density_operator = density_operator
        self._interaction_strength = interaction_strength
        self._density0 = density0

    def __call__(self, bra, ket=None, args=(), *, params=None):
        """API similar to a Kwant operator"""
        density = self._density_operator(bra, ket, args, params=params)
        return (density - self._density0) * self._interaction_strength


syst = make_system().finalized()

sites = [site.pos[0] for site in syst.sites]
times = [500, 700, 900, 1100]
u = 0  # interaction strength

# calculate the spectrum E(k) for all leads
spectra = kwantspectrum.spectra(syst.leads)

# set the chemical potential in the leads
occupations = tkwant.manybody.lead_occupation(chemical_potential=-1)
emin, emax = tkwant.manybody.calc_energy_cutoffs(occupations)

# define boundary conditions
bdr = tkwant.leads.automatic_boundary(spectra, tmax=max(times), emin=emin, emax=emax)

# calculate the k intervals for the quadrature
interval_type = functools.partial(tkwant.manybody.Interval, order=20,
                                  quadrature='gausslegendre')
intervals = tkwant.manybody.calc_intervals(spectra, occupations, interval_type)
intervals = tkwant.manybody.split_intervals(intervals, number_subintervals=60)

# calculate all onebody scattering states at t = 0
tasks = tkwant.manybody.calc_tasks(intervals, spectra, occupations)
psi_init = tkwant.manybody.calc_initial_state(syst, tasks, bdr)

# set up the non-interacting manybody wave function
wave_function = tkwant.manybody.WaveFunction(psi_init, tasks)

density_operator = kwant.operator.Density(syst)

density0 = wave_function.evaluate(density_operator)

densities = []
for time in times:
    print_master('time= {}'.format(time))
    wave_function.evolve(time)
    density = wave_function.evaluate(density_operator)
    if am_master():
        density -= density0
    densities.append(density)

results = {}
results['densities'] = densities
results['times'] = times
results['sites'] = sites

#  write the result into a file
if am_master():
    filename = 'plasmon_u_{}_data.npy'.format(u)
    pickle.dump(results, open(filename, "wb"))
