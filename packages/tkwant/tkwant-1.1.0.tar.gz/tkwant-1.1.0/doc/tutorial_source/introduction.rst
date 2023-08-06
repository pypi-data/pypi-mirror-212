.. _introduction:

Introduction
============

Tkwant is a Python package for the simulation of quantum nanoelectronics devices on which
external time-dependent perturbations are applied. Tkwant is an extension of the `Kwant <https://kwant-project.org>`_  package
and can handle the same types of systems: discrete tight-binding like
models that consist of an arbitrary central region connected to semi-infinite electrodes, also called leads.
For such systems, tkwant provides algorithms to simulate the time-evolution of manybody expectation values, as e.g. densities and currents.

.. _system:

.. figure:: scattering_region.png
    :width: 500px


    Sketch of a typical open quantum system which can
    be simulated with Tkwant. A central scattering region (in
    black) is connected to several leads (in grey). Each lead
    represents a translationally invariant, semi-infinite system in
    thermal equilibrium. Sites and hopping matrix elements are
    represented by dots and lines. The regions in red indicate a
    time-dependent perturbation, in this example a global voltage
    pulse :math:`V_p (t)` on lead 0 and a time-dependent voltage :math:`V_g (t)` on
    a gate inside the scattering region.
    The figure is taken from Ref. `[1] <#references>`__.


**Input**: A tight-binding Hamiltonian of generic form

.. math::

       \hat{H}(t) = \sum_{ij} H_{ij}(t) \hat{c}^\dagger_i \hat{c}_j

as well as the chemical potential :math:`\mu` and the temperature :math:`T` in each lead.

**Output**: Time-dependent manybody expectation values, such as
the electron density :math:`n_i(t) = \langle \hat{c}^\dagger_i \hat{c}_i \rangle`
an currents 
:math:`j_i(t) = i[\langle \hat{c}^\dagger_i \hat{c}_{i+1} \rangle - \langle \hat{c}^\dagger_{i+1} \hat{c}_{i} \rangle]`.
We refer to Tkwant's main paper Ref. `[1] <#references>`__  for the technical background.


Outline of the tutorial
-----------------------

The first tutorial sections :ref:`getting_started` and :ref:`fabry_perot` dives directly into Tkwant with two simple examples.
While the first one is a simple toy example for educative purpose, the
second one is full fledged example, which has been described in detail in Ref. `[1] <#references>`__.
Tkwant's core concepts to solve time-dependent manybody problems are explained in section :ref:`manybody`.
Understanding this section allows one to use Tkwant effectively and to be able to perform realistic simulations.
Another important tutorial section is :ref:`boundstates`, as Tkwant does not handle boundstates automatically.
Technical details are covered in the sections :ref:`onebody_advanced`, :ref:`manybody_advanced`
and :ref:`boundary`. These sections can be skipped in a first tour and are intended for advanced users who are interested to change the default behavior.
The two sections :ref:`mpi` and :ref:`logging` introduce both topics at a beginner's level and give some hands-on advice.
Although not necessary for a basic understanding, these topics are likely to be relevant in practice.
The section :ref:`examples` section summarizes several complete Tkwant examples.
Learning directly from the examples might be a good starting point especially for experienced Kwant users.
Finally, we strongly recommend users to follow the advices in :ref:`pitfalls` to check their results for validity.


References
----------

[1] T. Kloss, J. Weston, B. Gaury, B. Rossignol, C. Groth and X. Waintal,
`Tkwant: a software package for time-dependent quantum transport <https://doi.org/10.1088/1367-2630/abddf7>`_
New J. Phys. **23**, 023025 (2021),
`arXiv:2009.03132 [cond-mat.mes-hall]. <https://arxiv.org/abs/2009.03132>`_
