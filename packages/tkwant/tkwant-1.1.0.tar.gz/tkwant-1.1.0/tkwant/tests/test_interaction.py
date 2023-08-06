import pytest
import numpy as np
import kwant
from numpy.testing import (assert_array_almost_equal, assert_almost_equal)
from scipy.special import erf
import functools
import kwantspectrum
import scipy

from .. import interaction, manybody, leads, onebody


def create_system(a=1, L=20, W=1):
    gamma = 1 / a**2

    # === onsite function definitions ===
    def onsite(time):
        return 4 * gamma

    # === System Building ===
    lat = kwant.lattice.square(a=a, norbs=1)
    syst = kwant.Builder()

    # main part of system
    syst[(lat(x, y) for x in range(L) for y in range(W))] = onsite
    syst[lat.neighbors()] = -gamma

    sym = kwant.TranslationalSymmetry((-a, 0))
    lead_left = kwant.Builder(sym)
    lead_left[(lat(0, y) for y in range(W))] = 4 * gamma
    lead_left[lat.neighbors()] = -gamma

    syst.attach_lead(lead_left)
    syst.attach_lead(lead_left.reversed())

    return syst, lat


def gaussian(time):
    t0 = 50
    A = 0.31415926535
    tau = 12.01122
    return A * (1 + erf((time - t0) / tau))


def test_extrapolation():

    # -- extrapolation of a piecewise flat function

    def g(x):
        if x <= 3:
            return -2
        return 5

    x0 = 1
    tau = 1

    # initial construction at x = 1, extrapolation between [x, x+tau] = [1, 2]
    f_extrapolate = interaction.Extrapolate(g(x0), tau, order=0, x0=x0)

    for y in [1, 1.6, 2]:
        assert_almost_equal(f_extrapolate(y), -2)

    # update at x = 2, extrapolation between [x, x+tau] = [2, 3]
    x = x0 + tau
    dy = f_extrapolate.add_point(x, g(x))
    error = np.max(np.abs(dy))
    assert_almost_equal(error, 0)

    tau = 2
    f_extrapolate.set_stepsize(tau)

    for y in [2, 3.8, 2.9, 4]:
        assert_almost_equal(f_extrapolate(y), -2)

    # update at x = 4, extrapolation between [x, x+tau] = [4, 6.5]
    x += tau
    dy = f_extrapolate.add_point(x, g(x))
    error = np.max(np.abs(dy))
    assert_almost_equal(error, 7)

    tau = 2.5
    f_extrapolate.set_stepsize(tau)
    for y in [4, 5.2, 4.2, 6, 6.5]:
        assert_almost_equal(f_extrapolate(y), 5)

    # -- extrapolation of a linear function

    def h(x):
        return 2 - 3 * x

    # -- zero initial slope (default value)
    x0 = 1
    tau = 1

    # initial construction at x = 1, extrapolation between [x, x+tau] = [1, 2]
    f_extrapolate = interaction.Extrapolate(h(x0), tau, order=1, x0=x0)

    # first extrapolation is constant, as first derivative is set to zero
    for x in [1, 1.5, 2]:
        assert_almost_equal(f_extrapolate(x), h(1))

    # update at x = 2, extrapolation between [x, x+tau] = [2, 5]
    x = x0 + tau
    dy = f_extrapolate.add_point(x, h(x))
    error = np.max(np.abs(dy))
    assert_almost_equal(error, 3)  # h(1) - h(2), error due to constant approx.

    tau = 3
    f_extrapolate.set_stepsize(tau)

    # second extrapolation is linear, but only endpoint matches, as we start from a wrong point
    assert_almost_equal(f_extrapolate(5), h(5))

    # update at x = 5, extrapolation between [x, x+tau] = [5, 7], now we have the correct slope
    x += tau
    dy = f_extrapolate.add_point(x, h(x))
    error = np.max(np.abs(dy))
    assert_almost_equal(error, 0)
    tau = 2
    f_extrapolate.set_stepsize(tau)

    for x in [5, 6.2, 5.7, 7]:
        assert_almost_equal(f_extrapolate(x), h(x))

    # -- provide correct initial slope
    x0 = 1
    tau = 1

    # extrapolate with the correct initial slope
    # initial construction at x = 1, extrapolation between [x, x+tau] = [1, 2]
    f_extrapolate = interaction.Extrapolate(h(x0), tau, order=1, x0=x0, dy0=-3)

    for x in [1, 1.5, 2]:
        assert_almost_equal(f_extrapolate(x), h(x))

    # update at x = 2, extrapolation between [x, x+tau] = [2, 5]
    x = x0 + tau
    dy = f_extrapolate.add_point(x, h(x))
    error = np.max(np.abs(dy))
    assert_almost_equal(error, 0)

    tau = 3
    f_extrapolate.set_stepsize(tau)
    for x in [2, 4.5, 3.2, 5]:
        assert_almost_equal(f_extrapolate(x), h(x))

    update_pts = np.asarray([-1, -0.7, -0.4, -0.2, 0, 0.25, 0.5, 0.75, 1])
    taus = {update_pts[i]: update_pts[i + 1] - update_pts[i] for i in range(len(update_pts) - 1)}
    taus[update_pts[-1]] = 1.  # some placeholder value

    # -- extrapolation of a nonlinear function

    def f(x):
        x3 = 0.2
        x2 = 0.5
        a = 0.5
        return (x - x3)**3 + a * (x - x2)**2

    tau = 0.01
    x0 = update_pts[0] - tau

    func_extr = interaction.Extrapolate(f(x0), tau, order=1, x0=x0)

    for i, x in enumerate(update_pts):
        y = func_extr(x)
        if i > 1:  # check that the point coincides with the discontineous linear extrapolation
            x0 = update_pts[i - 1]
            x1 = update_pts[i - 2]
            yl = f(x0) + (f(x0) - f(x1)) / (x0 - x1) * (x - x0)
            assert_almost_equal(y, yl)
        func_extr.add_point(x, f(x))
        func_extr.set_stepsize(taus[x])
        # check that after the update, there is no step
        assert_almost_equal(func_extr(x), y)


def test_extrapolation_raises():

    def f(x):
        return 1

    x0 = 0
    tau = 1

    # nonexisting order
    func_extr = interaction.Extrapolate(f(x0), tau, order=3, x0=x0)
    with pytest.raises(NotImplementedError) as exc:
        func_extr(0.5)
    assert 'extrapolation order=3 is not implemented' in str(exc.value)

    # zero tau
    with pytest.raises(ValueError) as exc:
        interaction.Extrapolate(f(x0), tau=0)
    assert 'update timestep must be real and larger zero, found tau=0' in str(exc.value)

    # zero tau
    func_extr = interaction.Extrapolate(f(x0), tau, x0=x0)
    func_extr.add_point(tau, f(tau))
    with pytest.raises(ValueError) as exc:
        func_extr.set_stepsize(tau=0)
    assert 'update timestep must be real and larger zero, found tau=0' in str(exc.value)

    # update not at the correct x value
    func_extr = interaction.Extrapolate(f(x0), tau, x0=x0)
    with pytest.raises(ValueError) as exc:
        func_extr.add_point(0.5, f(0.5))
    assert 'update time must be at x=1, found x=0.5' in str(exc.value)

    # extrapolation beyond the range
    func_extr = interaction.Extrapolate(f(x0), tau, x0=x0)
    with pytest.raises(ValueError) as exc:
        func_extr(-0.5)
    with pytest.raises(ValueError) as exc:
        func_extr(1.5)


def test_estimate_extrapolation_step():


    def f(x):
        x3 = 0.2
        x2 = 0.5
        a = 0.5
        return (x - x3)**3 + a * (x - x2)**2

    x = np.linspace(0, 100)
    y = [f(xi) for xi in x]
    yt = [yi + np.random.rand() for yi in y]  # mimic some approximation

    stepsize = interaction.AdaptiveStepsize(1, 1e-5)

    for tau in [1e-5, 10]:  # test also wrong, negative input values
        dt = stepsize(y, yt, tau)
        assert isinstance(dt, float)
        assert dt > 0


@pytest.mark.integtest
def test_self_consistent_state():

    class HartreePotential:
        def __init__(self, interaction_strength, density0):
            self._interaction_strength = interaction_strength
            self._density0 = density0

        def prepare(self, density_func, tmax):
            """Pre-calculate the interaction contribution Q(t)"""
            self._density = density_func

        def evaluate(self, time):
            """Return the interaction contribution Q(t) evaluated at time *t*

            Here Q(t) is a diagonal matrix consisting of the onsite elements only.
            """
            diag = (self._density(time) - self._density0) * self._interaction_strength
            return scipy.sparse.diags([diag], [0], dtype=complex)


    times = [0, 40, 80, 100]

    syst, lat = create_system()
    leads.add_voltage(syst, 0, gaussian)
    syst = syst.finalized()

    density_operator_sum = kwant.operator.Density(syst, sum=True)

    occupation = manybody.lead_occupation(chemical_potential=3)
    spectra = kwantspectrum.spectra(syst.leads)
    boundaries = leads.automatic_boundary(spectra, tmax=max(times))
    Interval = functools.partial(manybody.Interval, order=4,
                                 quadrature='gausslegendre')
    intervals = manybody.calc_intervals(spectra, occupation, interval_type=Interval)

    tasks = manybody.calc_tasks(intervals, spectra, occupation)
    psi_init = manybody.calc_initial_state(syst, tasks, boundaries)
    wave_function = manybody.WaveFunction(psi_init, tasks)

    # class to calculate the interaction contribution to the hamiltonian
    density_operator = kwant.operator.Density(syst)
    density0 = wave_function.evaluate(density_operator, root=None)  # no MPI root, density0 is available on all ranks

    hartree_potential = HartreePotential(interaction_strength=2, density0=density0)

    wave_function_mf = interaction.SelfConsistentState(wave_function,
                                                       density_operator,
                                                       hartree_potential)
    assert isinstance(wave_function_mf.steps, int)
    assert wave_function_mf.steps == 0

    densities_u1 = []
    for time in times:
        wave_function_mf.evolve(time)
        density = wave_function_mf.evaluate(density_operator_sum)
        densities_u1.append(density)

    # -- simple regression test against tabulated result
    densities_ref = [6.9999999, 7.00909565, 6.994956018, 7.059345737]
    for dens_u1, dens_ref in zip(densities_u1, densities_ref):
        assert_almost_equal(dens_u1, dens_ref, decimal=4)

@pytest.mark.integtest
def test_self_consistent_onebody():

    # try simply if it runs also for the onebody wavefunction

    # lattice sites and time steps
    xi = np.arange(400)
    #times = np.arange(0, 1201, 50)
    times = [0, 10]

    # initial condition
    k = np.pi / 6
    psi0 = np.exp(- 0.001 * (xi - 100)**2 + 1j * k * xi)

    # hamiltonian matrix
    diag = 2 * np.ones(len(xi))
    offdiag = - np.ones(len(xi) - 1)
    H0 = scipy.sparse.diags([diag, offdiag, offdiag], [0, 1, -1], dtype=complex)

    # initialize the solver
    wave_function = onebody.WaveFunction(H0, W=None, psi_init=psi0)

    def density_operator(psi, params):
        return np.real(psi * psi.conjugate())

    class InteractPotential:
        def __init__(self, density0):
            self._density0 = density0

        def prepare(self, density_func, tmax):
            """Pre-calculate the interaction contribution Q(t)"""
            self._density = density_func

        def evaluate(self, time):
            """Return the interaction contribution Q(t) = (|psi(t)|^2 -|psi(0)|^2)"""
            diag = (self._density(time) - self._density0)
            return scipy.sparse.diags([diag], [0], dtype=complex)

    density0 = wave_function.evaluate(density_operator)

    interact_potential = InteractPotential(density0)

    # set up the self-consistent interacting wave function
    wave_function_mf = interaction.SelfConsistentState(wave_function,
                                                       density_operator,
                                                       interact_potential)

    for time in times:
        wave_function_mf.evolve(time)
        density = wave_function_mf.evaluate(density_operator)
