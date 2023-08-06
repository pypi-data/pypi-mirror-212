.. _pitfalls:


Frequent pitfalls encountered when doing Tkwant simulations
===========================================================

Tkwant has been designed to be as simple to use and as automatic as
possible. Yet, time-dependent simulations are not easy and require a
working understanding of the underlying theory. One may encounter
several problems that affect the accuracy or the validity of the
simulations. Whenever possible, results should be validated with a known
benchmark and the accuracy of the convergence (time-steps, manybody
integral, absorbing boundary conditions) explicitly tested.

In this section we list difficulties that are often encountered when
performing simulations with Tkwant. We encourage users, especially
inexperienced ones, to systematically check at least points 1 to 5 when
starting a new type of simulation or moving to a new regime. The
remaining points are less critical, but should also be checked for new
problems, in case of doubt or persistent problems.

As a general advise we recommend to check the standard output (stdout) for
warning messages from Tkwant. The warnings in the log output are often a first hint to see where a
calculation is getting stuck or what is missing.
One can also increase the verbosity of the logged output with

.. code-block:: python

    import tkwant
    import logging

    tkwant.logging.level = logging.INFO  # possible levels (increasing verbosity): WARNING, INFO, DEBUG

at the beginning of the Tkwant script. Further details are explained in
the :ref:`logging` tutorial.

Convergence of the manybody integral (1/2)
------------------------------------------

Problem
~~~~~~~

The manybody integral is poorly approximated (not enough sampling points
and/or slowly converging integral) and the result inaccurate.

Diagnostic
~~~~~~~~~~

Perform adaptive integral refinement of
:math:`\texttt{tkwant.manybodyState()}` with the method:

.. code-block:: python

    refine_intervals()

at various stages of the calculation. If the results change, then the
previous result were not converged. Without refinement, the numerical
result is likely to be wrong, so we recommend to always use this method
unless you have experience with numerical integration. Check the
tutorial section
`adaptive refinement and error estimate <https://tkwant.kwant-project.org/doc/stable/tutorial/manybody.html#adaptive-refinement-and-error-estimate>`_
for more details.

Solution
~~~~~~~~

Try adding further calls to :math:`\texttt{refine_integrals()}` at
different times in the simulation and check if the results change.
Adding calls to this function always improve the accuracy but can be
dear in computational time. At the initial time :math:`t=0` the manybody
integral is refined by default, such that no additional call to
:math:`\texttt{refine_integrals()}` is needed.

Convergence of the many-body integral (2/2)
-------------------------------------------

Problem
~~~~~~~

Adaptive refinement with :math:`\texttt{refine_intervals()}` blocks and
endlessly adds points to refine the integral without convergence.

Diagnostic
~~~~~~~~~~

In some problems, the many-body integral can converge very poorly due to
a difficult integrant with e.g. very sharp resonances. A typical example
is a very large quantum dot almost decoupled from its leads. Plotting
the function that is integrated usually helps to identify the problem.
For the integrator to work properly, the integrant should look
resonnably smooth.

The MPI parallelization makes it difficult to plot the integrand
directly from the manybody solver, but Tkwant provides the auxiliary
routine :math:`\texttt{tkwant.manybody.ManybodyIntegrand}` for
diagnostic purpose. The following code snipped shows its use for the the
density integrand which is plotted again momentum :math:`k` within the
range :math:`kmin` and :math:`kmax` at a certain time snapshot. Note
that one can only plot the contribution of a certain, lead and band to
the manybody integral:

.. code-block:: python

    import tkwant
    import kwant
    import numpy as np
    import matplotlib.pyplot as plt

    # user defined system definition
    syst = make_my_kwant_system().finalized()

    # define the momentum range in between which the integrand will be analyzed
    kmin = 0.01
    kmax = np.pi/2

    # specify the lead and band index
    interval = tkwant.manybody.Interval(lead=0, band=0, kmin=kmin, kmax=kmax)

    # define an operator
    density_operator = kwant.operator.Density(syst, sum=True)

    # define a time where to evaluate the integrand
    integrand = tkwant.manybody.ManybodyIntegrand(syst, interval, density_operator, time=100)

    # plot the integrand on some arbitrary points within [kmin, kmax]
    k = np.linspace(kmin, kmax)
    plt.plot(k, integrand.vecfunc(k))

Solution
~~~~~~~~

The difficulty often actually originates from the physical problem. The
solution is often to sligthly change the problem to bring it to a
simpler regime. For instance, in the case of a quantum dot, increasing
the coupling to the leads will facilitates the convergence by making the
resonances less narrow. In some contexts, increasing the Fermi energy in
the lead can also help, see the discussion in section 10.1 of Ref. `[1] <#references>`__
(Figure 15).

Presence of unincluded boundstates
----------------------------------

Problem
~~~~~~~

Manybody observables are wrong due to the negligence of existing
boundstates.

Diagnostic
~~~~~~~~~~

Check for the prensence of boundstates in your system with the function:

.. code-block:: python

    boundstates_present()

When this function returned :math:`\texttt{True}`, the system contains
boundstates. These are not automatically handled by Tkwant but its up to
the user to include them. Ignoring boundstates might lead to wrong
results, at least for the density.

Solution
~~~~~~~~

Read the tutorial :ref:`boundstates`
for more information and to learn how to include them.

Error in Hamiltonian construction or unphysical parameter regime
----------------------------------------------------------------

Problem
~~~~~~~

The initial Hamiltonian is wrong and/or the parameters are set to
unphysical values.

Diagnostic
~~~~~~~~~~

-  Plot the Kwant system which defines the Hamiltonian via:

.. code-block:: python

    kwant.plot()

Check visually if all sites, couplings and leads appear as expected.

-  Plot the banstructure with the help of the
   `kwantSpectrum <https://kwant-project.org/extensions/kwantspectrum>`_ package:

.. code-block:: python

    import kwantspectrum as ks
    import kwant
    import numpy as np
    import matplotlib.pyplot as plt

    syst = my_kwant_system_with_leads().finalized()

    lead_index = 0  # change this number to the intended lead
    spec = ks.spectrum(syst.leads[lead_index])
    momenta = np.linspace(-np.pi, np.pi, 500)
    for band in range(spec.nbands):
        plt.plot(momenta, spec(momenta, band), label='n=' + str(band))

Check that the energy dispersion is as expected and that there are
available states below the chemical potential :math:`\mu`. Note that
without defining the occupation explicitly (via
:math:`\texttt{tkwant.manybody.lead_occupation()}`) Tkwant will assume
:math:`\mu = 0` for all leads present in the system. Read the
`manybody tutorial <https://tkwant.kwant-project.org/doc/stable/tutorial/manybody.html#chemical-potential-and-temperature-of-the-leads>`_
for more details.

-  Plot the values of important matrix elements of the system. For
   instance a 2D plot of the onsite potential can help to see if it has
   been set properly.

Solution
~~~~~~~~

Change the Hamiltonian to the physically correct one.

Observables
-----------

Problem
~~~~~~~

Error in the mapping between the result obtained from a Kwant operator
and the lattice positions (not obvious for a system with more than one
dimensions or orbitals).

Diagnostic
~~~~~~~~~~

The result obtaind from a Kwant operator is packed in a one-dimensional
array, check that you're using the correct ordering for that array.

The mapping from a lattice position to the index in the array can be
obtained from the class :math:`\texttt{siteId}`

.. code-block:: python

    
    # system construction
    lat = kwant.lattice.square(a=1, norbs=2)
    syst = kwant.Builder()
    .
    .
    syst = syst.finalized()

    idx = tkwant.system.siteId(syst, lat)
    index = idx(i, j)  # map integer lattice positions (i,j) to the array index

where :math:`\texttt{syst}` refers to a finalized Kwant system,
:math:`\texttt{lat}` the Kwant lattice and :math:`\texttt{i, j}` the integer lattice
positions one is interested. The Kwant ordering of the sites can also be
printed with:

.. code-block:: python
    
    for site in syst.sites:
        print(site)

Solution
~~~~~~~~

Don't assume the ordering of the results, use the above to know how the
data as actually stored.

Unsufficient accuracy in perturbation interpolation
---------------------------------------------------

Problem
~~~~~~~

For abruptly varying time-dependent perturbations :math:`𝑊(𝑡)` of the
Hamiltonian, the result becomes inaccurate.

Diagnostic
~~~~~~~~~~

Tkwant interpolates the time-dependent perturbation :math:`𝑊(𝑡)` of the
Hamiltonian using an adaptive cubic spline interpolation. If :math:`𝑊(𝑡)`
becomes strongly varying however, this interpolation becomes inaccurate.

We recommend to perform a second simulation with the interpolation turned off
and to check if the result changes.

Solution
~~~~~~~~

Turn of the interpolation, as explained in:

- `Onebody time-dependent perturbation <https://tkwant.kwant-project.org/doc/stable/tutorial/onebody\_advanced.html#time-dependent-perturbation>`_
- `Manybody time-dependent perturbation <https://tkwant.kwant-project.org/doc/stable/tutorial/manybody\_advanced.html#time-dependent-perturbation>`_

Spurious reflections on the leads
---------------------------------

Problem
~~~~~~~

The result shows spurious reflections by a lead.

Diagnostic
~~~~~~~~~~

Tkwant provives automatic and adaptive boundary conditions to prevent
reflections from the lead. So far, we have not observed any failure of
the automatic tuning of the boundary conditions, but it might happen.

To check that no reflection is occurring, one can perform a second
simulation with a smaller reflection coefficient. Alternatively, one can
also analyse the (static) lead reflection.

Solution
~~~~~~~~

Make sure that there are no spurious reflections at the lead.

The following tutorials explain how to perform the diagnostic and ensure
the absence of spurious reflections.

- `Onebody boundary conditions <https://tkwant.kwant-project.org/doc/stable/tutorial/onebody\_advanced.html#boundary-conditions>`_
- `Manybody boundary conditions <https://tkwant.kwant-project.org/doc/stable/tutorial/manybody\_advanced.html#boundary-conditions>`_


and to compare if the result changes. One can also analyse the lead
reflection or tweak the boundary conditions as explained in the :ref:`boundary` tutorial.

Unsufficient time-stepping accuracy
-----------------------------------

Problem
~~~~~~~

The accuracy of the time integration of the Schrodinger equation is
insufficient.

Diagnostic
~~~~~~~~~~

Tkwant has automatic routines to adaptively integrate the onebody
Schrödinger equation in time. So far, we have not observed any failure
but it might happen.

To check for the accuracy of the time-dependent Schrodinger solver,
perform a second simulation with a higer accuracy of the adaptive
algorithm and check for convergence.

Solution
~~~~~~~~

Use a high enough accuracy. See,

- `Onebody time integration <https://tkwant.kwant-project.org/doc/stable/tutorial/onebody\_advanced.html#time-integration>`_
- `Manybody time integration <https://tkwant.kwant-project.org/doc/stable/tutorial/manybody\_advanced.html#time-integration>`_

for the tutorials on this aspect of the numerical algorithm.

Miscellaneous problems
----------------------

A list other known problems that may occur is given in the :ref:`faq` section.

References
----------

[1] B. Gaury, J. Weston, M. Santin, M. Houzet, C. Groth, and X. Waintal,
`Numerical simulations of time-resolved quantum electronics <http://dx.doi.org/10.1016/j.physrep.2013.09.001>`_
Phys. Rep. **534**, 1 (2014).
