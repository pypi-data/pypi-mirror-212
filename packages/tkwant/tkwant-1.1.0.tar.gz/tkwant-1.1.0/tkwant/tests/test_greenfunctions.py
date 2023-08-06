# -*- coding: utf-8 -*-
# Copyright 2022 tkwant authors.
#
# This file is part of tkwant.  It is subject to the license terms in the file
# LICENSE.rst found in the top-level directory of this distribution and at
# https://tkwant.kwant-project.org/doc/stable/pre/license.html.
# A list of tkwant authors can be found in
# the file AUTHORS.rst at the top-level directory of this distribution and at
# https://tkwant.kwant-project.org/doc/stable/pre/authors.html.

"""Test module for `tkwant.greenfunctions` and `tkwant.special`"""

from .. import special, manybody, system
import kwant

import pytest
import numpy as np
from numpy.testing import (assert_array_almost_equal, assert_almost_equal)


def make_double_impurity_matrices(gamma_L, gamma_C, gamma_R, epsilon_L, epsilon_R, mu_L, mu_R):
    h_ss = np.array([[epsilon_L, -gamma_C], [-gamma_C, epsilon_R]])
    h_se = np.array([[- gamma_L, 0], [0, - gamma_R]])
    gr_e = np.array([special.g_ee_retarded(mu_L), special.g_ee_retarded(mu_R)])
    mu_e = [mu_L, mu_R]
    return h_ss, h_se, gr_e, mu_e


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


def create_system(length):

    def onsite_potential(site, time):
        """Time dependent onsite potential (static part + V(t))"""
        return 1 + v(time)

    # system building
    lat = kwant.lattice.square(a=1, norbs=1)
    syst = kwant.Builder()

    # central scattering region
    syst[(lat(x, 0) for x in range(length))] = 0
    syst[lat.neighbors()] = -1

    # add leads
    sym = kwant.TranslationalSymmetry((-1, 0))
    lead_left = kwant.Builder(sym)
    lead_left[lat(0, 0)] = 0
    lead_left[lat.neighbors()] = -1
    syst.attach_lead(lead_left)
    syst.attach_lead(lead_left.reversed())

    return syst


def test_green_quantumdot_flatband():

    # couplings
    gamma_L = 0.14
    gamma_C = 0.05
    gamma_R = 0.08

    # onsite elements
    epsilon_L = 0.5
    epsilon_R = 0.3

    # chemical potentials
    mu_L = 0
    mu_R = 0

    h_ss, h_se, gr_e, mu_e = make_double_impurity_matrices(gamma_L, gamma_C, gamma_R, epsilon_L, epsilon_R, mu_L, mu_R)

    hybRe = np.array([[0, 0], [0, 0]])
    hybIm = np.array([[- gamma_L * gamma_L, 0], [0, - gamma_R * gamma_R]])

    green_flatband = special.GreenFlatBand(h_ss, h_se, gr_e, mu_e)
    green_flatband_eq = special.GreenFlatBandEq.from_block_hamiltonian(h_ss, h_se, gr_e)
    green_flatband_alt = special.GreenFlatBandEq(h_ss, hybRe, hybIm)

    times = np.linspace(-20, 20, 21)

    for i in [0, 1]:
        for j in [0, 1]:
            for time in times:

                gless = green_flatband.lesser(i, j, time)
                gless_eq = green_flatband_eq.lesser(i, j, time)
                gless_alt = green_flatband_alt.lesser(i, j, time)

                assert_almost_equal(gless, gless_eq)
                assert_almost_equal(gless, gless_alt)

                ggreat = green_flatband.greater(i, j, time)
                ggreat_eq = green_flatband_eq.greater(i, j, time)
                ggreat_alt = green_flatband_alt.greater(i, j, time)

                assert_almost_equal(ggreat, ggreat_eq)
                assert_almost_equal(ggreat, ggreat_alt)


@pytest.mark.integtest
def test_green_retarded():

    # when not all leads are taken into account, this should also hold for the retarded function

    # parameters
    tmax = 20

    # create system
    syst = create_system(5).finalized()

    green = manybody.GreenFunction(syst, tmax, occupations=manybody.lead_occupation(chemical_potential=0))
    green_gen = manybody.greenfunctions._GreenGeneric(syst, tmax, occupations=manybody.lead_occupation(chemical_potential=None))
    assert_almost_equal(green.retarded(0, 0), -green_gen.evaluate(0, 0))

    green = manybody.GreenFunction(syst, tmax, occupations=[manybody.lead_occupation(chemical_potential=0), None])
    green_gen = manybody.greenfunctions._GreenGeneric(syst, tmax, occupations=[manybody.lead_occupation(chemical_potential=None), None])
    assert_almost_equal(green.retarded(0, 0), -green_gen.evaluate(0, 0))


@pytest.mark.integtest
def test_equal_time_green_with_density_current():

    # couplings
    gamma_L = 0.14
    gamma_C = 0.05
    gamma_R = 0.08

    # onsite elements
    epsilon_R = 0.3

    # chemical potentials
    mu_L = 0.5
    mu_R = - 0.8

    n0_wave = []
    n0_green = []

    i10_wave = []
    i10_green = []

    epsilons = np.linspace(-1, 1, 3)

    for epsilon_L_ in epsilons:

        syst, lat = make_double_impurity_system(gamma_L, gamma_C, gamma_R, epsilon_L_, epsilon_R)
        syst = syst.finalized()

        occupations = [manybody.lead_occupation(chemical_potential=mu_L),
                       manybody.lead_occupation(chemical_potential=mu_R)]

        # -- via wavefunction and density operator

        density_operator = kwant.operator.Density(syst, where=[lat(0)])
        current_operator = kwant.operator.Current(syst, where=[(lat(1), lat(0))])

        state = manybody.State(syst, tmax=1, occupations=occupations)
        density = state.evaluate(density_operator)
        current = state.evaluate(current_operator)
        n0_wave.append(density)
        i10_wave.append(current)

        # -- via greenfunction from tkwant

        idx = system.siteId(syst, lat)
        site_0 = idx(0)
        site_1 = idx(1)

        green = manybody.GreenFunction(syst, tmax=1, occupations=occupations)
        g_less_00 = green.lesser(site_0, site_0)
        g_less_10 = green.lesser(site_1, site_0)

        density = g_less_00.imag
        current = - 2 * gamma_C * g_less_10.real
        n0_green.append(density)
        i10_green.append(current)

        assert_array_almost_equal(n0_wave, n0_green)
        assert_array_almost_equal(i10_wave, i10_green)


@pytest.mark.integtest
def test_green_numeric_vs_flatband():

    green_types = {}
    green_types['lesser'] = 'G^<'
    green_types['greater'] = 'G^>'
    green_types['ordered'] = 'G^T'
    green_types['anti_ordered'] = 'G^{Tbar}'
    green_types['retarded'] = 'G^R'
    green_types['advanced'] = 'G^A'
    green_types['keldysh'] = 'G^K'

    green_data_00 = {key: [] for key in green_types.keys()}
    green_data_01 = {key: [] for key in green_types.keys()}
    green_data_10 = {key: [] for key in green_types.keys()}
    green_data_11 = {key: [] for key in green_types.keys()}

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

    syst, lat = make_double_impurity_system(gamma_L, gamma_C, gamma_R, epsilon_L, epsilon_R)
    syst = syst.finalized()

    idx = system.siteId(syst, lat)
    site_0 = idx(0)
    site_1 = idx(1)

    occupations = [manybody.lead_occupation(chemical_potential=mu_L),
                   manybody.lead_occupation(chemical_potential=mu_R)]

    times = np.linspace(0, 20, 5)

    # -- negative times
    green = manybody.GreenFunction(syst, max(times), occupations)

    for time in times[1:]:
        green.evolve(0, time)
        green.refine_intervals()

        for gtype in green_types.keys():
            green_data_00[gtype].insert(0, getattr(green, gtype)(site_0, site_0))
            green_data_01[gtype].insert(0, getattr(green, gtype)(site_0, site_1))
            green_data_10[gtype].insert(0, getattr(green, gtype)(site_1, site_0))
            green_data_11[gtype].insert(0, getattr(green, gtype)(site_1, site_1))

    # -- positive times
    green = manybody.GreenFunction(syst, max(times), occupations)

    for time in times:
        green.evolve(time, 0)
        green.refine_intervals()

        for gtype in green_types.keys():
            green_data_00[gtype].append(getattr(green, gtype)(site_0, site_0))
            green_data_01[gtype].append(getattr(green, gtype)(site_0, site_1))
            green_data_10[gtype].append(getattr(green, gtype)(site_1, site_0))
            green_data_11[gtype].append(getattr(green, gtype)(site_1, site_1))

    times_pm = np.concatenate((-times[:0:-1], times))
    green_data_00 = {key: np.array(val) for key, val in green_data_00.items()}
    green_data_01 = {key: np.array(val) for key, val in green_data_01.items()}
    green_data_10 = {key: np.array(val) for key, val in green_data_10.items()}
    green_data_11 = {key: np.array(val) for key, val in green_data_11.items()}

    matr = make_double_impurity_matrices(gamma_L, gamma_C, gamma_R, epsilon_L, epsilon_R, mu_L, mu_R)

    green_flatband = special.GreenFlatBand(*matr)

    green_data_00_ref = {key: np.array([getattr(green_flatband, key)(0, 0, t) for t in times_pm])
                         for key in green_types.keys()}
    green_data_01_ref = {key: np.array([getattr(green_flatband, key)(0, 1, t) for t in times_pm])
                         for key in green_types.keys()}
    green_data_10_ref = {key: np.array([getattr(green_flatband, key)(1, 0, t) for t in times_pm])
                         for key in green_types.keys()}
    green_data_11_ref = {key: np.array([getattr(green_flatband, key)(1, 1, t) for t in times_pm])
                         for key in green_types.keys()}

    for i, (key, gtype) in enumerate(green_types.items()):

        assert_array_almost_equal(green_data_00[key], green_data_00_ref[key], decimal=1)
        assert_array_almost_equal(green_data_01[key], green_data_01_ref[key], decimal=1)
        assert_array_almost_equal(green_data_10[key], green_data_10_ref[key], decimal=1)
        assert_array_almost_equal(green_data_11[key], green_data_11_ref[key], decimal=1)
