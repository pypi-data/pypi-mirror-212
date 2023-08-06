:orphan:

.. _graphene:

Pulse propagation in a graphene quantum dot
===========================================

.. jupyter-execute::
    :hide-code:

    # suppress jupyter warnings messages when calling kwant.plot()
    import matplotlib.pyplot, matplotlib.backends

The physical system in this example is a downscaled version of the
"graphene quantum billard" from Ref. `[1] <#references>`__.
An irregular shaped graphene dot, which is subjected to a time-dependent perturbation
(the two red sites of the system plot are perturbed by a Gaussian shaped pulse).
We calculate several snapshots of the electron density after the
perturbation has been applied. While the accuracy and parameters are arbitrary
and tuned to speed up the calculation, this example shows that graphene
can be studied in a similar way. 

.. jupyter-execute:: graphene.py

.. seealso::
    The complete source code of this example can be found in
    :download:`graphene.py <graphene.py>`.


References
----------

[1] T. Kloss, J. Weston, B. Gaury, B. Rossignol, C. Groth and X. Waintal,
`Tkwant: a software package for time-dependent quantum transport <https://doi.org/10.1088/1367-2630/abddf7>`_
New J. Phys. **23**, 023025 (2021),
`arXiv:2009.03132 [cond-mat.mes-hall]. <https://arxiv.org/abs/2009.03132>`_
