.. _boundstates:

Accounting for possible boundstates present in the system
=========================================================

.. note::

    Quantum transport focuses on propagating states. However sometimes boundstates can play a major role (e.g. the Andreev states in Josephson junctions) or are simply there and must be taken into account. Tkwant does not handle boundstates automatically, but provides methods to detect and include them manually.
    The user must be careful, as neglecting existing boundstates can lead to incorrect results.
    While in the other tutorials boundstates were either not present or did not play a role, this tutorial demonstrates the detection and proper handling of boundstates in Tkwant with a simple example.

Boundstates are localized states inside the central region of an
infinite scattering systems which decay exponentially in the leads. They
are solutions of the Schrödinger equation and might occur in addition to
the usual propagating states. General algorithms have been derived to
calculate boundstates in arbitrary tight-binding system numerically `[1] <#references>`__,
but they can often be calculated by simply diagonalizing a finite system
that encompass the scattering region and a portion of the leads.

In this tutotiral, we illustrate the procedure to detect their presence,
calculate them and include them in a Tkwant simulation on a simple toy
example. We consider an infinite one-dimensional wire with a single
impurity at a central site. For an attractive impurity potential, a
single boundstate appears and its energy and its wavefunction can be
calculated easily either numerically or analytically.

Model
-----

We consider the simple tight-binding system of an infinite
one-dimensional chain. At the center with lattice index zero there is an
additional on-site potential with strength :math:`V`. In second
quantization the Hamiltonian is

.. math::

   \begin{align}
     \hat{H} &=  -\gamma \sum_{i=-\infty}^\infty  c^\dagger_{i+1} c_{i} + \text{h.c.} + V c^\dagger_{0} c_{0} , \tag{1}
   \end{align}

where :math:`c^\dagger_i` (:math:`c_i`) are the fermionic creation
(annihilation) operator on site :math:`i` and :math:`\gamma` is the
hopping matrix element. In the following we set :math:`\gamma = 1` and
work in dimensionless units.

Analytical calculation of the boundstate
----------------------------------------

To proceed, we consider the discrete Schrödinger equation

.. math::

   \begin{align}
     H \Psi = E \Psi , \tag{2}
   \end{align}

where :math:`H` is the Hamiltonian matrix,
:math:`\Psi = \{\psi_i, \psi_{i+1}, \ldots \}` the projection of the
wavefunction on the lattice sites :math:`i` and :math:`E` the energy.
For our model the discrete Schrödinger equation can be written
explicitly

.. math::

   \begin{equation}
    -\psi_{i+1} - \psi_{i-1} + V_i \psi_{i} = E \psi_{i} , \tag{3}
   \end{equation}

with :math:`V_i = V \delta_{i, 0}`. The states are also required to be
normalized and we fix the normalization to be:

.. math::

   \begin{align}
     \sum_i |\psi_i|^2 = 1 . \tag{4}
   \end{align}

One possible solution of Eqs. (3) and (4) are linar combination of
plain-wave solution of the form
:math:`\psi_n = c_1 e^{i k n} + c_2 e^{-i k n}`. These are the
well-known scattering states with the corresponding dispersion relation
:math:`E(k) = - 2 \gamma \cos(k)`. For the boundstates we are however
looking for solutions of the form

.. math::

   \begin{align}
     \psi_n = a \lambda^{|n|}, \quad |n| \geq 1 \tag{5}
   \end{align}

with :math:`a, \lambda \in \mathcal{R}` and :math:`\lambda > 0`. The
normalization condition Eq. (4) requires that
:math:`\lim_{i \rightarrow \pm \infty} \psi_i = 0`, such that
:math:`|\lambda| < 1`. We can fix :math:`\lambda` and the normalization
constant :math:`a` and :math:`\psi_0` by simple wave function matching
at the impurity. Equation (3) leads to

.. math::

   \begin{align}
    \hspace{31ex}  -\psi_{1} - \psi_{-1} &= (E - V) \psi_0 , \hspace{31ex}  \tag{6a} \\
     -\psi_{2} - \psi_{0} &= E \psi_1 , \tag{6b}\\
     -\psi_{3} - \psi_{1} &= E \psi_2 . \tag{6c}
   \end{align}

From Eq. (6c) and the ansatz Eq. (5) we find

.. math::

   \begin{align}
     \lambda = \frac{- E - \sqrt{E^2 - 4}}{2} . \tag{7}
   \end{align}

For :math:`\lambda` to be real the argument in the square root must be
positive such that :math:`|E| \geq 2`. We will focus on solutions for
attractive potentian :math:`V \leq 0` with negative energy :math:`E`,
such that only the root with the negative sign is possible as
:math:`0 < \lambda < 1`. Together with Eqs. (6a, 6b) one finds the
boundstate energies

.. math::

   \begin{align}
     E &=  - \sqrt{V^2 + 4} , \tag{8}
   \end{align}

such that the boundstate exists for all :math:`V < 0`. In terms of
:math:`V`, Eq. (7) writes

.. math::

   \begin{align}
     \lambda = \frac{V + \sqrt{V^2 + 4}}{2} . \tag{9}
   \end{align}

The constant :math:`a` can be fixed from the normalization condition Eq.
(4):

.. math::

   \begin{align}
     \sum_i |\psi_i|^2 = 2 \sum_{i=1}^{\infty} |\psi_i|^2 + |\psi_0|^2 = 2 a^2 \frac{\lambda^2}{1 - \lambda^2} + |\psi_0|^2 = 1 .
   \end{align}

Together with Eq. (6a) we find

.. math::

   \begin{align}
     \psi_0 = a , \quad a = \sqrt{\frac{1 - \lambda^2}{1 + \lambda^2}} . \tag{10}
   \end{align}

Observables in presence of boundstates
--------------------------------------

The expectation value of an observable

.. math::

   \begin{equation}
   \label{eq:observable}
   \hat{\mathbf{A}} = \sum_{i,j} \mathbf{A}_{ij} \hat{c}^\dagger_i \hat{c}_j , \tag{11}
   \end{equation}

can be calculated in in a wave-function based approach in the presence
of boundstates as `[2] <#references>`__

.. math::

   \begin{align}
    \langle \hat{\mathbf{A}} \rangle (t)
     = \sum_{\alpha ij} \int \frac{dE}{2 \pi} f_\alpha(E)  \psi_{\alpha E}^*(t,i) \mathbf{A}_{ij} \psi_{\alpha E}(t,j) &
     +\sum_{b ij} f(E_b)  \psi_{b}^*(t,i) \mathbf{A}_{ij} \psi_{b}(t,j) , \tag{12}
   \end{align}

where :math:`\psi_{\alpha E}(t, i)` is the scattering wave function for
lead :math:`\alpha`, site index :math:`i` and time :math:`t`, and
:math:`f_\alpha` is the Fermi function of lead :math:`\alpha`. The
second term sums over the boundstate wavefunctions :math:`\psi_{b}` with
:math:`f(E_b)` the Fermi function in the central region and :math:`E_b`
are the boundstate energies. Note that from a theoretical point of view,
the Fermi function for the boundstate does not have to be at the same
temperature or chemical potential than the leads. Hence it is not
strictly speaking incorrect to ignore the bound states (i.e. assuming a
large negative chemical potential for them) but often unphysical at
least in the cases where the system is initially in thermal equilibrium.
For the special case of the density we find

.. math::

   \begin{align}
   n(t, i) = \langle c^\dagger_i c_i \rangle (t)
   &= \sum_{\alpha} \int \frac{dE}{2 \pi} f_\alpha(E)  |\psi_{\alpha E}(t,i) |^2  + \sum_{b} f(E_b)  |\psi_{b}(t,i)|^2 . \tag{13}
   \end{align}

A very important remark for the detection of boundstates is that a given
site contain exactly one electron when all the states are filled. Hence,
if we diregard the Fermi functions in the above equation, one finds that
Kwant `[2] <#references>`__ and Tkwant `[3] <#references>`__ give :math:`n(t, i) = 1` in for all times
:math:`t` and all sites :math:`i`,

.. math::

   \begin{align}
   \sum_{\alpha} \int \frac{dE}{2 \pi}  |\psi_{\alpha E}(t,i) |^2  + \sum_{b}  |\psi_{b}(t,i)|^2  = 1. \tag{14}
   \end{align}

Numerical solution
------------------

We show in the following how to calculate the boundstates numerically
for above model and how to include them into Tkwant. We first include
standard Python packages alongside Kwant, Tkwant and KwantSpectrum `[3] <#references>`__.

.. jupyter-execute::

    import tkwant
    import kwant
    import kwantspectrum as ks
    
    import numpy as np
    import matplotlib.pyplot as plt

Characterization of the boundstate and comparison to the analytical result
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We first implement two functions that return the analytical results:
:math:`\texttt{bs_psi_func}` calculate the boundstate wave function Eqs.
(5, 9, 10) and :math:`\texttt{bs_energy_func}` for the groundstate
energy Eq. (8).

.. jupyter-execute::

    def bs_psi_func(v, i):
        lbda = 0.5 * (v + np.sqrt(v**2 + 4))
        lbda2 = lbda**2
        a = np.sqrt((1 - lbda2)/(1 + lbda2))
        return a * pow(lbda, abs(i))
    
    
    def bs_energy_func(v):
        return - np.sqrt(v**2 + 4)

For the numerical solution we first implement the model Eq. (1) with
Kwant. We also set the parameters such to have a boundstate present.

.. jupyter-execute::

    def make_system(L, V, a=1):
    
        lat = kwant.lattice.square(a=a, norbs=1)
        syst = kwant.Builder()
    
        # central system
        syst[(lat(i, 0) for i in range(-L, L))] = 0
        syst[lat(0, 0)] = V
        syst[lat.neighbors()] = -1
    
        # leads
        lead = kwant.Builder(kwant.TranslationalSymmetry((-a, 0)))
        lead[lat(0, 0)] = 0
        lead[lat.neighbors()] = -1
        syst.attach_lead(lead)
        syst.attach_lead(lead.reversed())
    
        return syst
    
    # parameters
    L = 20
    V = -2.5
    
    syst = make_system(L, V).finalized()
    
    hamiltonian = syst.hamiltonian_submatrix()

In the previous lines, :math:`\texttt{hamiltonian}` is the Hamiltonian
matrix of the finite central system with size
:math:`(2 L + 1) \times (2 L + 1)`. This matrix could have been defined
also directly, without using Kwant. One can plot the elements of this
matrix for
:math:`\{\psi_{-2}, \psi_{-1}, \psi_{0}, \psi_{1}, \psi_{2} \}` to see
that it corresponds indeed to Eq. (3):

.. jupyter-execute::

    np.array(np.real_if_close(hamiltonian[L-2:L+3, L-2:L+3]))

Using standard linear algebra tools, we calculate the eigenvalues and
eigenvectors of the matrix:

.. jupyter-execute::

    eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian)

Boundstate energy
^^^^^^^^^^^^^^^^^

The eigenvalues correspond to discrete energy levels of the finite
system. We plot the eigenvalues together with the energy dispersion of
one lead, which corresponds to a semi-infinite system without any onsite
energy.

.. jupyter-execute::

    spec = ks.spectrum(syst.leads[0])
    momenta = np.linspace(-np.pi, np.pi, 500)
    
    plt.plot([-1, 1], 2 * [eigenvalues[0]], c='#e15759', label=r'boundstate')
    
    for i, energy in enumerate(eigenvalues[1:]):
        plt.plot([-1, 1], 2 * [energy], c='#f28e2b', label=r'plane waves' if i == 0 else "")
    
    for band in range(spec.nbands):
        plt.plot(momenta, spec(momenta, band), label='contineous band')
    
    plt.xlabel(r'$k$')
    plt.ylabel(r'$E$')
    plt.legend()
    plt.show()

One finds that almost all eigenvalues are located inside the band
opening. The corresponding states are plain-wave like solutions. The
energy levels outsite the contineous band correspond to the boundstate.
We find only one in this model. We copy the corresponding state and
energy into

.. jupyter-execute::

    bs_energy = eigenvalues[0]
    psi_bs = eigenvectors[:, 0]

and compare the energy to the analytical result:

.. jupyter-execute::

    bs_analyt = bs_energy_func(V)
    print('boundstate energy (numeric): {:.4f}, (analytic): {:.4f}, diff: {:.4e}'.
          format(bs_energy, bs_analyt, np.abs(bs_energy - bs_analyt)))

Boundstate wave function
^^^^^^^^^^^^^^^^^^^^^^^^

We can also plot the value of :math:`\psi_i` on the lattice positions
and compare to the analytical result. Summing up :math:`|\psi_i|^2` on
all sites we can also check that the normalization Eq. (4) holds:

.. jupyter-execute::

    sites = [s.pos[0] for s in syst.sites]
    plt.plot(sites, np.real_if_close(psi_bs), label='numeric')
    plt.plot(sites, [bs_psi_func(V, i) for i in sites], '--', label='analytic')
    
    plt.xlabel(r'lattice site $i$')
    plt.ylabel(r'$\psi_i$')
    plt.legend()
    plt.show()
    
    print('normalization: {:.4f}'.format(np.sum(np.abs(psi_bs)**2)))

Wrong equilibrium density in Tkwant due to a missing boundstate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Although boundstates do not contribute to transport, a proper inclusion
is nessessary when calculating manybody observables such as the density
:math:`n(t, i)`. Here we show the error in the equilibrium density at
initial time :math:`t=0` when the existing boundstate is not properly
included. To do this, we calculate the onside density using Eq. (13),
neglecting the second term with the contribution of the boundstates. The
numerical calculation is easily to perform with Tkwant, and we fill up
all bands by setting the chemical potential :math:`\mu` to a value
higher than the largest band energy, which in this case is two. The
deviation of the density from one near the impurity is the signature of
the missing boundstate.

.. jupyter-execute::

    occupations = tkwant.manybody.lead_occupation(chemical_potential=4)
    density_operator = kwant.operator.Density(syst)
    
    state = tkwant.manybody.State(syst, tmax=1, occupations=occupations)
    density = state.evaluate(density_operator)
    
    plt.plot(sites, density)
    plt.xlabel(r'lattice site $i$')
    plt.ylabel(r'$n(t=0)$')
    plt.show()

Detecting boundstates with Tkwant
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tkwant provides the boolian function
:math:`\texttt{boundstates_present()}` to check if boundstates are
present:

.. jupyter-execute::

    syst_1 = make_system(L, V).finalized()
    print("boundstates present: {}".format(tkwant.manybody.boundstates_present(syst_1)))
    
    syst_2 = make_system(L, V=0).finalized()
    print("boundstates present: {}".format(tkwant.manybody.boundstates_present(syst_2)))

Internally the function :math:`\texttt{boundstates_present()}` checks
for the density deviation from one as shown before.

Including boundstates in Tkwant
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tkwant does not automatically include boundstates. It merly provides a
mechanism to manually add boundstates manually to the manybody state. To
do this, the class :math:`\texttt{tkwant.manybody.State()}` provides a
method called :math:`\texttt{add_boundstate()}`. The boundstates must be
added at initial time:

.. jupyter-execute::

    occupations = tkwant.manybody.lead_occupation(chemical_potential=4)
    density_operator = kwant.operator.Density(syst)
    
    state = tkwant.manybody.State(syst, tmax=1, occupations=occupations)
    state.add_boundstate(psi_bs, bs_energy)

In case of several contributing boundstates they must be added one by
one.

Note that the manybody wavefunction behaves normally, such that
:math:`\texttt{evolve()}` and :math:`\texttt{refine_intervals()}` work
as before and the boundstates evolved forward in time like the
scattering states of the system. One can check that the density after
the procedure is again one everywhere:

.. jupyter-execute::

    density = state.evaluate(density_operator)
    plt.plot(sites, density)
    plt.xlabel(r'lattice site $i$')
    plt.ylabel(r'$n(t=0)$')
    plt.show()


References
----------

[1] M. Istas, C. Groth, A. R. Akhmerov, M. Wimmer, and X. Waintal,
`A general algorithm for computing bound states in infinite tight-binding systems <http://dx.doi.org/10.21468/SciPostPhys.4.5.026>`_
SciPost Phys. **4**, 26 (2018).

[2] C. W. Groth, M. Wimmer, A. R. Akhmerov, and X. Waintal,
`Kwant: a software package for quantum transport <http://stacks.iop.org/1367-2630/16/i=6/a=063065>`_
New J. Phys. **16**, 063065 (2014).

[3] T. Kloss, J. Weston, B. Gaury, B. Rossignol, C. Groth and X. Waintal,
`Tkwant: a software package for time-dependent quantum transport <https://doi.org/10.1088/1367-2630/abddf7>`_
New J. Phys. **23**, 023025 (2021).
