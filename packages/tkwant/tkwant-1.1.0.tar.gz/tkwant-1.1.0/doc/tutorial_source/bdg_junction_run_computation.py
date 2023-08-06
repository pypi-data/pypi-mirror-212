# Script 1/2 to produce the figure in Tkwant's tutorial
# "Self-consistent Tkwant: a generic solver for time-dependent mean field calculations"
# in the section on Microscopic Bogoliubov-deGennes equations.
#
# Step 1: run this script (preferably on a cluster using MPI parallelization)
# Step 2: plot the results by running the script bdg_junction_plot_results.py
#
import tkwant
import kwant
import kwantspectrum

import cmath
import numpy as np
import scipy.integrate
import scipy.interpolate
import functools
import tinyarray
import pickle


comm = tkwant.mpi.get_communicator()

sx = tinyarray.array([[0, 1], [1, 0]], complex)
sz = tinyarray.array([[1, 0], [0, -1]], complex)
sa = tinyarray.array([[1, 0], [0, 0]], complex)
sb = tinyarray.array([[0, 0], [0, 1]], complex)

# parameters for pulse
tmax = 1000
tau = 100
delta = 0.1
U = 2
Ef = 0
w0 = delta
dV = w0 / (2 * tmax - tau)
taupi2 = tau**2 / np.pi**2


def V0(t):
    if t < tau:
        return dV * (t - np.sin(t / tau * np.pi) * tau / np.pi)
    else:
        return 2 * dV * (t - 0.5 * tau)


def phi0(t):
    if t < tau:
        return dV * (0.5 * t**2 + (np.cos(t / tau * np.pi) - 1) * taupi2)
    else:
        return dV * (t**2 - tau * t + 0.5 * tau**2 - taupi2)


def make_SNS_system(delta, U, Ef):

    # system building
    lat = kwant.lattice.square(a=1, norbs=2)
    syst = kwant.Builder()

    # central scattering region
    onsite_N = (U - Ef) * sz
    onsite_S = - Ef * sz + delta * sx
    syst[lat(-1, 0)] = onsite_S
    syst[lat(0, 0)] = onsite_N
    syst[lat(1, 0)] = onsite_S
    syst[lat.neighbors()] = sz

    # add leads
    lead_left = kwant.Builder(kwant.TranslationalSymmetry((-1, 0)))
    lead_left[lat(0, 0)] = onsite_S
    lead_left[lat.neighbors()] = sz
    syst.attach_lead(lead_left)
    syst.attach_lead(lead_left.reversed())

    return syst, lat


class BdGPotential:
    """A class to calculate Q(t) for the Bogoliubov-deGennes equations"""

    def __init__(self, syst, lat, w0, q, r):

        self._a = w0 / q
        self._b = w0**2
        self._c = r * w0 / q
        self._phi_init = 0
        self._v_init = 0
        self._tmin = 0
        self._tmax = 0
        self.time = []
        self.current = []
        self.phi = []
        self.v = []

        # Prepare a self-consistent hamiltonian matrix Q(t) with non-zero
        # 2x2 submatrix between site -1 and 0
        self._qt = tkwant.system.Hamiltonian(syst, hopping=(lat(0, 0), lat(-1, 0)))

    def prepare(self, current_func, tmax):
        """Pre-calculate the interaction contribution Q(t)"""
        self._tmin = self._tmax
        self._tmax = tmax

        # time grid for the solution/interpolation of the BdG differential equation
        times = np.linspace(self._tmin, self._tmax, num=4)

        def calc_rhs(tt, yy):  # right-hand-side of the BdG differential equation
            phi, v = yy
            return [v, - self._a * v - self._b * phi + self._c * current_func(tt)]

        # solve the BdG differential equation: d(phi, V) / dt = rhs
        dgl = scipy.integrate.ode(calc_rhs).set_integrator('dopri5')
        dgl.set_initial_value([self._phi_init, self._v_init], self._tmin)

        phi = [self._phi_init]
        for time in times[1:]:
            result = dgl.integrate(time)
            assert dgl.successful(), 'ode integration problem'
            phi.append(result[0])

        # save I(t), phi(t), V(t)
        # which are current, phase and voltage trought the classical circuit
        self.time.append(self._tmin)
        self.current.append(current_func(self._tmin))
        self.phi.append(self._phi_init)
        self.v.append(self._v_init)

        # initial values for the next update step
        self._phi_init = result[0]
        self._v_init = result[1]

        # interpolate phi(t) for t in [tmin, tmax]
        self._phi_func = scipy.interpolate.interp1d(times, phi, kind='cubic')

    def evaluate(self, time):
        """Return the interaction contribution Q(t) evaluated at time t in [tmin, tmax]"""
        phi_j = phi0(time) - self._phi_func(time)  # phi_j is the phase trough the junction
        ephi = cmath.exp(- 1j * phi_j) - 1
        qmat = ephi * sa - ephi.conjugate() * sb  # subblock of self-consistent matrix Q(t)
        return self._qt.get(qmat)


def main():

    # initialize the tight-binding system
    syst, lat = make_SNS_system(delta, U, Ef)
    syst = syst.finalized()

    # set chemical potential and zero temperature (default)
    occupations = tkwant.manybody.lead_occupation(chemical_potential=Ef)

    # calculate the spectrum E(k) for all leads
    spectra = kwantspectrum.spectra(syst.leads)

    # define boundary conditions, set upper cutoff energy to Ef
    boundaries = tkwant.leads.automatic_boundary(spectra, tmax, emax=Ef)

    # calculate the k intervals for the quadrature
    interval_type = functools.partial(tkwant.manybody.Interval, order=20,
                                      quadrature='gausslegendre')
    intervals = tkwant.manybody.calc_intervals(spectra, occupations, interval_type)
    intervals = tkwant.manybody.split_intervals(intervals, number_subintervals=40)

    # calculate all onebody scattering states at t = 0
    tasks = tkwant.manybody.calc_tasks(intervals, spectra, occupations)
    psi_init = tkwant.manybody.calc_initial_state(syst, tasks, boundaries)

    # set up the manybody wave function
    wave_function = tkwant.manybody.WaveFunction(psi_init, tasks)

    # measure the current from the center (site 0) to the right lead (site 1)
    current_operator = kwant.operator.Current(syst, onsite=sz,
                                              where=[(lat(1, 0), lat(0, 0))])

    # self-consistent potential
    bdg_potential = BdGPotential(syst, lat, w0=w0, q=20, r=3*np.sqrt(2))

    # set up the self-consistent interacting manybody wave function
    sc_wavefunc = tkwant.interaction.SelfConsistentState(wave_function,
                                                         current_operator,
                                                         bdg_potential)

    # evolve the interacting wave function up to tmax
    sc_wavefunc.evolve(tmax)

    # save the result
    if comm.rank == 0:

        v0t = [V0(t) for t in bdg_potential.time]

        results = {}
        results['times'] = np.array(bdg_potential.time)
        results['current'] = np.array(bdg_potential.current)
        results['phi'] = np.array(bdg_potential.phi)
        results['v'] = np.array(bdg_potential.v)
        results['v0t'] = np.array(v0t)
        results['delta'] = delta
        pickle.dump(results, open('self_consistent_bdg_data.npy', "wb"))


if __name__ == '__main__':
    main()
