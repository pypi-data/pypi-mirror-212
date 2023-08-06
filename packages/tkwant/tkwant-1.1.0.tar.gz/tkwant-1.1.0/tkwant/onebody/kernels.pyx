# -*- coding: utf-8 -*-
# cython: embedsignature=True
#
# Copyright 2016-2022 tkwant authors.
#
# This file is part of tkwant.  It is subject to the license terms in the file
# LICENSE.rst found in the top-level directory of this distribution and at
# https://tkwant.kwant-project.org/doc/stable/pre/license.html.
# A list of tkwant authors can be found in
# the file AUTHORS.rst at the top-level directory of this distribution and at
# https://tkwant.kwant-project.org/doc/stable/pre/authors.html.
"""Calculating the right-hand side of the time-dependent Schrödinger equation.

This module is mainly for internal use.

The classes in this module are used for calculating the following expression:

    ..math:: -i(H_0 ψ + W(t) ψ)

where :math:`H_0` is the time-independent part of the Hamiltonian,
:math:`W(t)` is the time-dependent part, and :math:`ψ` is some vector
defined over the Hilbert space of the problem. We recognise this expression
as the right-hand side of the time-dependent Schrödinger equation (TDSE),
where the left-hand side is :math:`∂ψ/∂t`.

In practice we will want to handle many different cases, including solving the
TDSE on infinite domains, or starting the evolution from an eigenstate.  All
the forms of TDSE that we will need to handle these cases are encompassed by
the above formula. This module is only concerned with calculating expressions
of the above form, not performing the mapping from the various problems. For
more details on the mapping, see `tkwant/onebody/solver.py`.
"""

__all__ = ['Kernel', 'Scipy', 'Simple',
           'default', 'PerturbationExtractor',
           'PerturbationInterpolator']

import numpy as np
import cython
from .. import _common, system, _logging
from scipy.sparse._sparsetools import coo_matvec, csr_matvec
import scipy.sparse as sp


# set module logger
logger = _logging.make_logger(name=__name__)

########## Abstract Base Classes for kernels

cdef class Kernel:
    """ABC for right-hand side of the time-dependent Schrödinger equation.

    Attributes
    ----------
    size : int
        The size of the time-independent part of the Hamiltonian. This
        also sets the size of the solution vector.
    """

    def __init__(self, H0, W, complex[:] psi_st=None, complex[:] work=None):
        raise NotImplementedError()

    def rhs(self, energy=None):
        """Evaluate the RHS of the TDSE and store the result in `dpsidt`."""
        raise NotImplementedError()


### C-level interface to Kernels (needed for C-implemented solvers)




########## Concrete kernel implementations

class Scipy(Kernel):
    """Evaluate the RHS of the Schrödinger equation using scipy sparse.

    Parameters
    ----------
    H0 : `scipy.sparse.base`
        Hamiltonian at ``t=0`` (including any boundary conditions).
    W : callable
        Time-dependent part of the Hamiltonian. Typically the object returned
        by `tkwant.system.extract_perturbation`.
    psi_st : array of complex, optional
        The wavefunction of the initial eigenstate defined over the central
        system (if starting in an initial eigenstate).
    work : `~numpy.ndarray` of complex, optional
        Workarray of size ``H0.shape[0]`` for performance and memory optimization.

    Attributes
    ----------
    H0 : `scipy.sparse.csr_matrix`
        Hamiltonian at ``t=0`` (including any boundary conditions).
    W : callable
        Time-dependent part of the Hamiltonian. Typically the object returned
        by `tkwant.system.extract_perturbation`.
    psi_st : array of complex or `None`
        The wavefunction of the initial eigenstate defined over the central
        system (if starting in an initial eigenstate).
    """

    def __init__(self, H0, W, psi_st=None, work=None):

        if not isinstance(H0, sp.csr.csr_matrix):
            self.H0 = H0.tocsr()  # self.H0 is no reference any more in that case
        else:
            self.H0 = H0

        self.W = W
        self.psi_st = psi_st
        # The size of the time-independent part of the Hamiltonian. This
        # also sets the size of the solution vector.
        self.size = self.H0.shape[0]

        if W is not None:
            self.center_size = self.W.size
        else:
            self.center_size = self.size

        if work is None:
            self._tmp = np.zeros((self.size,), dtype=complex)
        else:
            if work.size < self.center_size:
                raise ValueError('work array size={} must be at least '
                     'the size of the central system={}'
                     .format(work.size, self.center_size))
            self._tmp = work

    def rhs(self, energy=None):

        if energy is None:
            H0 = self.H0
        else:
            H0 = self.H0 - energy * sp.eye(self.size)

        # The approach with a separated class ``_CalcRHS`` to calculate the r.h.s.
        # seems more complicated, but it allows to store the static Hamiltonian
        # as a reference in class ``Scipy(Kernel)`` in ``self.H0``
        # (for manybody calculations there is onle reference per rank).
        # Moreover, the calculation ``H = H0 - E`` is done inplace,
        # and only once when the Scipy(Kernel).rhs() method is called.
        # It is important to precalculate H0 - E at this stage
        # (typically when ``WaveFunction.evolve()`` is called) and not
        # to do the inplace calculation in ``_CalcRHS.__call__()``,
        # as the later method is called very often (by the DGL solver).
        # The implace calculation generates only a temporary object ``H``
        # which not stored in the ``onebody.WaveFunction``, such
        # that it is cleaned by the garbage collector.
        return _CalcRHS(H0, self.W, self.psi_st, self.size, self.center_size, self._tmp)

    def set_W(self, W):
        '''Set the time dependent perturbation W(t)'''
        self.W = W


class _CalcRHS:
    """Calculate the right-hand-side of the time-dependent Schrödinger equation."""
    def __init__(self, H0, W, psi_st, size, center_size, tmp):

        self.H0 = H0
        self.W = W
        self.psi_st = psi_st
        self.size = size
        self.center_size = center_size
        self._tmp = tmp

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def __call__(self, const complex[:] psi, complex[:] dpsidt, const double time):

        # H0 @ psi -> tmp
        cdef complex[:] tmp = self._tmp
        tmp[:] = 0    
        csr_matvec(
            self.H0.shape[0], self.H0.shape[1], self.H0.indptr,
            self.H0.indices, self.H0.data, psi, tmp)

        # W(t) @ (psi + psi_st) + tmp -> tmp
        psi_centre = np.asarray(psi[:self.center_size])
        if self.psi_st is not None:
            psi_centre = psi_centre + self.psi_st
        try:
            self.W.apply(time, psi_centre[:self.center_size], out=tmp[:self.center_size])
        except Exception as exept:
            if self.W is None:
                pass
            else:
                raise exept

        # dpsidt = -1j * tmp
        cdef int i
        for i in range(self.size):
            dpsidt[i] = -1j * tmp[i]


@cython.boundscheck(False)
@cython.wraparound(False)
cdef(double, double, double, double, double) update_times(double t, double t0, double dt):
    '''Return new update times for the Hamiltonian matrix.
    '''
    assert dt > 0
    cdef int quotient
    quotient = int(round((t - t0) / dt, 10))  # integer division // has problems with the numerics
    t0 = t0 + quotient * dt
    # adding dt up we get inaccurate routings
    cdef double t1 = t0 + dt
    cdef double t2 = t0 + 2 * dt
    cdef double t3 = t0 + 3 * dt
    cdef double t4 = t0 + 4 * dt
    return t0, t1, t2, t3, t4


@cython.boundscheck(False)
@cython.wraparound(False)
cdef(double, double, double, double) _get_polynome_coeffs(double t, double t0, double t1, double dt):

    cdef double rdx = 1 / dt
    cdef double fac = dt * dt / 6.

    cdef double a = (t1 - t) * rdx
    cdef double b = (t - t0) * rdx
    cdef double c = (a * a * a - a) * fac
    cdef double d = (b * b * b - b) * fac
    return a, b, c, d


def _herm_conj(value):
    if hasattr(value, 'conjugate'):
        value = value.conjugate()
    if hasattr(value, 'transpose'):
        value = value.transpose()
    return value


_errormsg = ('{0} vector has length {1}, but the system '
             'contains {2} orbitals')


cdef class Interpolation:

    cdef:
        double dt
        double t0, t1, t2, t3, t4
        double atol, rtol
        double fac, facmin, facmax
        double dt_min
        object Ht0, Ht1, Ht2, Ht3, Ht4
        object d2Ht0, d2Ht1, d2Ht2
        object func
        unsigned nnz

    def __init__(self, func, t0, dt_init=0.001, atol=1E-10, rtol=1E-10, dt_min=1E-6, fac=0.9, facmin=0.1, facmax=3):

        # The spline interpolation in this routine is done "on the fly".
        # Quite generally, for a cubic spline, the cubic function f(t) is defined
        # on two neighboring intervals [t0, t1] and [t1, t2],
        # t1 - t0 = t2 - t1 = dt. One needs to know
        # f(t) on t0, t1, and t2, and f''(t) on the endpoints t0, t2.
        # As the Schrödinger equation which calls the interpolant propagates only
        # foreward in time, we do a stepwise interpolation and assume, at least
        # for the optimization, that the time argument monontonically increases
        # when the interpolation function is called. The idea is to reuse the
        # evaluated function and derivative values, and don't calculate them twice.
        # Therefore, one always need to keep 5. timesteps in memory, t0, t1 .. t4.
        # Interpolation is always done between t0, t1 and t2.
        # The points t3 and t4 are used to estimate the 2. derivative on t2
        # using a central finite difference scheme with 5 points. The second
        # derivative on point t0 is known from the step before.
        # Only when this routine is initialized, we have to estimate f''(t0).
        # We use a foreward derivative in this case.

        assert dt_init > 0
        assert dt_min > 0
        assert atol >= 0
        assert rtol >= 0

        self.dt = dt_init
        self.func = func

        self.atol = atol
        self.rtol = rtol

        self.fac = fac
        self.facmin = facmin
        self.facmax = facmax

        self.dt_min = dt_min

        self.t0 = t0
        self.t1 = self.t0 + self.dt
        self.t2 = self.t1 + self.dt
        self.t3 = self.t2 + self.dt
        self.t4 = self.t3 + self.dt

        self.Ht0 = self.func(self.t0)
        self.Ht1 = self.func(self.t1)
        self.Ht2 = self.func(self.t2)
        self.Ht3 = self.func(self.t3)
        self.Ht4 = self.func(self.t4)

        self.nnz = self.Ht0.shape[0]

        Ht02 = self.func(self.t0 + 0.5 * self.dt)
        Ht12 = self.func(self.t0 + 1.5 * self.dt)
        Ht22 = self.func(self.t0 + 2.5 * self.dt)

        rdt2 = 1 / (self.dt * self.dt)
        rdt2h = 4 * rdt2

        # w''(t0), forward finite difference scheme (4. order)
        # on the half interval dt / 2
        cl0 = 15 / 4 * rdt2h
        cl1 = -77 / 6 * rdt2h
        cl2 = 107 / 6 * rdt2h
        cl3 = -13 * rdt2h
        cl4 = 61 / 12 * rdt2h
        cl5 = -5 / 6 * rdt2h
        self.d2Ht0 = np.zeros((self.nnz,), dtype=complex)
        for i in range(self.nnz):
            self.d2Ht0[i] = cl0 * self.Ht0[i] + cl1 * Ht02[i] + cl2 * self.Ht1[i] \
                + cl3 * Ht12[i] + cl4 * self.Ht2[i] + cl5 * Ht22[i]

        # w''(t2), central finite difference scheme (4. order)
        cc2 = - rdt2 / 12
        cc1 = rdt2 * 4 / 3
        cc0 = - 2.5 * rdt2
        self.d2Ht2 = np.zeros((self.nnz,), dtype=complex)
        for i in range(self.nnz):
            self.d2Ht2[i] = cc2 * (self.Ht0[i] + self.Ht4[i]) \
                + cc1 * (self.Ht1[i] + self.Ht3[i]) \
                + cc0 * self.Ht2[i]

        # w''(t1), spline formula
        self.d2Ht1 = np.zeros((self.nnz,), dtype=complex)
        for i in range(self.nnz):
            self.d2Ht1[i] = 1.5 * rdt2 * (self.Ht0[i] + self.Ht2[i] - 2 * self.Ht1[i]) \
                - 0.25 * (self.d2Ht0[i] + self.d2Ht2[i])

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def eval(self, double time, complex[:] out):

        if self.nnz == 0: return

        cdef double c0, c1, c2, rdt2
        cdef double a, b, c, d
        cdef unsigned i

        # update matrices
        time_larger = time >= self.t2
        time_smaller = time < self.t0

        if time_larger or time_smaller:

            if time_larger:
                error = self._estimate_error(self.t1 + 0.5 * self.dt)
            else:
                error = self._estimate_error(self.t0 + 0.5 * self.dt)

            self.dt = self._estimate_stepsize(self.dt, error)

            t0_new, t1_new, t2_new, t3_new, t4_new = update_times(time, self.t0, self.dt)
            rdt2 = 1 / (self.dt * self.dt)
            cc2 = - rdt2 / 12
            cc1 = rdt2 * 4 / 3
            cc0 = - 2.5 * rdt2

            Htm2 = self.func(t0_new - 2 * self.dt)
            Htm1 = self.func(t0_new - self.dt)
            self.func(t0_new, self.Ht0)
            self.func(t1_new, self.Ht1)
            self.func(t2_new, self.Ht2)
            self.func(t3_new, self.Ht3)
            self.func(t4_new, self.Ht4)

            for i in range(self.nnz):
                # w''(t) on t0 and t2, central finite difference scheme
                self.d2Ht0[i] = cc2 * (Htm2[i] + self.Ht2[i]) \
                    + cc1 * (Htm1[i] + self.Ht1[i]) \
                    + cc0 * self.Ht0[i]
                self.d2Ht2[i] = cc2 * (self.Ht0[i] + self.Ht4[i]) \
                    + cc1 * (self.Ht1[i] + self.Ht3[i]) \
                    + cc0 * self.Ht2[i]
                # w''(t) on t1, spline formula
                self.d2Ht1[i] = 1.5 * rdt2 * (self.Ht0[i] + self.Ht2[i] - 2 * self.Ht1[i])\
                    - 0.25 * (self.d2Ht0[i] + self.d2Ht2[i])

            self.t0, self.t1, self.t2, self.t3, self.t4 = t0_new, t1_new, t2_new, t3_new, t4_new

        # construct the spline, either on [t0, t1] or on [t1, t2] interval.
        if time < self.t1:
            a, b, c, d = _get_polynome_coeffs(time, self.t0, self.t1, self.dt)
            for i in range(self.nnz):
                out[i] = a * self.Ht0[i] + b * self.Ht1[i] + c * self.d2Ht0[i] + d * self.d2Ht1[i]
        else:
            a, b, c, d = _get_polynome_coeffs(time, self.t1, self.t2, self.dt)
            for i in range(self.nnz):
                out[i] = a * self.Ht1[i] + b * self.Ht2[i] + c * self.d2Ht1[i] + d * self.d2Ht2[i]

    def _estimate_error(self, double time):
        fx = self.func(time)
        fapp = np.zeros((self.nnz,), dtype=complex)
        self.eval(time, fapp)
        scale = self.atol + self.rtol * np.abs(fx)
        return np.max(np.abs(fx - fapp) / scale)

    def _estimate_stepsize(self, double dt, double error):
        # Eq. (4.13), page 168 in book:
        # E. Hairer, S. Nørsett, and G. Wanner, Solving Ordinary Differential Equations,
        # I: Nonstiff Problems, Second  revised edition (Springer, Berlin, Heidelberg, 2008).
        assert dt > 0
        assert error >= 0
        a = - 1 / 4  # cubic order p = 3
        dt_new = dt * min(self.facmax, max(self.facmin, self.fac * error**a))
        if dt_new < self.dt_min:
            logger.warning('minimal W(t) stepsize dt_min={} reached.'
                           .format(self.dt_min))
            dt_new = self.dt_min
        return dt_new



# TODO: this only works for finalized builders so far -- how to extend
#       this to something more general?
# TODO: change this routine when kwant supports vectorized systems
cdef class PerturbationExtractor:
    """Extract the time-dependent perturbation to the Hamiltonian.

    The total Hamiltonian can be split into two parts: the stationary
    part and the time-dependent perturbation, i.e.  H(t) = H_0 + W(t).
    This routine extracts the W(t) part from the Kwant system that
    specifies the H(t).

    Parameters
    ----------
    syst : `kwant.builder.FiniteSystem`
        The system from which to extract the time-dependent perturbation.
    time_name : str
        The name of the time argument. Only sites with Hamiltonian value
        functions with the argument name `time_name` are extracted into W(t).
    time_start : float
        The initial time.
    params : dict, optional
        Extra arguments to pass to the Hamiltonian of ``syst``, excluding time.

    Notes
    -----
    By definition the perturbation is defined with respect to the initial time.
    The perturbation should be therefore zero for times t < `time_start`. This
    is not inforced by this routine however, but W(t) is always evaluated
    with the time argument it gets.
    """
    cdef:
        object H
        object tparams
        int size
        int nnz
        object time_name
        object td_hamiltonian

    def __init__(self, syst, time_name, time_start, params=None):
        self.tparams = system.add_time_to_params(params, time_name, time_start)
        self.time_name = time_name
        self.H = H = syst.hamiltonian

        # Number of (potentially) non-zero entries in the time-dependent
        # Hamiltonian matrix.
        nnz = 0

        # Process onsites.
        self.td_hamiltonian = td_hamiltonian = []
        for i, (onsite, _) in enumerate(syst.onsites):
            if system.is_time_dependent_function(onsite, time_name):
                a, b = rng = system.orb_range(syst, i)
                norbs = b - a
                nnz += norbs * norbs
                td_hamiltonian.append(
                    ((i, i, rng, rng, H(i, i, params=self.tparams))))

        # Process hoppings.
        for edge_id, (i, j) in enumerate(syst.graph):
            hop_val, _ = syst.hoppings[edge_id]
            if system.is_time_dependent_function(hop_val, time_name):
                a, b = ori = system.orb_range(syst, i)
                c, d = orj = system.orb_range(syst, j)
                nnz += 2 * (b - a) * (d - c)
                td_hamiltonian.append((i, j, ori, orj, H(i, j, params=self.tparams)))

        _, _, total_norbs = syst.site_ranges[-1]
        self.nnz = nnz
        self.size = total_norbs

    @property
    def size(self):
        '''The size of the W(t) matrix.

        Returns
        -------
        size : int
            The size of the W(t) matrix is ``size`` x ``size``.
        '''
        return self.size

    @property
    def nnz(self):
        '''The total number of time-dependent matrix elements.

        Returns
        -------
        nnz : int
            The total number of time-dependent matrix elements, equal to
            len(W(t).data).
        '''
        return self.nnz

    def data(self, double time, object out=None):
        '''Return the time-dependent matrix elements.

        Parameters
        ----------
        time : int or float
            Time argument, must be equal or larger than `time_start`.
        out : `numpy.ndarray`, optional
            Data array of the W(t) matrix for operation in-place.

        Returns
        -------
        out : `numpy.ndarray` or `None`
            Data array of the W(t) matrix (W(t).data). If an ``out`` argument is given,
            the operation is performed in-place and the routine returns `None`.
        '''
        if out is None:
            do_return = True
            out = np.empty(self.nnz, complex)
        else:
            do_return = False
            assert out.shape[0] == self.nnz, _errormsg.format('output',
                                                              out.shape[0],
                                                              self.nnz)
        index = 0
        self.tparams[self.time_name] = time
        for i, j, _, _, H_0 in self.td_hamiltonian:
            H = self.H(i, j, params=self.tparams)
            mat_els = np.asarray(H - H_0).flatten()
            for val in mat_els:
                out[index] = val
                index += 1
            if i != j:
                mat_els = mat_els.conjugate()
                for val in mat_els:
                    out[index] = val
                    index += 1
        return out if do_return else None

    def row_col(self):
        '''Return the row and column vectors of the W(t) matrix.

        Returns
        -------
        row : `np.ndarray`
            Row vector of the W(t) matrix in coo format.
        col : `np.ndarray`
            Column vector of the W(t) matrix in coo format.
        '''
        row = np.empty(self.nnz, np.int32)
        col = np.empty(self.nnz, np.int32)
        index = 0
        for i, j, to, frm, H_0 in self.td_hamiltonian:
            to = range(*to)
            frm = range(*frm)
            for k in to:
                for l in frm:
                    row[index] = k
                    col[index] = l
                    index += 1
            if i != j:
                for k in to:
                    for l in frm:
                        row[index] = l
                        col[index] = k
                        index += 1
        return row, col

    def empty(self):
        '''Return an empty W(t) matrix with correct shape and indices.

        Returns
        -------
        out : `~scipy.sparse.coo_matrix`
            An "empty" W(t) matrix filled with zeros.
        '''
        data = np.zeros((self.nnz,), dtype=complex)
        row_col = self.row_col()
        return sp.coo_matrix((data, row_col), (self.size, self.size))

    def evaluate(self, double time, object out=None):
        '''Evaluate the W(t) matrix for the given time t.

        Parameters
        ----------
        time : int or float
            Time argument, must be equal or larger than `time_start`.
        out : `~scipy.sparse.coo_matrix`, optional
            Sparse matrix with to perform the operation in-place.

        Returns
        -------
        out : `~scipy.sparse.coo_matrix` or `None`
            The matrix W(t).
            The size of the W(t) matrix is ``size`` x ``size``, containing
            ``nnz`` complex entries. If an ``out`` argument is given,
            the operation is performed in-place and the routine returns `None`.
        '''
        if out is None:
            data = self.data(time)
            row_col = self.row_col()
            return sp.coo_matrix((data, row_col), (self.size, self.size))
        else:
            assert out.shape[0] == self.size, _errormsg.format('output',
                                                                out.shape[0],
                                                                self.size)
            self.data(time, out.data)

    def apply(self, double time, ket, out=None):
        '''Evaluate the matrix-vector product W(t) @ ket for the given time.

        Parameters
        ----------
        time : int or float
            Time argument, must be equal or larger than `time_start`.
        out : `numpy.ndarray`, optional
            Sparse matrix with to perform the operation in-place.
            If provided, array must be zero on input.

        Returns
        -------
        out : `numpy.ndarray` or `None`
            The product W(t) @ ket. If an ``out`` argument is given,
            the operation is performed in-place and the routine returns `None`.
        '''
        assert ket.shape[0] == self.size, _errormsg.format('Ket', ket.shape[0],
                                                           self.size)
        if out is None:
            do_return = True
            out = np.zeros((self.size,), dtype=complex)
        else:
            do_return = False
            assert out.shape[0] == self.size, _errormsg.format('output',
                                                               out.shape[0],
                                                               self.size)
        self.tparams[self.time_name] = time
        for i, j, to, frm, H_0 in self.td_hamiltonian:
            to = slice(*to)
            frm = slice(*frm)
            mat_el = self.H(i, j, params=self.tparams) - H_0
            out[to] += np.dot(mat_el, ket[frm])
            if i != j:
                out[frm] += np.dot(_herm_conj(mat_el), ket[to])
        return out if do_return else None


cdef class PerturbationInterpolator:
    r"""A class to extract and interpolate W(t).

    This class can be used like `tkwant.onebody.kernel.PerturbationExtractor`,
    to calculate W(t) and the matrix-vector product W(t) * ket.
    Interpolation is done only for performance reasons, as W(t) from
    Kwant is slow to evaluate.

    Parameters
    ----------
    syst : `kwant.builder.FiniteSystem`
        The system from which to extract the time-dependent perturbation.
    time_name : str
        The name of the time argument. Only sites with Hamiltonian value
        functions with the argument name `time_name` are extracted into W(t).
    time_start : float
        The initial time.
    params : dict, optional
        Extra arguments to pass to the Hamiltonian of ``syst``, excluding time.
    interpolation_type : optional
        The interpolator class

    Notes
    -----
    By definition the perturbation is defined with respect to the initial time.
    The perturbation should be therefore zero for times t < `time_start`. This
    is not inforced by this routine however, but W(t) is always evaluated
    with the time argument it gets.
    """

    cdef:
        double dt
        unsigned size
        unsigned nnz
        object wt
        object wfunc
        object intfunc

    def __init__(self, syst, time_name, time_start, params=None, interpolation_type=Interpolation):

        self.wfunc = PerturbationExtractor(syst, time_name, time_start, params)

        # for non-vectorized systems
        _, _, norbs = syst.site_ranges[-1]
        self.size = norbs
        self.nnz = self.wfunc.nnz

        self.intfunc = interpolation_type(self.wfunc.data, time_start)
        self.wt = self.wfunc.empty()

    @property
    def size(self):
        '''The size of the W(t) matrix.

        Returns
        -------
        size : int
            The size of the W(t) matrix is ``size`` x ``size``.
        '''
        return self.size

    @property
    def nnz(self):
        '''The total number of time-dependent matrix elements.

        Returns
        -------
        nnz : int
            The total number of time-dependent matrix elements, equal to
            len(W(t).data).
        '''
        return self.nnz

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def evaluate(self, double time, object out=None):
        '''Evaluate the W(t) matrix for the given time t.

        Parameters
        ----------
        time : int or float
            Time argument, must be equal or larger than `time_start`.
        out : `~scipy.sparse.coo_matrix`, optional
            Sparse matrix with to perform the operation in-place.

        Returns
        -------
        out : `~scipy.sparse.coo_matrix` or `None`
            The matrix W(t).
            The size of the W(t) matrix is ``size`` x ``size``, containing
            ``nnz`` complex entries. If an ``out`` argument is given,
            the operation is performed in-place and the routine returns `None`.
        '''

        if out is None:
            self.intfunc.eval(time, self.wt.data)
            return self.wt
        else:
            assert out.shape[0] == self.size, _errormsg.format('output',
                                                               out.shape[0],
                                                               self.size)
            assert out.data.shape[0] == self.nnz, _errormsg.format('output.dat',
                                                                   out.data.shape[0],
                                                                   self.nnz)
            self.intfunc.eval(time, out.data)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def apply(self, double time, const complex[:] ket, object out=None):
        '''Evaluate the matrix-vector product W(t) @ ket for the given time.

        Parameters
        ----------
        time : int or float
            Time argument, must be equal or larger than `time_start`.
        out : `numpy.ndarray`, optional
            Sparse matrix with to perform the operation in-place.

        Returns
        -------
        out : `numpy.ndarray` or `None`
            The product W(t) @ ket. If an ``out`` argument is given,
            the operation is performed in-place and the routine returns `None`.
        '''

        assert ket.shape[0] == self.size, _errormsg.format('Ket',
                                                           ket.shape[0],
                                                           self.size)
        if out is None:
            do_return = True
            out = np.zeros((self.size,), dtype=complex)
        else:
            assert out.shape[0] == self.size, _errormsg.format('output',
                                                               out.shape[0],
                                                               self.size)

        self.evaluate(time, self.wt)

        coo_matvec(
            self.wt.nnz, self.wt.row, self.wt.col, self.wt.data,
            ket, out)

        return out if do_return else None


# Example Kernel implementation in C

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
cdef _csr_spmv_ptr(const int size, const int *indptr, const int *indices,
                   const complex *data,  const complex *X, complex *Y):
    """Naive implementation of CSR-format matrix-vector multiplication.

    This is taken almost verbatim from scipy.sparse.
    """
    cdef complex sum
    cdef unsigned i, jj

    for i in range(size):
       sum = Y[i]
       for jj in range(indptr[i], indptr[i+1]):
           sum += data[jj] * X[indices[jj]]
       Y[i] = sum


cdef class Simple(Kernel):
    """A C-implemented kernel using naive CSR matvec."""

    cdef:
        object H0
        object W
#        PerturbationExtractor W
        int center_size
        complex[:] psi_st
        object _temp

    def __init__(self, H0, W, complex[:] psi_st=None, work=None):
        pass

    def __cinit__(self, H0, W, complex[:] psi_st=None, work=None):

        if not isinstance(H0, sp.csr.csr_matrix):
            self.H0 = H0.tocsr()  # self.H0 is no reference any more in that case
        else:
            self.H0 = H0

        self.W = W
        self.size = H0.shape[0]

        if W is not None:
            self.center_size = self.W.size
        else:
            self.center_size = self.size
        self.psi_st = psi_st
        if work is None:
            self._temp = np.empty((self.center_size,), dtype=complex)
        else:
            if work.size < self.center_size:
                raise ValueError('work array size={} must be at least '
                     'the size of the central system={}'
                     .format(work.size, self.center_size))
            self._temp = work


    def rhs(self, energy=None):

        if energy is None:
            H0 = self.H0
        else:
            H0 = self.H0 - energy * sp.eye(self.size)

        # The approach with a separated class ``_CalcRHS`` to calculate the r.h.s.
        # seems more complicated, but it allows to store the static Hamiltonian
        # as a reference in class ``Scipy(Kernel)`` in ``self.H0``
        # (for manybody calculations there is onle reference per rank).
        # Moreover, the calculation ``H = H0 - E`` is done inplace,
        # and only once when the Scipy(Kernel).rhs() method is called.
        # It is important to precalculate H0 - E at this stage
        # (typically when ``WaveFunction.evolve()`` is called) and not
        # to do the inplace calculation in ``_CalcRHS.__call__()``,
        # as the later method is called very often (by the DGL solver).
        # The implace calculation generates only a temporary object ``H``
        # which not stored in the ``onebody.WaveFunction``, such
        # that it is cleaned by the garbage collector.
        return _CalcRHSc(H0.indptr, H0.indices, H0.data, self.W, self.psi_st, 
                         self.size, self.center_size, self._temp)

    @property
    def W(self):
        '''The time dependent perturbation W(t)'''
        return self.W

    def set_W(self, W):
        '''Set the time dependent perturbation W(t)'''
        self.W = W


cdef class _CalcRHSc:

    cdef:
        object W
        #PerturbationExtractor W
        int center_size, size
        complex *psi_st
        complex *temp
        complex[:] _data
        int[:] _indices, _indptr

    def __init__(self, int[:] indptr, int[:] indices, complex[:] data, W, complex[:] psi_st, 
                 int size, int center_size, complex[:] temp):
        pass

    """Calculate the right-hand-side of the time-dependent Schrödinger equation."""
    def __cinit__(self, int[:] indptr, int[:] indices, complex[:] data, W, complex[:] psi_st, 
                  int size, int center_size, complex[:] temp):

        self._data = data
        self._indices = indices
        self._indptr = indptr
        self.W = W
        if psi_st is None:
            self.psi_st = NULL
        else:
            self.psi_st = &psi_st[0]
        self.size = size
        self.center_size = center_size

        # the id of the temp array is not the same any more due to argument complex[:] temp
        #print('simple kernel work', id(temp))
        #exit(0)

        self.temp = &temp[0]


    # RHS implemented as a static method to conform to the solver interface.
    @cython.boundscheck(False)
    @cython.wraparound(False)
    def __call__(self, const complex[::1] psi, complex[::1] dpsidt, double time):

        cdef int *indptr
        cdef int *indices
        cdef complex *data

        data = &self._data[0]
        indices = &self._indices[0]
        indptr = &self._indptr[0]

        cdef unsigned i
        for i in range(self.size):
            dpsidt[i] = 0

        ### H0 @ psi -> dpsidt
        _csr_spmv_ptr(self.size, indptr, indices, data, &psi[0], &dpsidt[0])


        ### W(t) @ psi + dpsidt -> dpsidt
        if self.psi_st == NULL:
            try:
                self.W.apply(time, <complex[:self.center_size]>&psi[0],
                             out=<complex[:self.center_size]>&dpsidt[0])
            except Exception as exept:
                if self.W is None:
                    pass
                else:
                    raise exept
        else:
            # we need to act on `temp = psi + psi_st`
            # use pre-allocated storage
            for i in range(self.center_size):
                self.temp[i] = psi[i] + self.psi_st[i]
            try:
                self.W.apply(time, <complex[:self.center_size]>self.temp,
                             out=<complex[:self.center_size]>&dpsidt[0])
            except Exception as exept:
                if self.W is None:
                    pass
                else:
                    raise exept
        ### dpsidt = -1j * dpsidt
        for i in range(self.size):
            dpsidt[i] = -1j * dpsidt[i]

    def __reduce__(self):
        raise NotImplementedError("use the scipy kernel for serialization")

default = Simple
