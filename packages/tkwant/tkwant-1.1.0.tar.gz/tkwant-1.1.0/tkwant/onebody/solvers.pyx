# -*- coding: utf-8 -*-
#
# Copyright 2016 - 2022 tkwant authors.
#
# This file is part of tkwant.  It is subject to the license terms in the file
# LICENSE.rst found in the top-level directory of this distribution and at
# https://tkwant.kwant-project.org/doc/stable/pre/license.html.
# A list of tkwant authors can be found in
# the file AUTHORS.rst at the top-level directory of this distribution and at
# https://tkwant.kwant-project.org/doc/stable/pre/authors.html.
"""Classes for solving the time-dependent Schrödinger equation."""

import numpy as np
import scipy.integrate


__all__ = ['Scipy']


cdef class Scipy:
    """Solve the time-dependent Schrödinger equation using `scipy.integrate`.

    This solver will currently only work with the 'dopri5' and 'dop853'
    integrators, as these are the only re-entrant ones.

    Parameters
    ----------
    size : int
        The size of the ``psi`` vector.
    integrator : `scipy.integrate._ode.IntegratorBase`, default: dopri5
        The integrator to use with this solver.
    **integrator_options
        Options to pass when instantiating the integrator.

    See Also
    --------
    scipy.integrate.ode
    """

    cdef:
        object _integrator
        object _rhs_out
        object rhs
        int size

    _default_options = {'atol': 1E-9, 'rtol': 1E-9, 'nsteps': int(1E9)}

    def __init__(self, size, integrator=scipy.integrate._ode.dopri5, **integrator_options):
        # allocate storage for kernel output
        self._rhs_out = np.empty((size,), dtype=complex)
        options = dict(self._default_options)
        options.update(integrator_options)
        self._integrator = integrator(**options)
        # Factor 2 because Scipy integrators expect real arrays
        self._integrator.reset(2 * size, has_jac=False)
        self.size = size

    def _rhs(self, t, y):
        # Kernel expects complex, Scipy expects real
        self.rhs(y.view(complex), self._rhs_out, t)
        return self._rhs_out.view(float)

    def __call__(self, psi, time, next_time, rhs):
        if time == next_time:
            return psi
        self.rhs = rhs
        # self._integrator.reset(2 * self.size, has_jac=False) ## RESET TO BE RE-ENTRANT
        # psi is complex, Scipy expects real
        next_psi, final_time = self._integrator.run(
            self._rhs, lambda: None, psi.view(float), time, next_time, (), ())
        if not self._integrator.success:
            raise RuntimeError('Integration failed between {} and {}'
                               .format(time, next_time))
        return next_psi.view(complex)

    @property
    def size(self):
        return self.size


default = Scipy
