import tkwant
import kwant

import numpy as np
import scipy.special
import scipy.integrate
import cmath
import functools as ft
import matplotlib.pyplot as plt

import sys
import pickle

import logging
tkwant.logging.level = logging.INFO  # possible levels (increasing verbosity): WARNING, INFO, DEBUG

comm = tkwant.mpi.get_communicator()


def am_master():
    return comm.rank == 0


def print_master(*args, **kwargs):
    if am_master():
        print(*args, **kwargs)
    sys.stdout.flush()

# parameters
gamma = 0.1  # coupling
epsilon = 0.1  # onsite element
time0 = 100

times = np.linspace(0, 200, 201)


def gamma_t(site1, site2, time):
    # time dependent coupling function \gamma(t) = \Theta(t) * gamma
    if time <= 0:
        return 0
    return - gamma


def make_siam_system(gt, epsilon):

    # system building
    lat = kwant.lattice.square(a=1, norbs=1)
    syst = kwant.Builder()

    # central scattering region
    syst[(lat(x, 0) for x in [-1, 0, 1])] = 0
    syst[lat(0, 0)] = epsilon

    syst[(lat(0, 0), lat(-1, 0))] = gt
    syst[(lat(1, 0), lat(0, 0))] = gt

    # add leads
    sym = kwant.TranslationalSymmetry((-1, 0))
    lead_left = kwant.Builder(sym)
    lead_left[lat(0, 0)] = 0
    lead_left[lat.neighbors()] = -1
    syst.attach_lead(lead_left)
    syst.attach_lead(lead_left.reversed())

    return syst, lat

# Switch off perturbation interpolation for sudden switch
onebody_wavefunction_type = ft.partial(tkwant.onebody.WaveFunction.from_kwant,
                                       perturbation_type=tkwant.onebody.kernels.PerturbationExtractor)

scattering_state_type = ft.partial(tkwant.onebody.ScatteringStates,
                                   wavefunction_type=onebody_wavefunction_type)

# --- Tkwant simulation for the dynamics of G^<(t, t0)

syst, lat = make_siam_system(gamma_t, epsilon)
syst = syst.finalized()

green = tkwant.manybody.GreenFunction(syst, max(times),
                                      scattering_state_type=scattering_state_type)

green_less = []

for time in times:

    print_master('time= {}'.format(time))

    green.evolve(time, time0)
    green.refine_intervals()
    green_less.append(green.lesser(1, 1))


# --- Tkwant simulation for the dynamics G^<(t, t)

density_operator = kwant.operator.Density(syst, where=[lat(0, 0)])

green = tkwant.manybody.GreenFunction(syst, max(times),
                                      scattering_state_type=scattering_state_type)

state = tkwant.manybody.State(syst, max(times),
                              scattering_state_type=scattering_state_type)

green_less_tt = []
nt = []

for time in times:

    print_master('time= {}'.format(time))

    green.evolve(time, time)
    green.refine_intervals()
    green_less_tt.append(green.lesser(1, 1))

    state.evolve(time)
    state.refine_intervals()
    nt.append(state.evaluate(density_operator))


# --- Tkwant simulation for the equilibrium density

syst_eq, lat = make_siam_system(gamma, epsilon)
syst_eq = syst_eq.finalized()

density_operator = kwant.operator.Density(syst_eq, where=[lat(0, 0)])

state = tkwant.manybody.State(syst_eq, tmax=1)
dens_tkwant_equilibrium = state.evaluate(density_operator)


# --------. Analytica formulas

def n_equilibrium(gamma, epsilon=0):
    # siam equlibrium density on the dot in flatband approx for mu_L = mu = R = 0
    Gamma = 2 * gamma**2
    return np.arctan(- epsilon / Gamma) / np.pi + 0.5


def integrate_quad(func, a, b):

    def func_re(time):
        return func(time).real

    def func_im(time):
        return func(time).imag

    epsabs = 1.49e-8
    epsrel = 1.49e-8
    limit = 5000
    return (scipy.integrate.quad(func_re, a, b, epsabs=epsabs, epsrel=epsrel, limit=limit)[0]
            + 1j * scipy.integrate.quad(func_im, a, b, epsabs=epsabs, epsrel=epsrel, limit=limit)[0])


def green_lesser_flatband(t0, t1, gamma, epsilon=0):
    # siam G^< on the dot in flatband approx for mu_L = mu = R = 0 after sudden switching of the leads
    # using analytical fourier tranform
    if t0 <= 0 or t1 <= 0:
        return 0
    Gamma = 2 * gamma**2
    iless = tkwant.special._iless  # I^<_t(a) =  - \int_{-\infty}^{0} d \omega \frac{e^{- i \omega t}}{\omega - a}

    def it(t):
        return iless(epsilon - 1j * Gamma, t) - iless(epsilon + 1j * Gamma, t)

    neq = n_equilibrium(gamma, epsilon)
    if t0 == t1:
        return (1j * neq * (1 + np.exp(- 2 * Gamma * t0)) - 0.5 / np.pi * np.exp(- Gamma * t0)
                * (cmath.exp(1j * epsilon * t0) * it(t0) + cmath.exp(-1j * epsilon * t0) * it(-t0)))
    return 0.5 / np.pi * (it(t0 - t1)
                          + 2 * np.pi * 1j * cmath.exp(-1j * epsilon * (t0 - t1) - Gamma * (t0 + t1)) * neq
                          - cmath.exp(1j * epsilon * t1 - Gamma * t1) * it(t0)
                          - cmath.exp(-1j * epsilon * t0 - Gamma * t0) * it(-t1))


def green_lesser_flatband_num(t0, t1, gamma, epsilon=0):
    # siam G^< on the dot in flatband approx for mu_L = mu = R = 0 after sudden switching of the leads
    # using numerical fourier transform
    if t0 <= 0 or t1 <= 0:
        return 0
    Gamma = 2 * gamma**2

    def integrand_n(w):
        y = w - epsilon
        return (cmath.exp(-1j * t0 * y + Gamma * t0) - 1) * (cmath.exp(1j * t1 * y + Gamma * t1) - 1) / (Gamma**2 + y**2)
    fac = 1j * Gamma / np.pi * cmath.exp(-1j * epsilon * (t0 - t1)) * np.exp(- Gamma * (t0 + t1))
    return fac * integrate_quad(integrand_n, -100, 0)


def green_lesser_riwar(t0, t1, gamma, epsilon=0):
    # this is the form of the paper Eq. 15
    # R.-P. Riwar and T. L. Schmidt, “Transient dynamics of a molecular quantum dot with a vibrational degree of freedom,” Phys. Rev. B 80,125109 (2009).
    if t0 <= 0 or t1 <= 0:
        return 0
    Gamma = 2 * gamma**2

    def integrand_n(w):
        y = w - epsilon
        return (cmath.exp(-1j * t0 * y) - np.exp(- Gamma * t0)) * (cmath.exp(1j * t1 * y) - np.exp(- Gamma * t1)) / (Gamma**2 + y**2)
    fac = 1j * Gamma / np.pi
    return fac * integrate_quad(integrand_n, -100, 0)


dens_flatband_equilibrium = n_equilibrium(gamma, epsilon)
gless_tt_flatband = np.array([green_lesser_flatband(t, t, gamma, epsilon) for t in times])
gless_tt0_flatband = np.array([green_lesser_flatband(t, time0, gamma, epsilon) for t in times])
gless_tt_flatband_num = np.array([green_lesser_flatband_num(t, t, gamma, epsilon) for t in times])
gless_tt0_flatband_num = np.array([green_lesser_flatband_num(t, time0, gamma, epsilon) for t in times])
gless_tt_riwar = np.array([green_lesser_riwar(t, t, gamma, epsilon) for t in times])
gless_tt0_riwar = np.array([green_lesser_riwar(t, time0, gamma, epsilon) for t in times])


# --------------- Store result

results = {}
results['times'] = times
results['gamma'] = gamma
results['epsilon'] = epsilon
results['t0'] = time0

results['gless_tt0_tkwant'] = np.array(green_less)
results['gless_tt_tkwant'] = np.array(green_less_tt)
results['n_t_tkwant'] = np.array(nt)
results['dens_tkwant_equilibrium'] = dens_tkwant_equilibrium

results['gless_tt_flatband'] = gless_tt_flatband
results['gless_tt0_flatband'] = gless_tt0_flatband
results['gless_tt_flatband_num'] = gless_tt_flatband_num
results['gless_tt0_flatband_num'] = gless_tt0_flatband_num
results['dens_flatband_equilibrium'] = dens_flatband_equilibrium

results['gless_tt_riwar'] = gless_tt_riwar
results['gless_tt0_riwar'] = gless_tt0_riwar

if am_master():
    pickle.dump(results, open('siam_sudden_switch_data.npy', "wb"))
