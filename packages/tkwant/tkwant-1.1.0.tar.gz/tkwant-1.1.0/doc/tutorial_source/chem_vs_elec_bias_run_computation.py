# Script 1/2 to produce the figure in Tkwant's "DC current through a 1D chain" tutorial.
#
# Step 1: run the simulation (chem_vs_elec_bias_run_computation.py)
# Step 2: plot the data (chem_vs_elec_bias_plot_results.py)
#
# This is the script for step 1 to do the kwant/tkwant simulation.
# Run this script preferably on a cluster using MPI parallelization,
# because it will take some time.
# The result from the calculation will be saved to a file.

import tkwant
import kwant

import cmath
import scipy
import numpy as np
import pickle
import sys
import functools


# --- MPI helper routines

def am_master():
    """Return true for the MPI master rank"""
    return tkwant.mpi.get_communicator().rank == 0


def print_master(*args, **kwargs):
    if am_master():
        print(*args, **kwargs)
    sys.stdout.flush()


# --- system definition for electric and chemical potential in steady state regime

def make_system_static(a=1):

    def onsite(site, ve):
        return ve

    # central system
    lat = kwant.lattice.square(a=a, norbs=1)
    syst = kwant.Builder()

    syst[(lat(i, 0) for i in [-1, 0, 1])] = 0
    syst[lat.neighbors()] = -1

    # leads
    lead_left = kwant.Builder(kwant.TranslationalSymmetry((-a, 0)))

    lead_left[lat(0, 0)] = onsite
    lead_left[lat.neighbors()] = -1
    syst.attach_lead(lead_left)

    lead_right = kwant.Builder(kwant.TranslationalSymmetry((-a, 0)))

    lead_right[lat(0, 0)] = 0
    lead_right[lat.neighbors()] = -1

    syst.attach_lead(lead_right.reversed())

    return syst, lat


# --- system definition for electric and chemical potential in transient regime

def coupling_nn(site1, site2, time, ve):
    phi = ve * time
    return - cmath.exp(- 1j * phi)


def make_system_transient(a=1):

    lat = kwant.lattice.square(a=a, norbs=1)
    syst = kwant.Builder()

    syst[(lat(i, 0) for i in [-1, 0, 1])] = 0
    syst[lat.neighbors()] = -1

    # time dependent coupling - e^(-i \phi(t)) c^\dagger_0 c_{-1}
    syst[(lat(0, 0), lat(-1, 0))] = coupling_nn

    lead = kwant.Builder(kwant.TranslationalSymmetry((-a, 0)))
    lead[lat(0, 0)] = 0
    lead[lat.neighbors()] = -1
    syst.attach_lead(lead)
    syst.attach_lead(lead.reversed())

    return syst, lat


# --- current from scattering matrix for electrical and chemical potential

def current_vc(vc):
    return min(2, vc)


def transmission(syst, energy, ve):
    try:
        smatrix = kwant.smatrix(syst, energy=energy, params={"ve": ve})
        res = smatrix.transmission(1, 0)
    except:  # exactly at the band opening, the kwant smatrix crashes
        res = 0
    return res


def current_ve(syst, ve):
    def transfunc(energy):
        return transmission(syst, energy, ve)
    return scipy.integrate.quad(transfunc, 0, ve)[0]


def main():

    # define the system to calculate the steady-state current
    syst_stat, lat = make_system_static()
    syst_stat = syst_stat.finalized()

    # define the system to calculate the transient current
    syst_trans, lat = make_system_transient()
    syst_trans = syst_trans.finalized()

    # parameters
    mu = 0
    tmax = 100

    all_results = {}

    # current from site 0 to site 1
    current_operator = kwant.operator.Current(syst_stat, where=[(lat(1, 0), lat(0, 0))])

    # loop over chemical/electrical potential, vc = ve = v
    potential = np.append(np.logspace(-6, -1, 40), np.linspace(0.1, 5, 50))
    for v in potential:

        print_master('v= {}'.format(v))
        results = {}

        # occupation of left and right lead
        occupations = [tkwant.manybody.lead_occupation(chemical_potential=mu+v),
                       tkwant.manybody.lead_occupation(chemical_potential=mu)]

        # --- (Ia) - chemical potential - scattering matrix
        results['I_vc_sc'] = current_vc(v)

        # --- (Ib) - chemical potential - wave function
        state = tkwant.manybody.State(syst_stat, tmax=1, occupations=occupations, params={"ve": 0})
        current = state.evaluate(current_operator)
        if am_master():
            results['I_vc_wf'] = 2 * np.pi * current

        # --- (IIa) - electrical potential - scattering matrix
        results['I_ve_sc'] = current_ve(syst_stat, v)

        # --- (IIb) - electrical potential - wave function
        state = tkwant.manybody.State(syst_stat, tmax=1, occupations=occupations, params={"ve": v})
        current = state.evaluate(current_operator)
        if am_master():
            results['I_ve_wf'] = 2 * np.pi * current

        # --- (IIc) - electrical potential - wave function - transient regime

        # turn off extrapolation of the time-dependent perturbation
        # this becomes crutial for large values of v
        onebody_wavefunction_type = functools.partial(tkwant.onebody.WaveFunction.from_kwant,
                                                      perturbation_type=tkwant.onebody.kernels.PerturbationExtractor)
        scattering_state_type = functools.partial(tkwant.onebody.ScatteringStates,
                                                  wavefunction_type=onebody_wavefunction_type)

        # defining no occupation corresponds to mu=0 in all leads
        state = tkwant.manybody.State(syst_trans, tmax=tmax, params={'ve': v},
                                      scattering_state_type=scattering_state_type)
        state.evolve(tmax)
        state.refine_intervals()
        current = state.evaluate(current_operator)
        if am_master():
            results['I_ve_wf_tr'] = 2 * np.pi * current

        all_results[v] = results

    #  write the result into a file
    if am_master():
        pickle.dump(all_results, open('chem_vs_elec_bias_result_data.npy', "wb"))


if __name__ == '__main__':
    main()
