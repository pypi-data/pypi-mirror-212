.. _green_functions:

Green functions
===============

.. jupyter-execute::
    :hide-code:

    # suppress jupyter warnings messages when calling kwant.plot()
    import matplotlib.pyplot, matplotlib.backends


Introduction
------------

We consider a general quadratic Hamiltonian describing a noninteracting
open tight-binding system

.. math::
   :label: h0

   \begin{equation}
       \hat{H} = \sum_{i,j} H_{ij}(t) c^\dagger_i c_j .
   \end{equation}

The :math:`c^\dagger_i,\, (c_i)` are the usual Fermionic creation and
annihilation operators of a one electron state at site :math:`i`, where
the site index comprises all degreens of freedom of the system, such as
lattice site, spin, orbital index etc. Moreover, an element of the
Hamiltion matrix :math:`H_{ij}(t)` can have an arbitrary time
dependence. We are interested in the nonequilibrium Green function


.. math::
   :label: ggen

   \begin{align}
       G_{ij}^<(t, t') &= i \langle c^\dagger_j(t')  c_i(t)  \rangle , \\
       G_{ij}^R(t, t') &= - i \theta(t - t') \langle \{ c_i(t) , c^\dagger_j(t') \} \rangle , 
   \end{align}



where :math:`c^\dagger_i(t)` and respectively :math:`c_i(t)` correspond
to the fermionic operators in the Heisenberg representation, the curly
brackets :math:`\{ \ldots \}` stand for the anticommutator and the
manybody average
:math:`\langle \ldots \rangle \equiv \textrm{Tr}(\hat{\rho} \ldots)`
where :math:`\hat{\rho}` is the non-equilibrium density matrix at
initial time. Note that above lesser and retarded Green functions are
sufficient to obtain all other kind of Green functions `[1] <#references>`__ also in a
general nonequilibrium situation, where no fluctucation-dissipation
relation holds.

A numerically exact method to calculate :math:`G^<` and :math:`G^R` for
quadratic Hamiltonians as Eq. (1) has been developed in `[2] <#references>`__
to express them in terms of the wave function $\psi$ as

.. math::
   :label: ggen2

   \begin{align}
        G_{ij}^<(t, t') &=  \sum_\alpha \int \frac{dE}{2 \pi} i f_\alpha(E) \psi_{\alpha E}(t, i) \psi^*_{\alpha E}(t', j) , \\
        G_{ij}^R(t, t') &= - i \theta(t - t') \sum_\alpha \int \frac{dE}{2 \pi} \psi_{\alpha E}(t, i) \psi^*_{\alpha E}(t', j) ,
   \end{align}

where :math:`f_\alpha` is the Fermi function in lead :math:`\alpha`. This method has now
been implemented in the Tkwant package `[3] <#references>`__. After a short introduction
to the corresponding Tkwant class we will show in this tutorial how
different Green functions are calculated in practice using Tkwant. As a
toy example we will use two impurity models on a one dimensional chain:
(I) a double quantum dot in a stationary out-of-equilibrium
regime and (II) a single impurity in the transient regime after a quench. Closed analytical expressions can be derived at weak coupling
between the impurites and the semi-infinite leads in the so-called
flatband approximation `[4] <#references>`__, which serve as a benchmark for the numerical
Tkwant results. The detailled calculation of the analytical flat-band
results are provided in the `Appendix`_.

The class :math:`\texttt{tkwant.manybody.Greenfunction}`
--------------------------------------------------------

.. jupyter-execute::
    :hide-code:

    # make first examples into real running code
    import tkwant
    import kwant


    def make_system():
        lat = kwant.lattice.chain(a=1, norbs=1)
        syst = kwant.Builder()
        syst[(lat(x) for x in range(10))] = 0
        syst[lat.neighbors()] = -1
        sym = kwant.TranslationalSymmetry((-1,))
        lead_left = kwant.Builder(sym)
        lead_left[lat(0)] = 0
        lead_left[lat.neighbors()] = -1
        syst.attach_lead(lead_left)
        syst.attach_lead(lead_left.reversed())
        return syst
    syst = make_system().finalized()
    tmax = 10
    occupations = tkwant.manybody.lead_occupation()


Tkwant provides the class :math:`\texttt{tkwant.manybody.Greenfunction}`
to compute nonequilibrium Greenfunctions between two sites of the
central scattering system. The Green functions are real two-time objects
which are also valid in the transient nonequilibrium regime. The class
:math:`\texttt{tkwant.manybody.Greenfunction}` is simple to use and
behaves similar to the manybody wavefunction class
:math:`\texttt{tkwant.manybody.State}`. The
:math:`\texttt{tkwant.manybody.Greenfunction}` class is instatiated as

.. jupyter-execute::

    green = tkwant.manybody.GreenFunction(syst, tmax, occupations)

where :math:`\texttt{syst}` is a finalized Kwant system of type
:math:`\texttt{kwant.builder.FiniteSystem}`, :math:`\texttt{tmax}` is the maximal time such that
:math:`t_0, t_1 \leq t_{max}` for :math:`G(t_0, t_1)` and occupations is
a sequence of lead occupations of type :math:`\texttt{tkwant.manybody.Occupation}`.
To calculate :math:`G^<_{i=0,j=2}(t_0, t_1)` and
:math:`G^>_{i=1, j=5}(t_0, t_1)` for instance, both for time arguments
:math:`t_0=8, t_1 =3`, one evaluates

.. jupyter-execute::

    green.evolve(time0=5, time1=3)
    green.refine_intervals()
    gless = green.lesser(i=0, j=2)
    ggreat = green.greater(i=1, j=5)

The second call to the :math:`\texttt{refine_intervals()}` method is optional, but
is important to reach a numerically precise estimate of the manybody
integral. Without further arguments, a default precision will be
targeted for the diagonal Green function elements :math:`G_{ii}` at the
given times, where :math:`i` runs over all sites of the central
scattering region. One can change this behavior and pass a sequence of
tuples :math:`(i,j)` to the :math:`\texttt{refine_intervals()}` method, which will
refine the corresponding :math:`G_{ij}` elements in the sequence. For
instance

.. jupyter-execute::

    green.refine_intervals(sites=[(0, 1), (2, 1)])

will refine the Green functions on sites :math:`G_{01}` and
:math:`G_{21}`. One can also change the relative and the absolute
precision of the result via

.. jupyter-execute::

    green.refine_intervals(rtol=1e-8, atol=1e-8)

To obtain the other Green functions (retarded, keldysh, time-ordered...)
is also possible as shown in section `Various kinds of Green functions`_. We can now directly study the
two toy problems.

Example I: A two sites impurity on an infinite one-dimensional chain (double quantum dot)
-----------------------------------------------------------------------------------------

We depict two impurities on a one-dimensional chain described by the
Hamiltonian

.. math::
   :label: h_ex1

   \begin{align}
     H = - \sum_{i = -\infty}^\infty [\gamma_i c^\dagger_{i + 1} c_i + \text{h.c.}] + \epsilon_L c^\dagger_{0} c_{0} + \epsilon_R c^\dagger_{1} c_{1}
   \end{align}

The sites :math:`i` label the discrete lattice sites and the hoppings
are :math:`\gamma_i = 1` for all :math:`i` except at the impurity, where
we introduce the more descriptive notation
:math:`\gamma_{-1} = \gamma_L`, :math:`\gamma_0 = \gamma_C` and
:math:`\gamma_1 = \gamma_R`. In both the left and the right lead far
away from the central system, the electrons are considered to be in
thermal equilibrium. For simplicity we choose the temperature to be zero
in both leads, but allow two different chemical potentials :math:`\mu_L`
and :math:`\mu_R` to realize a stationary non-equilibrium situation.

As the above problem is stationary in time, all Green functions depend
only on the time difference

.. math::
   :label: gdia

   \begin{equation}
       G(t,t') = G(t - t')
   \end{equation}

and we will plot effecitve single-time Green functions defined as

.. math::
   :label: gdia2

   \begin{equation}
       G(t) = 
       \begin{cases}
       G(t, 0) & \text{for } t \geq 0 \\
       G(0, -t) & \text{for } t < 0 \\
       \end{cases} 
   \end{equation}

A true non-stationary problem, where translational time symmetry does
not hold such that the Green functions have a true two-time dependence
are consideren for model II below. The analytical calculation of the
non-equilibrium Green functions in flatband approximation are given
below. Let us state again that the wave function method in `[2] <#references>`__ which is
implemented in Tkwant does not rely on the smallness of the coupling
constants, but we choose this regime here in order to use the flatband
limit as a benchmark.



Numerical calculation of :math:`G^<` and :math:`G^R` using Tkwant
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We will show how to do this using the Python package Tkwant. First we
include Tkwant `[3] <#references>`__ and Kwant `[5] <#references>`__ alongsinde standard Python packages.

.. jupyter-execute::

    import tkwant
    import kwant
    
    import numpy as np
    import matplotlib.pyplot as plt

.. jupyter-execute::
    :hide-code:

    import pylab
    
    # --- plot settings
    markersize = 14
    
    fac = 6
    pylab.rcParams['figure.figsize'] = (fac * np.sqrt(2), fac)
    
    plt.rcParams.update({'font.size': 20})
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

The parameters and timesteps are set to:

.. jupyter-execute::

    # couplings
    gamma_L = 0.14
    gamma_C = 0.05
    gamma_R = 0.08
    
    # onsite elements
    epsilon_L = 0.5
    epsilon_R = 0.3
    
    # chemical potentials
    mu_L = 0.5
    mu_R = - 0.8
    
    # values of time where the green’s function will be evaluated
    times = np.linspace(0, 20, 21)

Building the Kwant system
^^^^^^^^^^^^^^^^^^^^^^^^^

We build a standard one-dimensional Kwant system. The plot below
visualizes again our model defind in Eq. (4).

.. jupyter-execute::

    def make_double_impurity_system(gamma_L, gamma_C, gamma_R, eps_L, eps_R):
    
        # system building
        lat = kwant.lattice.chain(a=1, norbs=1)
        syst = kwant.Builder()
    
        # central scattering region
        syst[(lat(x) for x in [-1, 2])] = 0
        syst[lat(0)] = eps_L
        syst[lat(1)] = eps_R
    
        syst[(lat(0), lat(-1))] = -gamma_L
        syst[(lat(1), lat(0))] = -gamma_C
        syst[(lat(2), lat(1))] = -gamma_R
    
        # add leads
        sym = kwant.TranslationalSymmetry((-1,))
        lead_left = kwant.Builder(sym)
        lead_left[lat(0)] = 0
        lead_left[lat.neighbors()] = -1
        syst.attach_lead(lead_left)
        syst.attach_lead(lead_left.reversed())
    
        return syst, lat
    
    
    syst, lat = make_double_impurity_system(gamma_L, gamma_C, gamma_R, epsilon_L, epsilon_R)
    
    # plot the system with onsite and coupling paramters
    kwant.plot(syst, site_color='k', lead_color='grey', num_lead_cells=3, show=False);
    plt.text(-0.1, 0.5, r'$\epsilon_L$', fontsize=20)
    plt.text(0.9, 0.5, r'$\epsilon_R$', fontsize=20)
    
    plt.text(-0.6, -0.5, r'$\gamma_L$', fontsize=20)
    plt.text(0.4, -0.5, r'$\gamma_C$', fontsize=20)
    plt.text(1.4, -0.5, r'$\gamma_R$', fontsize=20)
    
    plt.text(-4, 0.5, r'$\mu_L$', fontsize=20)
    plt.text(4.8, 0.5, r'$\mu_R$', fontsize=20)
    
    syst = syst.finalized()




The electrons in both left and right leads have typical
:math:`E(k) = 2(1 - \cos(k))` tight binding dispersion. We plot the
dispersion together with the chemical potentials :math:`\mu_{L/R}`:

.. jupyter-execute::

    kwant.plotter.bands(syst.leads[0], show=False)
    plt.plot([-np.pi, np.pi], [mu_L] * 2, '--', color='#e15759', label=r"$\mu_L$")
    plt.plot([-np.pi, np.pi], [mu_R] * 2, '--', color='#f28e2b', label=r"$\mu_R$")
    plt.legend()
    plt.show()




The leads can be defined using the :math:`\texttt{tkwant.manybody.lead_occupation}`
function in complete analogy to the standard Tkwant manybody
wavefunction calculation. Here we set the left and right lead to have
the chemical potentials :math:`\mu_L` and :math:`\mu_R`:

.. jupyter-execute::

    occupations = [tkwant.manybody.lead_occupation(chemical_potential=mu_L),
                   tkwant.manybody.lead_occupation(chemical_potential=mu_R)]

Without further specification, zero temperature is assumed in above
case.

Time evolution and evaluation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Tkwant class to calculate 2-time Green functions of different kind
between two sites :math:`i` and :math:`j` is called
:math:`\texttt{tkwant.manybody.GreenFunction}`. It is instatiated as:

.. jupyter-execute::

    green = tkwant.manybody.GreenFunction(syst, max(times), occupations)

The class :math:`\texttt{GreenFunction}` uses the indexing of Kwant for
the different lattice sites. While a lattice site is attributed by the
user during the definition of the Hamiltonian, its index (which is an
integer number) is an *a priori* arbitrary internal numbering from
Kwant.

To show the difference between the site and its corresponding index,
consider the definition of the Hamiltonian in this example. There, the
left impurity has been attributed to the lattice site 0 (see line
:math:`\texttt{syst[lat(0)] = eps_L}` in function
:math:`\texttt{make_double_impurity_system()}`), but the actual index
for this site is 1. While the indexing is still comprehensible in this
simple example (the index increases from left to right, starting at the
leftmost site with index 0), the situation gets more involved for
extended and multiorbital systems.

Tkwant therefore provides the class :math:`\texttt{siteId}` to easily
obtain the correct index. An instance of :math:`\texttt{siteId}` can be
called with a lattice site to get the index in the Kwant ordering. Below
we show how the index of the site with the left impurity can be obtained
with the help of :math:`\texttt{siteId}`:

.. jupyter-execute::

    idx = tkwant.system.siteId(syst, lat)
    site_0 = idx(0)
    print('the left impurity has index= {} in the Kwant system'.format(site_0))


The Green function can now be evolved forward in time with the
:math:`\texttt{evolve()}` method. Note that the
:math:`\texttt{GreenFunction.evolve()}` method takes 2 time arguments,
in contrast to the similar method in the wave function objects that take
only a single time argument. The
:math:`\texttt{tkwant.manybody.GreenFunction}` class provides also a
:math:`\texttt{refine_intervals()}` method, which should be called to ensure that
the result is numerically correct. There is no evaluate method as for
the wave function, but a method for each Green function type, which has
to be called with two indices (obtained from :math:`\texttt{siteId}`),
referring to the corresponding lattice sites. Here we call the
:math:`\texttt{lesser()}` and the :math:`\texttt{retarded()}` methods
with :math:`i = j` both on the lattice site 0 (left impurity position)
to evaluate :math:`G_{00}^<` and :math:`G_{00}^R`:

.. jupyter-execute::

    green_lesser = []
    green_retard = []
    
    for time in times:
    
        green.evolve(time, 0)
        green.refine_intervals()
    
        green_lesser.append(green.lesser(site_0, site_0))
        green_retard.append(green.retarded(site_0, site_0))

In the next step we calculate the referenc data.

Comparison to the analytical solution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Green functions for the quantum dot array in flatband approximations
are given in Eqs. (25), (28) and (32) and are implemented as special
purpose routine in :math:`\texttt{tkwant.special.GreenFlatBand}`. For
convenience, we have written the routine
:math:`\texttt{make_double_impurity_matrices}` to prepare the relevant
input for our double dot system:

.. jupyter-execute::

    def make_double_impurity_matrices(gamma_L, gamma_C, gamma_R, epsilon_L, epsilon_R, mu_L, mu_R):
        h_ss = np.array([[epsilon_L, -gamma_C], [-gamma_C, epsilon_R]])
        h_se = np.array([[- gamma_L, 0], [0, - gamma_R]])
        gr_e = np.array([tkwant.special.g_ee_retarded(mu_L), tkwant.special.g_ee_retarded(mu_R)])
        mu_e = [mu_L, mu_R]
        return h_ss, h_se, gr_e, mu_e

From this, we can directly calculate :math:`G_{00}^<` and
:math:`G_{00}^R` in flatband approximation:

.. jupyter-execute::

    matr = make_double_impurity_matrices(gamma_L, gamma_C, gamma_R, epsilon_L, epsilon_R, mu_L, mu_R)
    
    green_flatband = tkwant.special.GreenFlatBand(*matr)
    
    times_fine = np.linspace(0, 20, 201)
    green_lesser_ref = np.array([green_flatband.lesser(0, 0, t) for t in times_fine])
    green_retard_ref = np.array([green_flatband.retarded(0, 0, t) for t in times_fine])

We finally plot the Tkwant and the flatband results to see that they
agree nicely:

.. jupyter-execute::

    green_lesser = np.array(green_lesser)
    green_retard = np.array(green_retard)
    
    fig, axes = plt.subplots(2, 2)
    fig.set_size_inches(16, 10)
    
    axes[0][0].plot(times_fine, green_lesser_ref.real, label='flatband')
    axes[0][0].plot(times, green_lesser.real, 'o', label='Tkwant')
    axes[0][0].set_title(r'$\Re G_{00}^<(t)$')
    
    axes[0][1].plot(times_fine, green_lesser_ref.imag, label='flatband')
    axes[0][1].plot(times, green_lesser.imag, 'o', label='Tkwant')
    axes[0][1].set_title(r'$\Im G_{00}^<(t)$')
    
    axes[1][0].plot(times_fine, green_retard_ref.real, label='flatband')
    axes[1][0].plot(times, green_retard.real, 'o', label='Tkwant')
    axes[1][0].set_title(r'$\Re G_{00}^R(t)$')
    
    axes[1][1].plot(times_fine, green_retard_ref.imag, label='flatband')
    axes[1][1].plot(times, green_retard.imag, 'o', label='Tkwant')
    axes[1][1].set_title(r'$\Im G_{00}^R(t)$')
    
    
    for axs in axes:
        for ax in axs:
            ax.set_xlabel(r'time $t$')
            ax.set_xlim(0, max(times))
            
    plt.suptitle('$\gamma_L={}, \gamma_C={}, \gamma_R={}, \epsilon_L={}, \epsilon_R={}, \mu_L={}, \mu_R={}$'.
                 format(gamma_L, gamma_C, gamma_R, epsilon_L, epsilon_R, mu_L, mu_R), size=22)
    
    plt.subplots_adjust(wspace=0.3, hspace=0.4)
    plt.legend(bbox_to_anchor=(1.1, 2.9))
    plt.show()




Calculating equal time diagonal and off-diagonal Green functions related to density and current
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We write the discrete continuity equation in the form

.. math::
   :label: continuity

   \begin{equation}
     \partial_t n_{i}(t) = \sum_{j} I_{ij}(t) ,
   \end{equation}

where :math:`n_{i} = \langle c^\dagger_i(t) c_i(t) \rangle` is the
density on site :math:`i` and :math:`I_{ij} = - I_{ji}` the current
flowing from site :math:`j` to site :math:`i`. For a quadratic
Hamiltonian as Eq. (1), we can derive the current (in units of
:math:`\hbar`) as

.. math::
   :label: current

   \begin{equation}
     I_{ij}(t) = i \left[ \langle c^\dagger_j(t) H_{ji}(t) c_i(t) \rangle - \langle c^\dagger_i(t) H_{ij}(t) c_j(t) \rangle \right] . 
   \end{equation}

To calculate the onsite density and the current, they can be expressed
in terms of the equal time :math:`G^<` function Eq. (2):

.. math::
   :label: nigreen

   \begin{align}
     n_i(t) &=  - i G^<_{ii}(t,t) , \\ 
     I_{ij}(t) &= 2 \Re \left[ G^<_{ij}(t,t) H_{ji}(t) \right]  .
   \end{align}

Alternatively, both observables can be calculated using the wave
function approach `[2, 3] <#references>`__ with

.. math::
   :label: niwf

   \begin{align}
     n_i(t) &=  \int \frac{d E}{2 \pi} \sum_{\alpha} f_\alpha(E) | \psi_{\alpha E}(t, i)|^2 , \\ 
     I_{ij}(t) &= -  2  i \Im \int \frac{d E}{2 \pi} \sum_{\alpha} f_\alpha(E) \psi_{\alpha E}^*(t, i)  H_{ij}(t)   \psi_{\alpha E}(t, j) . 
   \end{align}

In the following we compute the density on the left (site 0) impurity
:math:`n_0(t) = - i G^<_{00}(t,t)` and the current :math:`I_{10}(t)`
from the left to the right impurity (site 0 to site 1) with the Green
and the wave function approach. Our Hamiltonian matrix is static and
with :math:`H_{10}(t) = - \gamma_C` one finds
:math:`I_{10}(t) = - 2 \gamma_C \Re G^<_{10}(t,t)`. First we compute the
equal time Green functions to check that they are indeed constant in
time:

.. jupyter-execute::

    green = tkwant.manybody.GreenFunction(syst, tmax=max(times), occupations=occupations)
    
    g_less_00 = []
    g_less_10 = []
    
    idx = tkwant.system.siteId(syst, lat)
    site_0 = idx(0)
    site_1 = idx(1)
    
    for time in times:
    
        green.evolve(time, time)
        green.refine_intervals()
    
        g_less_00.append(green.lesser(site_0, site_0))
        g_less_10.append(green.lesser(site_1, site_0))
    
    g_less_00 = np.array(g_less_00)
    g_less_10 = np.array(g_less_10)
    
    plt.plot(times, g_less_00.real, 'o-', color='#e15759', label='$\Re G^<_{00}$')
    plt.plot(times, g_less_00.imag, 'o-',color='#f28e2b', label='$\Im G^<_{00}$')
    
    plt.plot(times, g_less_10.real, 'o-', color='#4e79a7', label='$\Re G^<_{10}$')
    plt.plot(times, g_less_10.imag, 'o-', color='#76b7b2', label='$\Im G^<_{10}$')
    
    plt.xlabel(r'time $t$')
    plt.ylabel(r'$G^<_{ij}(t, t)$')
    plt.xlim(0, max(times))
    plt.legend()
    plt.show()




The stationary density and current can be obtained at initial time.
Plotting the stationary density and current as function of Hamiltonian
parameter :math:`\epsilon_L` one can check that the Green and the wave
function approach agree and the result also fits with the analytical
flat band estimate.

.. jupyter-execute::

    n0_wave = []
    n0_green = []
    n0_flat = []
    
    i10_wave = []
    i10_green = []
    i10_flat = []
    
    epsilons = np.linspace(-1, 1, 21)
    
    for epsilon_L_ in epsilons:
    
        syst, lat = make_double_impurity_system(gamma_L, gamma_C, gamma_R, epsilon_L_, epsilon_R)
        syst = syst.finalized()
        
        occupations = [tkwant.manybody.lead_occupation(chemical_potential=mu_L),
                       tkwant.manybody.lead_occupation(chemical_potential=mu_R)]
    
        # -- via wavefunction and density operator
    
        density_operator = kwant.operator.Density(syst, where=[lat(0)])
        current_operator = kwant.operator.Current(syst, where=[(lat(1), lat(0))])
        
        state = tkwant.manybody.State(syst, tmax=1, occupations=occupations)
        density = state.evaluate(density_operator)
        current = state.evaluate(current_operator)
        n0_wave.append(density)
        i10_wave.append(current)
        
        # -- via greenfunction from tkwant
    
        idx = tkwant.system.siteId(syst, lat)
        site_0 = idx(0)
        site_1 = idx(1)
    
        green = tkwant.manybody.GreenFunction(syst, tmax=1, occupations=occupations)
        g_less_00 = green.lesser(site_0, site_0)
        g_less_10 = green.lesser(site_1, site_0)
    
        density = g_less_00.imag
        current = - 2 * gamma_C * g_less_10.real
        n0_green.append(density)
        i10_green.append(current)
    
    epsilons_fine = np.linspace(-1, 1, 201)
    
    for epsilon_L_ in epsilons_fine:
    
         # -- via greenfunction in flatband approximation
        
        matr = make_double_impurity_matrices(gamma_L, gamma_C, gamma_R, epsilon_L_, epsilon_R, mu_L, mu_R)
    
        green_flatband = tkwant.special.GreenFlatBand(*matr)
        g_less_00 = green_flatband.lesser(0, 0, 0.)
        g_less_10 = green_flatband.lesser(1, 0, 0.)
        
        density = g_less_00.imag
        current = - 2 * gamma_C * g_less_10.real
        n0_flat.append(density)
        i10_flat.append(current)
    
    #--- plot the results
    
    fig, axes = plt.subplots(1, 2)
    fig.set_size_inches(16, 5)
    
    axes[0].plot(epsilons, n0_wave, 'o', color='#e15759', label='via $\Psi$ from Tkwant')
    axes[0].plot(epsilons, n0_green, 'x', color='#f28e2b', markersize=12, label='via $G^<_{00}$ from Tkwant')
    axes[0].plot(epsilons_fine, n0_flat, color='#4e79a7', label='via $G^<_{00}$ flatband')
    axes[0].set_ylabel(r'$n_0$')
    
    axes[1].plot(epsilons, i10_wave, 'o', color='#e15759', label='via $\Psi$ from Tkwant')
    axes[1].plot(epsilons, i10_green, 'x', color='#f28e2b', markersize=12, label='via $G^<_{10}$ from Tkwant')
    axes[1].plot(epsilons_fine, i10_flat, color='#4e79a7', label='via $G^<_{10}$ flatband')
    axes[1].set_ylabel(r'$I_{10}$')
    
    for ax in axes:
        ax.legend(fontsize=14)
        ax.set_xlabel(r'$\epsilon_L$')
        ax.set_xlim(min(epsilons), max(epsilons))
        
    plt.suptitle('$\gamma_L={}, \gamma_C={}, \gamma_R={}, \epsilon_R={}, \mu_L={}, \mu_R={}$'.
                 format(gamma_L, gamma_C, gamma_R, epsilon_R, mu_L, mu_R), size=22)
    
    plt.show()



Various kinds of Green functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Several kinds of nonequilibrium Greenfunctions can be defined. In the
so-called contour base, one usually works with the lesser :math:`G^<`,
greater :math:`G^>`, time-ordered :math:`G^T` and anti-time ordered,
:math:`G^{\bar{T}}` whereas in the RAK basis, one usually works with the
retarded :math:`G^{R}`, advanced :math:`G^{A}` and the Keldysh
:math:`G^{K}` Green functions, see e.g. Ref. `[1] <#references>`__. For Fermions, these
Green functions are defined as

.. math::
   :label: greentypes

   \begin{align}
       G^<_{ij}(t,t') &= i \langle c^\dagger_{j}(t') c_i(t)\rangle ,  \\
       G^>_{ij}(t,t') &= -i \langle c_{i}(t) c^\dagger_{j}(t')\rangle , \\
       G^T_{ij}(t,t') &= -i  \langle T(c_i ( t ) c^\dagger_{j} ( t^{\prime} )) \rangle , \\
       G^{\bar{T}}_{ij}(t,t') &= -i  \langle \bar{T}(c_i ( t ) c^\dagger_{j} ( t^{\prime} )) \rangle ,  \\
       G^{R}_{ij}(t,t') &= -i \theta(t - t')  \langle \{ c_i ( t ) , c^\dagger_{j} ( t^{\prime} ) \} \rangle ,   \\
       G^{A}_{ij}(t,t') &= i \theta(t' - t)  \langle \{ c_i ( t ) , c^\dagger_{j} ( t^{\prime} ) \} \rangle ,  \\
       G^{K}_{ij}(t,t') &= - i   \langle \{ c_i ( t ) , c^\dagger_{j} ( t^{\prime} ) \} \rangle  .
   \end{align}

In above equations, :math:`T` stands for the time-ordering and
:math:`\bar{T}` for the anti-time ordering operator. The class
:math:`\texttt{tkwant.manybody.GreenFunction}` has implemented all above
Green functions. In the following we compute the different kind of Green
functions for the diagonal :math:`G_{00}` and the off-diagonal
:math:`G_{01}` elements.

.. jupyter-execute::

    green_types = {}
    green_types['lesser'] = 'G^<'
    green_types['greater'] = 'G^>'
    green_types['ordered'] = 'G^T'
    green_types['anti_ordered'] = 'G^{\overline{T}}'
    green_types['retarded'] = 'G^R'
    green_types['advanced'] = 'G^A'
    green_types['keldysh'] = 'G^K'
    
    green_data_00 = {key: [] for key in green_types.keys()}
    green_data_01 = {key: [] for key in green_types.keys()}
    
    syst, lat = make_double_impurity_system(gamma_L, gamma_C, gamma_R, epsilon_L, epsilon_R)
    syst = syst.finalized()
    
    # -- negative times
    green = tkwant.manybody.GreenFunction(syst, max(times), occupations)
    
    for time in times[1:]:
        green.evolve(0, time)
        green.refine_intervals()
    
        for gtype in green_types.keys():
            green_data_00[gtype].insert(0, getattr(green, gtype)(site_0, site_0))
            green_data_01[gtype].insert(0, getattr(green, gtype)(site_0, site_1))
    
    # -- positive times
    green = tkwant.manybody.GreenFunction(syst, max(times), occupations)
    
    for time in times:
        green.evolve(time, 0)
        green.refine_intervals()
    
        for gtype in green_types.keys():
            green_data_00[gtype].append(getattr(green, gtype)(site_0, site_0))
            green_data_01[gtype].append(getattr(green, gtype)(site_0, site_1))
    
    times_pm = np.concatenate((-times[:0:-1], times))
    green_data_00 = {key: np.array(val) for key, val in green_data_00.items()}
    green_data_01 = {key: np.array(val) for key, val in green_data_01.items()}

Note that we have splitted the above evolution in two parts to account
for the positive and the negative time arguments as in Eqs. (5) and (6).
The different kind of Green functions are computed also in flatband
approximation:

.. jupyter-execute::

    matr = make_double_impurity_matrices(gamma_L, gamma_C, gamma_R, epsilon_L, epsilon_R, mu_L, mu_R)
    
    green_flatband = tkwant.special.GreenFlatBand(*matr)
    
    green_data_00_ref = {key: np.array([getattr(green_flatband, key)(0, 0, t) for t in times_pm])
                         for key in green_types.keys()}
    green_data_01_ref = {key: np.array([getattr(green_flatband, key)(0, 1, t) for t in times_pm])
                         for key in green_types.keys()}

We find perfect agreement the numerical Tkwant result and the analytical
flatband reference:

.. jupyter-execute::

    fig, axes = plt.subplots(len(green_types), 4)
    fig.set_size_inches(18, 15)
    
    for i, (key, gtype) in enumerate(green_types.items()):
    
        axes[i][0].plot(times_pm, green_data_00_ref[key].real, label='flatband')
        axes[i][0].plot(times_pm, green_data_00[key].real, linestyle='dotted', lw=4, label='Tkwant')
        axes[i][0].set_title('$\Re ' + gtype + '_{00}(t)$')
        
        axes[i][1].plot(times_pm, green_data_00_ref[key].imag, label='flatband')
        axes[i][1].plot(times_pm, green_data_00[key].imag, linestyle='dotted', lw=4, label='Tkwant')
        axes[i][1].set_title('$\Im ' + gtype + '_{00}(t)$')
    
        axes[i][2].plot(times_pm, green_data_01_ref[key].real, label='flatband')
        axes[i][2].plot(times_pm, green_data_01[key].real, linestyle='dotted', lw=4, label='Tkwant')
        axes[i][2].set_title('$\Re ' + gtype + '_{01}(t)$')
        
        axes[i][3].plot(times_pm, green_data_01_ref[key].imag, label='flatband')
        axes[i][3].plot(times_pm, green_data_01[key].imag, linestyle='dotted', lw=4, label='Tkwant')
        axes[i][3].set_title('$\Im ' + gtype + '_{01}(t)$')
    
    for axx in axes:
        for ax in axx:
            ax.set_xlim(-max(times), max(times))
    
    plt.suptitle('$\gamma_L={}, \gamma_C={}, \gamma_R={}, \epsilon_L={}, \epsilon_R={}, \mu_L={}, \mu_R={}$'.
                 format(gamma_L, gamma_C, gamma_R, epsilon_L, epsilon_R, mu_L, mu_R), size=22)
    
    plt.subplots_adjust(wspace=0.4, hspace=0.8)
    plt.legend(bbox_to_anchor=(1.1, 13.8))
    
    plt.show()




Example II: Single impurity site: quench of the coupling to the leads
---------------------------------------------------------------------

Transient dynamics
~~~~~~~~~~~~~~~~~~

To evaluate Greenfunctions also in the transient regime, we consider a
single impurity model where the initially empty dot is connected at
initial time :math:`t=0` abruptly to the leads. The Hamiltonian is

.. math::
   :label: h_ex2

   \begin{align}
     H = - \sum_{i = -\infty}^\infty [\gamma_i(t) c^\dagger_{i + 1} c_i + \text{h.c.}]  + \epsilon_0 c^\dagger_{0} c_{0}
   \end{align}

with index :math:`0` at the central impurity site. The hoppings
:math:`\gamma_i(t) = 1` for all :math:`i`, except at the impurity where
:math:`\gamma_{-1}(t) = \gamma_{0}(t) = \gamma\theta(t)`, where
:math:`\theta(x)` is the Heaviside stepfunction. We choose the
convention :math:`\theta(0) = 0`, such that the dot is initially
disconnected and empty. Moreover we consider the symmetric equilibrium
case with :math:`\mu_L = \mu_R = 0` and zero temperature in the leads,
and focus on the regime of weak coupling :math:`\gamma \ll 1` such that
we can compare to flatband approximation. The detailed calculation of
the flatband Green function in this regime is given in the `Appendix`_.
Introducing :math:`\Gamma = 2 \gamma^2`, the lesser Green
function on the dot can be written as

.. math::
   :label: gtt1

   \begin{align}
     G_{00}^<(t, t') =    \theta(t) \theta(t') \frac{i \Gamma}{\pi} e^{-i \epsilon_0 (t - t')} \int_{-\infty}^0 d \omega  \frac{1}{(\omega - \epsilon_0)^2 + \Gamma^2} \left( e^{-i (\omega - \epsilon_0) t} - e^{- \Gamma t}\right)
   \left( e^{i (\omega - \epsilon_0) t'} - e^{- \Gamma t'}\right)  
   \end{align}

Note that an almost identical expression has been derived in Ref. `[6] <#references>`__,
except a typo as the oscillating factor
:math:`e^{-i \epsilon_0 (t - t')}` is missing in Eq. (15) of that
reference. The occupation on the dot :math:`n(t)` can be obtained again
from the equal time :math:`G^<` function via
:math:`n(t) = - i G_{00}^<(t, t)`. The long-time limit corresponds to
the stationary equilibrium density :math:`n_{eq}` on the dot and one
obtains the well-known relation

.. math::
   :label: neq

   \begin{align}
     n_{eq} =   \lim_{t \rightarrow \infty} n(t), \qquad n_{eq} =   \frac{1}{\pi} \arctan \left(-\frac{ \epsilon_0}{\Gamma} \right) + \frac{1}{2}
   \end{align}

The Tkwant simulation for the Green function can be performed very
similar to all examples above, except that the coupling between the lead
and the dot are now time dependent. Due to the abrupte switching of the
leads, the integrand over the different energy modes is getting
numerically complicated and cause the adaptive integration routine to
use many integral subdivisions. The simulation is therefore too time
consuming for running this tutorial in real time. We will show therefore
only the result, but provide the Python scripts to perform the
simulation below.

.. figure:: fig_siam_sudden_switch.png
   :alt: siam_sudden_switch
   :width: 900px

Above simulations shows the lesser Green function with different (left)
and identical (right) time arguments. The density :math:`n(t)` on the
dot is calculated with Tkwant using the manybody wave function approach.
The value :math:`n_{eq}` is computed from Tkwant using the manybody wave
function approach for the stationary problem where lead couplings
are time independent and :math:`n_{eq}` in flatband approximation is
obtained from Eq. (48). The parameters are
:math:`\epsilon_0 = \gamma = 0.1` and :math:`t_0 = 100`.

.. seealso::

    The above figure can be obtained by running the two Python scripts:

    :download:`siam_sudden_switch_run_computation.py <siam_sudden_switch_run_computation.py>`

    :download:`siam_sudden_switch_plot_results.py <siam_sudden_switch_plot_results.py>`





References
----------

[1] H. Haug and A. P. Jauho,
`Quantum Kinetics in Transport and Optics of Semiconductors
<https://doi.org/10.1007/978-3-540-73564-9>`_
2nd ed. (Springer, Berlin, 2008).

[2] B. Gaury, J. Weston, M. Santin, M. Houzet, C. Groth, and X. Waintal,
`Numerical simulations of time-resolved quantum electronics <http://dx.doi.org/10.1016/j.physrep.2013.09.001>`_
Phys. Rep. **534**, 1 (2014).

[3] T. Kloss, J. Weston, B. Gaury, B. Rossignol, C. Groth and X. Waintal,
`Tkwant: a software package for time-dependent quantum transport <https://doi.org/10.1088/1367-2630/abddf7>`_
New J. Phys. **23**, 023025 (2021).

[4] A.-P. Jauho, N. S. Wingreen, and Y. Meir,
`Time-dependent transport in interacting and noninteracting resonant-tunneling systems
<https://doi.org/10.1103/PhysRevB.50.5528>`_
Phys. Rev. B **50**, 5528 (1994).

[5] C. W. Groth, M. Wimmer, A. R. Akhmerov, and X. Waintal,
`Kwant: a software package for quantum transport <http://stacks.iop.org/1367-2630/16/i=6/a=063065>`_
New J. Phys. **16**, 063065 (2014).

[6] R.-P. Riwar and T. L. Schmidt, `Transient dynamics of a molecular
quantum dot with a vibrational degree of freedom 
<https://doi.org/10.1103/PhysRevB.80.125109>`_
Phys. Rev. B **80**,125109 (2009).

[7] Y. N. Fernández, M. Jeannin, P. T. Dumitrescu, T. Kloss, J. Kaye, O.
Parcollet, and X. Waintal, `Learning Feynman Diagrams with Tensor Trains
<https://doi.org/10.1103/PhysRevX.12.041018>`_
Phys. Rev. X **12**, 041018 (2022).

Appendix
--------

    .. specialnote:: Nonequilibrium Green functions in flatband approximation


        In the following we derive zero temperature Green functions for a one
        dimensional quantum dot array in flatband approximation. The derivation
        is close to the one in Ref. `[7] <#references>`__, except that we calculate true
        nonequilibrium Green functions such that no fluctuation-dissipation
        theorem is present in the central system. The Green function is defined
        as

        .. math::
           :label: gdef2

           \begin{equation}
              G^{-1} = (\omega - H).
           \end{equation}

        It is practical to write above equation in a block matrix form to
        separate into a finite central system (S) and to the environment (E)
        which represents the semi-infinite leads:

        .. math::
           :label: ginv

           \begin{equation}
           G^{-1} =  \left(
           \begin{array}{cc}
           G_{SS}^{-1} & G_{SE}^{-1} \\
           G_{ES}^{-1} & G_{EE}^{-1}
           \end{array}
           \right), \quad 
           H =  \left(
           \begin{array}{cc}
           H_{SS} & H_{SE} \\
           H_{ES} &  H_{EE}
           \end{array}
           \right).
           \end{equation}

        Each of the Green function blocks with index
        :math:`\alpha, \beta \in \{S, E \}` has again a Keldysh block structure

        .. math::
           :label: gab

           \begin{equation}
           G_{\alpha \beta} =  \left(
           \begin{array}{cc}
           G^R & G^K \\
             &  G^A
           \end{array}
           \right)_{\alpha \beta}, \quad G^{-1}_{\alpha \beta} =  \left(
           \begin{array}{cc}
           (G^R)^{-1} & - (G^R)^{-1} G^K (G^A)^{-1}  \\
             &  (G^A)^{-1} 
           \end{array}
           \right)_{\alpha \beta}.
           \end{equation}

        The separated system and environment Green functions can be obtaind from

        .. math::
           :label: gss

           \begin{align}
            G_{SS}^{-1} &= \omega - H_{SS} - H_{SE} (\omega - H_{EE})^{-1} H_{ES},\\
            G_{EE}^{-1} &= \omega - H_{EE}.
           \end{align}

        We will now concentrate on the Green functions of the system. Using the
        Keldysh blockstructure one finds

        .. math::
           :label: grak

           \begin{align}
             (G^R_{SS})^{-1}  &= \omega - H_{SS} -  H_{SE} G_{EE}^R H_{ES}, \\
             (G^A_{SS})^{-1}  &= \omega - H_{SS} -  H_{SE} G_{EE}^A H_{ES},  \\
             G^K_{SS}         &= G^R_{SS} H_{SE} G_{EE}^K H_{ES} G^A_{SS}. 
           \end{align}

        To invert above equations, the effective Hamiltonian of the retarded
        Green function is written as

        .. math::
           :label: hss

           \begin{equation}
           H_{SS} +  H_{SE} G_{EE}^R H_{ES} = U D U^{-1},
           \end{equation}

        where :math:`D` is a diagonal matrix. We find

        .. math::
           :label: grakw

           \begin{align}
            G^R_{SS}(\omega) &= U (\omega - D)^{-1} U^{-1} , \\
            G^A_{SS}(\omega) &= U^* (\omega - D^*)^{-1} (U^*)^{-1} , \\
            G^K_{SS}(\omega) &= U (\omega - D)^{-1} U^{-1}  H_{SE} G^K_{EE} H_{ES}  U^* (\omega - D^*)^{-1} (U^*)^{-1},
           \end{align}

        where we have used that :math:`G^A(\omega) = (G^R(\omega))^*`. As the
        different leads are not coupled, all :math:`G^{\kappa}_{EE}` with
        :math:`\kappa \in \{ R,A,K\}` are diagonal matrices. One can therefore
        use the simplified notation

        .. math::
           :label: gk

           \begin{equation}
            g^K_\alpha(\omega) \equiv [G^K_{EE}]_{\alpha \alpha} = (1 - 2 f_\alpha(\omega)) [g^R_\alpha - g^A_\alpha] 
           \end{equation}

        for the components of the lead Green functions. We have also set
        :math:`g^{R/A}_\alpha(\omega) \approx g^{R/A}(\mu_\alpha) \equiv g^{R/A}_\alpha`,
        such that the lead Green functions are frequency independent. This is
        also known as flatband approximation. The Fermi function is

        .. math::
           :label: fermi

           \begin{equation}
            f_{\alpha}(\omega)  = \frac{1}{1 + e^{(\omega - \mu_\alpha)/T_\alpha}},
           \end{equation}

        where :math:`\mu_\alpha` is the chemical potential and :math:`T_\alpha`
        the temperature on lead :math:`\alpha`. Performing a Fourier transform
        to the time domaine

        .. math::
           :label: gtfourier

           \begin{equation}
            G(t) = \int_{-\infty}^{\infty} \frac{d \omega}{2 \pi} \, e^{- i \omega t} G(\omega) 
           \end{equation}

        we find for the retarded and the advanced Green functions

        .. math::
           :label: gra

           \begin{align}
            G^R_{SS}(t) &= (2 \pi)^{-1} U I(D, t) U^{-1} ,  \\
            G^A_{SS}(t) &= (2 \pi)^{-1} U^* I(D^*, t) (U^*)^{-1} . 
           \end{align}

        Using contour integration, one finds the frequency integrals for
        :math:`\Im{a} \neq 0`, :math:`t \neq 0` as

        .. math::
           :label: iat

           \begin{equation}
            I(a, t) = \int_{-\infty}^{\infty} d \omega \, e^{- i \omega t} \frac{1}{\omega - a} = 
            \begin{cases}
            - 2 \pi i \, \textrm{sgn}(t) e^{- i a t} \theta(- \Im a t)  &\quad \Re{a} \neq 0 \\
            - \pi i \, \textrm{sgn}(t) e^{- i a t} \theta(- \Im a t)    &\quad  \Re{a} = 0 .
            \end{cases}
           \end{equation}

        To perform Fourier transform of the Keldysh Green function, we write
        matrix function component wise as (Einstein sum convention):

        .. math::
           :label: gkomega

           \begin{equation}
            G^K_{ij}(\omega) = U_{il} (\omega - D)^{-1}_{l} U^{-1}_{lm}  H^{SE}_{mn} g^K_{n}(\omega) H^{ES}_{nm'}  U^*_{m'l'} (\omega - D^*)^{-1}_{l'} (U^*)^{-1}_{l'j}.
           \end{equation}

        In the time domaine, the Keldysh Green function is

        .. math::
           :label: gkt

           \begin{align}
            G^K_{ij}(t) = U_{il} U^{-1}_{lm}  H^{SE}_{mn} (g^R_{n} - g^A_{n}) Q_{n}(D_l, D^*_{l'}, t) H^{ES}_{nm'}  U^*_{m'l'}  (U^*)^{-1}_{l'j}  
           \end{align}

        with

        .. math::
           :label: qt1

           \begin{equation}
            Q_{n}(a, b, t) = \int_{-\infty}^{\infty} \frac{d \omega}{2 \pi} \, e^{- i \omega t} \frac{1 - 2 \theta(\mu_n - \omega)}{(\omega - a)(\omega - b)}. 
           \end{equation}

        Note that we have taken the zero temperature limit
        :math:`T \rightarrow 0` such that
        :math:`f_\alpha(\omega) = \theta(\mu_\alpha - \omega)` in above
        expression. Doing the integral one finds for
        :math:`t \neq 0, \, a \neq b`

        .. math::
           :label: qt2

           \begin{align}
             Q_{n}(a, b, t) &= \frac{1}{2 \pi (a - b)} \Bigl[ \int_{-\infty}^{\infty} d \omega \,  \frac{e^{- i \omega t}}{\omega - a} - \int_{-\infty}^{\infty} d \omega \,  \frac{e^{- i \omega t}}{\omega - b} - 2 \int_{-\infty}^{\mu_n} d \omega \,  \frac{e^{- i \omega t}}{\omega - a} + 2 \int_{-\infty}^{\mu_n} d \omega \,  \frac{e^{- i \omega t}}{\omega - b} \Bigr] \\
		              &= \frac{1}{2 \pi (a - b)} \Bigl[ I(a, t) - I(b, t) + 2  e^{- i \mu_n t} [I^<( a - \mu_n, t) - I^<(b - \mu_n, t) ] \Bigr], \quad \text{if } t \neq 0, \, a \neq b \\
               I^<(a, t) &=  - \int_{-\infty}^{0} d \omega \frac{e^{- i \omega t}}{\omega - a}  \\
               & =
             \begin{cases}
             e^{-i a t} \left[ E_1(-i a t) + 2 \pi i \, \textrm{sgn}(t) \theta(-\Im a t) \theta(-\Re a)  \right]  &\quad \Re{a} \neq 0 \\
             e^{- i a t} [- E_i(i a t) + \pi i \, \textrm{sgn}(t) \theta[- \Im{at}]]    &\quad  \Re{a} = 0
             \end{cases}, \quad \Im{a} \neq 0, t \neq 0 .
           \end{align}

        The two exponential integrals are
        :math:`E_1(z) = \int_z^\infty dx \, e^{-x} / x` for
        :math:`z \in \mathbb{C}` with :math:`|\arg(z)| < \pi` and
        :math:`E_i(x) = -\int_{-x}^\infty dt \, e^{-t} / t` for real and
        non-zero :math:`x`. For :math:`t = 0` one finds

        .. math::
           :label: int1

           \begin{align}
            \int_{-\infty}^{\infty} d \omega \,  \frac{1}{(\omega - a)(\omega - b)} &= \frac{2 \pi i}{a - b} \Bigl(\theta(\Im a) - \theta(\Im b) \Bigr)  ,  \\
            \int_{-\infty}^{\mu} d \omega \,  \frac{1}{(\omega - a)(\omega - b)} &= \frac{\log(a - \mu) - \log(b - \mu)}{a - b}, 
           \end{align}

        such that

        .. math::
           :label: qt3

           \begin{align}
            Q_{n}(a, b, t=0) = \frac{1}{(a - b)} \Bigl[ i \left(\theta(\Im a) - \theta(\Im b) \right)  - \frac{1}{\pi} \left(\log(a - \mu_n) - \log(b - \mu_n)\right)  \Bigr] .
           \end{align}

        Having the three Keldysh Green functions, one can obtain the lesser and
        greater Green functions from the well-known relation

        .. math::
           :label: glessgr

           \begin{align}
            G^< &= \frac{1}{2} \left( G^K - G^R + G^A \right) , \\
            G^> &= \frac{1}{2} \left( G^K + G^R - G^A \right). 
           \end{align}


        **Double quantum dot**

        For the Hamiltonian in Eq. (4) the Hamiltonian matrices are

        .. math::
           :label: hssddot

           \begin{align}
            H_{SS} =  \left(
           \begin{array}{cc}
           \epsilon_L & - \gamma_C \\
           - \gamma_C &  \epsilon_R
           \end{array}
           \right),
           \quad
           H_{SE} =  H_{ES}^\dagger = \left(
           \begin{array}{cc}
           -\gamma_L &  \\
             &  -\gamma_R
           \end{array}
           \right). 
           \end{align}

        The semi-infinite chain with couplings :math:`H_{i, i+i} = -1` can be
        solved exactly and one finds

        .. math::
           :label: grw

           \begin{equation}
            g^R(\omega) = \frac{\omega}{2} - i \sqrt{1 - \left(\frac{\omega}{2}\right)^2}, \quad \omega \in [-2, 2] 
           \end{equation}

        with :math:`g^A(\omega) = (g^R(\omega))^*`. Note that
        :math:`g^R(\omega)` corresponds to the lead self-energy in Eq. (C3) of
        Ref. `[2] <#references>`__.


        **Single quantum dot after suddenly coupling the leads**

        We will derive the lesser Green function :math:`G^<` for a single
        quantum dot and initially empty quantum dot which is suddenly coupled to
        two semi-infinite leads. For simplicity we choose the coupling
        :math:`\gamma` to both leads and also their chemical potential
        :math:`\mu` identical. Moreover we will work at the small coupling limit
        such that one can again use flatband approximation. The derivation is
        close to the one in Ref. `[6] <#references>`__.

        The Hamiltonian matrices for the Hamiltonian in Eq. (12) are

        .. math::
           :label: hssdot

           \begin{align}
            H_{SS} =  \epsilon_0,
           \quad
           H_{SE} =  H_{ES}^\dagger = \left(
           \begin{array}{cc}
           -\gamma &  \\
             &  -\gamma
           \end{array}
           \right).
           \end{align}

        We choose :math:`\mu_{L/R} = 0` such that :math:`g^R_{L/R}(0) = -i`. To
        simplify the notation, the dot Green function is written as
        :math:`G^\kappa \equiv [G^\kappa_{SS}]_{00}`. Retarded and advanced
        Green functions can be written in form of a Dyson equation

        .. math::
           :label: gradot

           \begin{align}
            G^{R/A} &= ( \omega - \epsilon_0 - \Sigma^{R/A})^{-1}
           \end{align}

        where the so-called lead self-energies are

        .. math::
           :label: sigmarak

           \begin{align}
            \Sigma^{R/A}(\omega) &= \mp i \Gamma, \\
            \Sigma^K (\omega) &= 2 \gamma^2 g^K = -2 i \Gamma (1 - 2 f(\omega)),  \\
            \Sigma^< (\omega) &= \frac{1}{2} \left( \Sigma^K - \Sigma^R + \Sigma^A \right) = 2 i \Gamma f(\omega) 
           \end{align}

        where :math:`f` is again the Fermi function and the effective coupling
        constant is :math:`\Gamma = 2 \gamma^2`. Note that we have also used the
        fluctuation-dissipation relation for the lead Green functions

        .. math::
           :label: gkw

           \begin{equation}
             g^K(\omega) = (1 - 2 f(\omega))(g^R(\omega) - g^A(\omega) ) = - 2 i (1 - 2 f(\omega)). 
           \end{equation}

        The the time domaine, the Dyson equation for the retarded and the
        advanced Green function can be written as

        .. math::
           :label: grattp

           \begin{equation}
            G^{R/A}(t,t') = G^{R/A}_0(t - t') + \int_0^\infty \int_0^\infty dt_1 dt_2 G^{R/A}_0(t - t_1) \Sigma^{R/A}(t_1 - t_2) G^{R/A}(t_1,t') 
           \end{equation}

        where the subscript 0 refers to the Green function without lead

        .. math::
           :label: gra0

           \begin{equation}
           G^{R/A}_0(t) = \mp i \theta(\pm t) e^{- i \epsilon_0 (t - t')}. 
           \end{equation}

        and the self-energy in the time domaine is

        .. math::
           :label: sigmaless

           \begin{align}
            \Sigma^{R/A}(t) &= \mp i \Gamma \delta(t),  \\
            \Sigma^{<}(t) &= \frac{i \Gamma}{\pi} \int_{-\infty}^0 d \omega \, e^{- i \omega t}, 
           \end{align}

        where we have used again the zero temperature limit for
        :math:`\Sigma^{<}`. The full retarded and advanced Green with leads are

        .. math::
           :label: grattp2

           \begin{align}
           G^{R/A}(t, t') &=  \mp i \theta(\pm(t - t')) e^{- i \epsilon_0 (t - t') \mp \Gamma(t - t')} 
           \end{align}

        and solve above Dyson equation. The lesser Green function can be written
        as an integral equation `[1] <#references>`__:

        .. math::
           :label: gless2

           \begin{equation}
             G^< = (1 + G^R \Sigma^R) G^<_0 (1 + G^A \Sigma^A) + G^R \Sigma^< G^{A}. 
           \end{equation}

        This form is practical for an initially empty dot as then the first term
        is zero. In our case, above equation takes the explicit form

        .. math::
           :label: gless3

           \begin{align}
             G^<(t, t') &=  \int_0^\infty dt_1 \int_0^\infty  dt_2 G^R_0(t - t_1) \Sigma^<(t_1 - t_2) G^A(t_1 - t') \\
                &= \frac{i \Gamma}{\pi} e^{- i \epsilon_0 (t - t') - \Gamma(t + t')} \int_{-\infty}^0 d \omega \int_0^t dt_1 \int_0^{t'} dt_2  e^{- i (\omega - \epsilon_0) t + \Gamma t} e^{i (\omega - \epsilon_0) t' + \Gamma t'}. 
           \end{align}

        After integrating over :math:`t_1` and :math:`t_2` one finds

        .. math::
           :label: gless4

           \begin{align}
             G^<(t, t') =    \theta(t) \theta(t') \frac{i \Gamma}{\pi} e^{-i \epsilon_0 (t - t')} \int_{-\infty}^0 d \omega  \frac{1}{(\omega - \epsilon_0)^2 + \Gamma^2} \left( e^{-i (\omega - \epsilon_0) t} - e^{- \Gamma t}\right)
           \left( e^{i (\omega - \epsilon_0) t'} - e^{- \Gamma t'}\right).  
           \end{align}

        As mentioned before, this form is basically equivalent to Eq. (15) in
        Ref. `[6] <#references>`__, except of the oscillating factor
        :math:`e^{-i \epsilon_0 (t - t')}` which is missing in that reference.
        One can perform the remaining frequency integral via contour integration
        to finally obtain

        .. math::
           :label: gless5

           G^<(t, t') &=    \theta(t) \theta(t') \frac{1}{2 \pi} \Bigl[  I^<(\epsilon_0 - i \Gamma, t - t') - I^<(\epsilon_0 + i \Gamma, t - t') + 2 \pi i n_{eq} e^{-i \epsilon_0 (t - t') - \Gamma (t + t')}  \\
            & \qquad \quad \quad \quad  - e^{i \epsilon_0 t' - \Gamma t'} \left[I^<(\epsilon_0 - i \Gamma, t) - I^<(\epsilon_0 + i \Gamma, t)\right] 
            \\
            & \qquad \quad \quad \quad - e^{-i \epsilon_0 t - \Gamma t} \left[I^<(\epsilon_0 - i \Gamma, -t') - I^<(\epsilon_0 + i \Gamma, -t')\right] 
            \Bigr] , \\
           G^<(t, t) &=    \theta(t)  \Bigl[    i n_{eq} \left(1 + e^{- 2 \Gamma t} \right) 
            - \frac{e^{- \Gamma t}}{2 \pi}  \bigl(e^{i \epsilon_0 t} \left[I^<(\epsilon_0 - i \Gamma, t) - I^<(\epsilon_0 + i \Gamma, t) \right]  \\
            &\qquad \quad  - e^{-i \epsilon_0 t} \left[ I^<(\epsilon_0 - i \Gamma, -t) - I^<(\epsilon_0 + i \Gamma, -t) \right] \bigr) 
           \Bigr],

        with

        .. math::
           :label: neq2

           \begin{equation}
             n_{eq} = \frac{\Gamma}{\pi}\int_{-\infty}^0 d \omega  \frac{1}{(\omega - \epsilon_0)^2 + \Gamma^2} = \frac{1}{\pi} \arctan \left(-\frac{ \epsilon_0}{\Gamma} \right) + \frac{1}{2}.
           \end{equation}

