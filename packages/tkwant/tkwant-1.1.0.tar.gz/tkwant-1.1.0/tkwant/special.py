# -*- coding: utf-8 -*-
# Copyright 2022 tkwant authors.
#
# This file is part of tkwant.  It is subject to the license terms in the file
# LICENSE.rst found in the top-level directory of this distribution and at
# https://tkwant.kwant-project.org/doc/stable/pre/license.html.
# A list of tkwant authors can be found in
# the file AUTHORS.rst at the top-level directory of this distribution and at
# https://tkwant.kwant-project.org/doc/stable/pre/authors.html.

"""Analytical implementations for special purpose."""

import numpy as np
import scipy.special
import cmath

from . import _logging


__all__ = ['g_ee_retarded', 'GreenFlatBand', 'GreenFlatBandEq']


# set module logger
logger = _logging.make_logger(name=__name__)
log_func = _logging.log_func(logger)


# --- Green functions on a one-dimensional quantum dot array in flatband approximation

def _iless(a, t):
    # I^<_t(a) =  - \int_{-\infty}^{0} d \omega \frac{e^{- i \omega t}}{\omega - a}
    assert (t != 0) and (a.imag != 0)
    z = - 1j * a * t
    if a.real == 0:
        return cmath.exp(z) * (- scipy.special.expi(-z) + 1j * np.pi * np.sign(t) * np.heaviside(-(a * t).imag, 0))
    phase = 2 * 1j * np.pi * np.sign(t) * np.heaviside(-(a * t).imag, 0) * np.heaviside(-a.real, 0)
    return cmath.exp(z) * (scipy.special.exp1(z) + phase)


def _igreat(a, t):
    # I^>_t(a) =  \int_{0}^{\infty} d \omega \frac{e^{- i \omega t}}{\omega - a}
    assert (t != 0) and (a.imag != 0)
    z = - 1j * a * t
    if a.real == 0:
        return cmath.exp(z) * (- scipy.special.expi(-z) - 1j * np.pi * np.sign(t) * np.heaviside(-(a * t).imag, 0))
    phase = 2 * 1j * np.pi * np.sign(t) * np.heaviside(-(a * t).imag, 0) * np.heaviside(a.real, 0)
    return cmath.exp(z) * (scipy.special.exp1(z) - phase)


def _iges(a, t):
    # I(a, t) = \int_{-\infty}^{\infty} d \omega \frac{e^{- i \omega t}}{\omega - a}
    assert (t != 0) and (a.imag != 0)
    phase = - 1j * np.pi * np.sign(t) * cmath.exp(- 1j * a * t) * np.heaviside(-(a * t).imag, 0)
    if a.real == 0:
        return phase
    return 2 * phase


def _q(l1, l2, mu, t):
    # Q(l_1, l_2, \mu, t) = \int_{-\infty}^{\infty} \frac{d \omega}{2 \pi} \, e^{- i \omega t} \frac{1 - 2 \theta(\omega - \mu)}{(\omega - l_1)(\omega - l_2)}
    assert l1 != l2
    if t == 0:
        return (1j * (np.heaviside(l1.imag, 0) - np.heaviside(l2.imag, 0)) - (cmath.log(l1 - mu) - cmath.log(l2 - mu)) / np.pi) / (l1 - l2)
    return (_iges(l1, t) - _iges(l2, t) + 2 * cmath.exp(- 1j * mu * t) * (_iless(l1 - mu, t) - _iless(l2 - mu, t))) / (2 * np.pi * (l1 - l2))


def g_ee_retarded(omega):
    r'''Retarded Green function of the 1d semi-infinite lead with H = - \sum_i c^\dagger_i+1 c_i + h.c.'''
    return 0.5 * omega - 1j * np.sqrt(1 - 0.25 * omega**2)


class GreenFlatBand:
    '''Nonequilibrium Green functions of a 1 dim quantum dot array in flatband approximation at temp T=0'''

    def __init__(self, h_ss, h_se, gr_e, mu_e):
        '''
        Parameters
        ----------
            h_ss : central system Hamiltonian matrix
            h_se : system-environment Hamiltonian matrix
            gr_e : sequence of lead retarded Green functions
            mu_e : sequence of lead chemical potentials
        '''

        h_ss = np.array(h_ss)
        self.h_se = np.array(h_se)
        gr_e = np.array(gr_e)
        self.mu_e = np.array(mu_e)

        assert((h_ss.shape[0] == h_ss.shape[1]) and (h_ss.shape[0] == self.h_se.shape[0]))
        assert((h_se.shape[1] == gr_e.shape[0]) and (self.h_se.shape[1] == self.mu_e.shape[0]))

        self.h_es = np.conj(self.h_se.T)
        self.gs_e = gr_e - np.conj(gr_e)

        mat = h_ss + self.h_se @ np.diag(gr_e) @ self.h_es

        self.D, self.U = np.linalg.eig(mat)
        self.Ui = np.linalg.inv(self.U)
        self.Dc = np.conj(self.D)
        self.Uc = np.conj(self.U)
        self.Uci = np.conj(self.Ui)

    def retarded(self, i, j, t):
        if t == 0:
            if i == j:
                return -1j
            else:
                return 0
        Df = np.array([_iges(x, t) for x in self.D])
        return self.U[i, :] @ np.diag(Df) @ self.Ui[:, j] / (2 * np.pi)

    def advanced(self, i, j, t):
        if t == 0:
            return 0
        Dcf = np.array([_iges(x, t) for x in self.Dc])
        return self.Uc[i, :] @ np.diag(Dcf) @ self.Uci[:, j] / (2 * np.pi)

    def keldysh(self, i, j, t):

        res = 0
        dim_s, dim_e = self.h_se.shape
        for l in range(dim_s):
            for m in range(dim_s):
                for n in range(dim_e):
                    for mp in range(dim_s):
                        for lp in range(dim_s):
                            res += (self.U[i, l] * self.Ui[l, m] * self.h_se[m, n]
                                    * self.gs_e[n] * _q(self.D[l], self.Dc[lp], self.mu_e[n], t)
                                    * self.h_es[n, mp] * self.Uc[mp, lp] * self.Uci[lp, j])
        return res

    def lesser(self, i, j, t):
        return 0.5 * (self.keldysh(i, j, t) - self.retarded(i, j, t) + self.advanced(i, j, t))

    def greater(self, i, j, t):
        return 0.5 * (self.keldysh(i, j, t) + self.retarded(i, j, t) - self.advanced(i, j, t))

    def ordered(self, i, j, t):
        if t == 0:
            if (i < j):
                return self.lesser(i, j, t)
            return self.greater(i, j, t)
        return np.heaviside(t, 0) * self.greater(i, j, t) + np.heaviside(- t, 0) * self.lesser(i, j, t)

    def anti_ordered(self, i, j, t):
        if t == 0:
            if (i < j):
                return self.greater(i, j, t)
            return self.lesser(i, j, t)
        return np.heaviside(t, 0) * self.lesser(i, j, t) + np.heaviside(- t, 0) * self.greater(i, j, t)


class GreenFlatBandEq:
    '''Equilibrium Green functions of a 1 dim quantum dot array in flatband approximation at temp T=0'''

    def __init__(self, ham, hybRe, hybIm):
        # constructor as in c++ class QdArrayFlatBand
        '''
        Parameters
        ----------
            ham : central system Hamiltonian matrix
            hybRe : real part of the system-lead hybridization matrix
            hybIm : imaginary part of the system-lead hybridization matrix
        The full Hamiltonian matrix is ham + hybRe + i hybIm.
        '''

        ham = np.array(ham)
        hybRe = np.array(hybRe)
        hybIm = np.array(hybIm)

        assert(ham.shape[0] == ham.shape[1])
        assert((ham.shape == hybRe.shape) and (ham.shape == hybIm.shape))

        mat = ham + hybRe + 1j * hybIm
        self.D, self.U = np.linalg.eig(mat)
        self.Ui = np.linalg.inv(self.U)

    @classmethod
    def from_block_hamiltonian(cls, h_ss, h_se, gr_e):
        # constructor similar as nonequilibrium version GreenFlatBand
        '''
        Parameters
        ----------
            h_ss : central system Hamiltonian matrix
            h_se : system-environment Hamiltonian matrix
            gr_e : sequence of lead retarded Green functions
        '''

        h_ss = np.array(h_ss)
        h_se = np.array(h_se)

        assert((h_ss.shape[0] == h_ss.shape[1]) and (h_ss.shape[0] == h_se.shape[0]))
        assert(h_se.shape[1] == gr_e.shape[0])

        mat = h_se @ np.diag(gr_e) @ np.conj(h_se.T)
        return cls(h_ss, mat.real, mat.imag)

    def lesser(self, i, j, t):
        if t == 0:
            Df = np.zeros(shape=self.D.shape, dtype=complex)
            for l, x in enumerate(self.D):
                Df[l] = cmath.log(-x) + 1j * np.pi * np.sign(x.imag)
            return (self.U[i, :] @ np.diag(Df) @ self.Ui[:, j]).imag * (- 1j / np.pi)
        return self._green_general(True, i, j, t)

    def greater(self, i, j, t):
        if t == 0:
            Df = np.zeros(shape=self.D.shape, dtype=complex)
            for l, x in enumerate(self.D):
                Df[l] = cmath.log(-x)
            return (self.U[i, :] @ np.diag(Df) @ self.Ui[:, j]).imag * (- 1j / np.pi)
        return self._green_general(False, i, j, t)

    def _green_general(self, is_lesser, i, j, t):
        if is_lesser:
            ifun = _iless
        else:
            ifun = _igreat
        Df = np.zeros(shape=self.D.shape, dtype=complex)
        Dfc = np.zeros(shape=self.D.shape, dtype=complex)
        for l, x in enumerate(self.D):
            Df[l] = ifun(x, t)
            Dfc[l] = ifun(np.conj(x), t)
        return (self.U[i, :] @ np.diag(Df) @ self.Ui[:, j]
                - np.conj(self.U[i, :]) @ np.diag(Dfc) @ np.conj(self.Ui[:, j])) * (0.5 / np.pi)
