# -*- coding: utf-8 -*-
# Copyright 2020 - 2023 tkwant authors.
#
# This file is part of tkwant.  It is subject to the license terms in the file
# LICENSE.rst found in the top-level directory of this distribution and at
# https://tkwant.kwant-project.org/doc/stable/pre/license.html.
# A list of tkwant authors can be found in
# the file AUTHORS.rst at the top-level directory of this distribution and at
# https://tkwant.kwant-project.org/doc/stable/pre/authors.html.
"""Tools for calculating interacting systems."""

import numpy as np
import scipy

import kwant

from . import onebody, mpi, _logging, _common

_all__ = ['AdaptiveStepsize', 'Extrapolate', 'SelfConsistentState']


# set module logger
logger = _logging.make_logger(name=__name__)
log_func = _logging.log_func(logger)


@log_func
class AdaptiveStepsize:
    def __init__(self, atol, rtol, tau_min=1E-6, fac=0.9, facmin=0.1, facmax=3, p=1):
        """A class to estimate the stepsize tau."""

        assert atol >= 0
        assert rtol >= 0
        assert tau_min > 0

        self.atol = atol
        self.rtol = rtol
        self.tau_min = tau_min
        self.fac = fac
        self.facmin = facmin
        self.facmax = facmax
        self.a = - 1 / (1 + p)  # order p

    def __call__(self, y, dyt, tau):
        # Eq. (4.13), page 168 in book:
        # E. Hairer, S. Nørsett, and G. Wanner, Solving Ordinary Differential Equations,
        # I: Nonstiff Problems, Second  revised edition (Springer, Berlin, Heidelberg, 2008).
        assert tau > 0
        error = self._estimate_error(y, dyt)

        if error > 0:
            new_tau = tau * min(self.facmax, max(self.facmin, self.fac * error**self.a))
        else:  # error is zero
            new_tau = tau * min(self.facmax, self.facmin)

        if new_tau < self.tau_min:
            logger.warning('minimal self-consistent stepsize tau_min={} reached.'
                           .format(self.tau_min))
            new_tau = self.tau_min
        return new_tau

    def _estimate_error(self, y, dyt):
        scale = self.atol + self.rtol * np.abs(y)
        return np.max(np.abs(dyt) / scale)


@log_func
class Extrapolate:
    r"""Extrapolate a function y = f(x) in positive x direction.

       To construct an approximation g(x), the function f(x) must be sampled
       on different points (x0 < x1 < x2, < ...). Sampling points are not required
       to be equidistant. For an accurate approximation g(x) \approx f(x),
       the function f(x) must be smooth and vary little between sampling points.
       In addition, the distance between the evaluation point x and
       the last sampling point x_n must fulfill dx = x - x_n << 1.
       Extrapolation is based on polynominal approximation g(x).

       g(x) = \sum_{n=0}^m a_n x

    """
    def __init__(self, y0, tau, order=1, x0=0, dy0=0, tol=1E-14):
        """Initialize an extrapolation function g(x)"""

        y0 = np.asarray(y0)
        dy = np.asarray(dy0)

        if not _common.is_type(x0, 'real_number'):
            raise TypeError('argument x0 must be a real scalar value')
        if not _common.is_type(tau, 'real_number') or tau <= 0:
            raise ValueError('update timestep must be real and larger zero, found tau={}'.format(tau))
        if not _common.is_type_array(y0, 'number').all():
            raise TypeError('y0 must be a scalar or vector of numbers')
        if not _common.is_type_array(dy, 'number').all():
            raise TypeError('dy must be a scalar or vector of numbers')
        if not _common.is_type(tol, 'real_number') or tol < 0:
            raise ValueError('tol must real and positive, found tol={}'.format(tol))

        self.x0 = x0
        self.x1 = x0 + tau
        self.order = order

        self._y0 = y0
        self._yt0 = y0
        self._dy = dy
        self._tol = tol

    def _g_func(self, x):
        if not _common.is_type_array(x, 'real_number').all():
            raise TypeError('argument must be a scalar or vector of real numbers')
        if not ((x >= self.x0 - self._tol) & (x <= self.x1 + self._tol)):
            raise ValueError('argument x={} is not inside interval=[{}, {}]'
                             .format(x, self.x0, self.x1))
        if self.order == 0:
            return self._y0
        elif self.order == 1:
            return self._yt0 + (x - self.x0) * self._dy
        else:
            raise NotImplementedError("extrapolation order={} is not "
                                      "implemented".format(self.order))

    def __call__(self, x):
        """Return the extrapolation function g(x)"""
        x = np.asarray(x)
        if x.size == 1:
            return self._g_func(x)
        return np.array([self._g_func(xx) for xx in x])

    def add_point(self, x, y):
        """Add a new point on the rhs"""
        y = np.asarray(y)
        if not _common.is_type(x, 'real_number'):
            raise TypeError('argument x must be a real scalar value')
        if not _common.is_type_array(y, 'number').all():
            raise TypeError('y must be a scalar or vector of numbers')
        if not _common.is_zero(x - self.x1, self._tol):
            raise ValueError('update time must be at x={}, found x={}'.format(self.x1, x))

        yt = self.__call__(x)

        dx = x - self.x0
        dy = y - self._y0
        dyt = y - yt

        # update the stored evaluation points
        self.x0 = x
        self._y0 = y
        self._yt0 = yt
        self._dx = dx
        self._dy = dy
        self._dyt = dyt

        return dyt

    def set_stepsize(self, tau):

        if not _common.is_type(tau, 'real_number') or tau <= 0:
            raise ValueError('update timestep must be real and larger zero, found tau={}'.format(tau))

        if self.order == 1:
            self._dy = self._dy / self._dx + self._dyt / tau

        # update the stored evaluation points
        self.x1 = self.x0 + tau
        return


@log_func
class SelfConsistentState:
    """Solve self-consistently the interacting and time-dependent many-particle
       Schrödinger equation"

       An instance of the class behaves like a manybody wavefunction.
       The class is independent from the physical decoupling of the interaction
       and manages only the self-consistent update of the memory kernel.
       """
    def __init__(self, wave_function, mf_operator, mf_potential,
                 atol=1E-6, rtol=1E-6, tau=AdaptiveStepsize,
                 extrapolator_type=Extrapolate):
        r"""
        Parameters
        ----------
        wave_function : `tkwant.manybody.WaveFunction`
            The manybody wavefunction of the non-interacting system.
        mf_operator : callable
            An operator to evaluate the expectation values needed for to
            calculate the mean-field potential.
            Must have the calling signature of `kwant.operator`
            and return a numpy array.
        mf_potential : object
            An object to calculate the mean-field potential
            Must have a ``prepare()`` and an ``evaluate()`` method.
        atol : float, optional
            Absolute tolerance for the ``mf_operator`` function extrapolation.
        rtol : float, optional
            Relative tolerance for the `mf_operator`` function extrapolation.
        tau : float or ``tkwant.interaction.AdaptiveStepsize``, optional
            For adaptive stepsize control, tau is a function to estimate the
            extrapolation stepsize. If ``tau`` is set to
            a number, the value is used as a constant stepsize.
        extrapolator_type : ``tkwant.interaction.Extrapolate``, optional
            A class to extrapolate the self-consistent potential
        """
        self.wavefunction = wave_function
        self._mf_operator = mf_operator
        self._mf_potential = mf_potential
        self.steps = 0

        self.time = wave_function.time  # time of the manybody state

        # tau is the stepsize from last self-consistent update (at time_sc - tau)
        # time_sc is the time of the next self-consistent update,
        # we set it initially to the minimal tau from the stepsize estimator
        if _common.is_type(tau, 'real_number'):  # fixed stepsize tau
            if tau <= 0:
                raise ValueError("stepsize tau must be > 0")
            self._tau = tau

            def const_tau(*args, **kwargs):
                return tau
            self._estimate_tau = const_tau
        else:  # adaptive stepsize tau
            self._estimate_tau = tau(rtol, atol)
            self._tau = self._estimate_tau.tau_min
        self._time_sc = self.time + self._tau

        # evaluate the operator and construct an extrapolation function f(t)
        # calculate the actual mean field potential Q(t) from f(t)
        # add Q(t) to the tkwant hamiltonian
        try:
            y = self.wavefunction.evaluate(self._mf_operator, root=None)
        except TypeError:  # if root argument not present
            y = self.wavefunction.evaluate(self._mf_operator)
        self._yt = extrapolator_type(y, self._tau, x0=self.time)
        self._mf_potential.prepare(self._yt, self._time_sc)
        self.wavefunction.add_perturbation(self._mf_potential.evaluate)

    def evolve(self, time):
        """
        Evolve all the self-consistent manybody state up to ``time``.

        Parameters
        ----------
        time : int or float
            time argument up to which the state should be evolved

        Notes
        -----
        The self-consistent updates are completely independent from the
        requested timesteps ``time``.
        The reported error max|y - yt| is between the operator value y and
        its extrapolation yt, estimated at tmax of the extrapolation interval.
        """
        # perform self-consistent updates in foreward-time direction
        # until the next self-consistent update time ``time_sc`` lies
        # ahead of the actual requested time ``time`` for the manybody state
        while self._time_sc <= time:

            self.wavefunction.evolve(self._time_sc)

            # calculate the exact mean-field potential at ``time_sc``,
            # and estimate the error of the extrapolation function
            try:
                y = self.wavefunction.evaluate(self._mf_operator, root=None)
            except TypeError:  # if root argument not present
                y = self.wavefunction.evaluate(self._mf_operator)
            dyt = self._yt.add_point(self._time_sc, y)

            # estimate the stepsize tau and the time for the next self-consistent update
            dt = self._estimate_tau(y, dyt, self._tau)
            logger.debug('tmin, tmax= [{}, {}], new tau= {}, max|y - yt|= {}'
                         .format(self._time_sc - self._tau, self._time_sc, dt, np.max(np.abs(dyt))))
            self._tau = dt
            time_next = self._time_sc + self._tau

            # update the self-consistent mean-field extrapolation
            # and update the mean-field potential in the manybody wave-function
            # by providing the new extrapolation function
            self._yt.set_stepsize(self._tau)
            self._mf_potential.prepare(self._yt, time_next)
            self.wavefunction.add_perturbation(self._mf_potential.evaluate)
            self._time_sc = time_next

            self.steps += 1

        self.wavefunction.evolve(time)
        self.time = time

    def evaluate(self, operator, root=0):
        """Evaluate the expectation value of an operator at the current time.

        Arguments and return values similar to `tkwant.manybody.WaveFunction`
        """
        try:
            return self.wavefunction.evaluate(operator, root)
        except TypeError:  # onebody wavefunction has no root argument
            return self.wavefunction.evaluate(operator)
