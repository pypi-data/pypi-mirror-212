# -*- coding: utf-8 -*-
# Copyright 2016 tkwant authors.
#
# This file is part of tkwant.  It is subject to the license terms in the file
# LICENSE.rst found in the top-level directory of this distribution and at
# https://tkwant.kwant-project.org/doc/stable/pre/license.html.
# A list of tkwant authors can be found in
# the file AUTHORS.rst at the top-level directory of this distribution and at
# https://tkwant.kwant-project.org/doc/stable/pre/authors.html.

"""Test module for `tkwant.system`"""

import numpy as np
import kwant
import pytest

from .. import system, leads, onebody
from .common import (make_chain, make_simple_lead, make_complex_lead,
                     make_system_with_leads, check_boundary_hamiltonian)


def test_orbital_slices():

    def check(fsyst):
        slices = (system.orb_range(fsyst, i) for i in range(len(fsyst.sites)))
        stop = 0
        for site, (start_orb, stop_orb) in zip(fsyst.sites, slices):
            assert start_orb == stop
            stop += site.family.norbs
            assert stop_orb == stop
            assert site.family.norbs == (stop_orb - start_orb)

    # uniform families
    lat, syst = make_chain(3, norbs=1)
    check(syst.finalized())
    lat, syst = make_chain(3, norbs=2)
    check(syst.finalized())
    # mixed families
    lat = kwant.lattice.chain(name='a', norbs=1)
    lat2 = kwant.lattice.chain(name='b', norbs=2)
    syst = kwant.Builder()
    syst[map(lat, range(3))] = 2
    syst[map(lat2, range(3))] = 2 * np.eye(2)
    check(syst.finalized())


@pytest.mark.parametrize('lead_maker', [make_simple_lead, make_complex_lead])
def test_hamiltonian(lead_maker):
    ncells = 10
    strength = 10
    degree = 6
    # construct
    syst = make_system_with_leads(kwant.lattice.square(norbs=1),
                                  lead_maker)
    fsyst = syst.finalized()
    boundaries = [leads.SimpleBoundary(10),
                  leads.MonomialAbsorbingBoundary(ncells, strength, degree)]
    Hext = onebody.make_extended_system(fsyst, onebody.solvers.default, boundaries)

    # test shapes
    norbs_central = len(fsyst.sites)
    norbs_leads = [lead.cell_size * ncells for lead in fsyst.leads]
    assert Hext.H0.shape[0] == Hext.H0.shape[1]
    assert Hext.H0.shape[0] == norbs_central + sum(norbs_leads)

    # test absorbing regions and coupling

    def absorbing(i):
        n = degree
        return -1j * np.eye(norbs) * ((n + 1) * strength *
                                      i**n / ncells**(n + 1))

    loop = zip(fsyst.leads, fsyst.lead_interfaces, Hext.boundary_slices,
               boundaries)
    for lead, lead_interface, slc, bdy in loop:
        norbs = lead.cell_size
        norbs_iface = lead.graph.num_nodes - lead.cell_size
        V = lead.inter_cell_hopping()
        V_dag = V.conjugate().transpose()
        if isinstance(bdy, leads.MonomialAbsorbingBoundary):
            def onsite(i):
                return lead.cell_hamiltonian() + absorbing(i)
        else:
            def onsite(i):
                return lead.cell_hamiltonian()
        check_boundary_hamiltonian(Hext.H0[slc, slc],
                                   norbs, norbs_iface, onsite, lambda i: V)

        # test coupling -- uses fact that norbs=1
        for i, iface_site in enumerate(lead_interface):
            bdy_iface = slice(slc.start, slc.start + norbs)
            iface_slice = slice(iface_site, iface_site + 1)
            assert np.allclose(Hext.H0[bdy_iface, iface_slice].todense(),
                               V[:, i:(i + 1)])
            assert np.allclose(Hext.H0[iface_slice, bdy_iface].todense(),
                               V_dag[i:(i + 1), :])


@pytest.mark.parametrize('lead_maker', [make_simple_lead])
def test_hamiltonian_with_boundaries_exceptions(lead_maker):

    # construct
    syst = make_system_with_leads(kwant.lattice.square(norbs=1), lead_maker)
    fsyst = syst.finalized()

    # too less boundary conditions
    boundaries = [leads.SimpleBoundary(10)]
    with pytest.raises(ValueError) as exc:
        onebody.make_extended_system(fsyst, onebody.solvers.default, boundaries)
    assert 'Number of leads= 2 does not match the number of boundaries provided= 1' in str(exc.value)

    # too many boundary conditions
    boundaries = [leads.SimpleBoundary(10)] * 3
    with pytest.raises(ValueError) as exc:
        onebody.make_extended_system(fsyst, onebody.solvers.default, boundaries)
    assert 'Number of leads= 2 does not match the number of boundaries provided= 3' in str(exc.value)


def test_is_time_dependent_function():
    def time_dependent(zeit):
        pass
    not_a_function = 'time'
    assert system.is_time_dependent_function(time_dependent, 'zeit')
    assert system.is_time_dependent_function(time_dependent, 'time') is False
    assert system.is_time_dependent_function(not_a_function, 'time') is False


def test_add_time_to_params():
    params_example = {'some_key': 2}
    time_name = 'my_time'
    time_value = 42

    # check against reference result
    tparams = system.add_time_to_params(params_example, time_name=time_name,
                                        time=time_value)
    assert isinstance(tparams, dict)
    assert tparams == {'some_key': 2, 'my_time': 42}

    # check for possible inputs
    for params in [None, {}, params_example]:
        tparams = system.add_time_to_params(params, time_name=time_name,
                                            time=time_value)
        assert isinstance(tparams, dict)
        assert time_name in tparams
        assert tparams[time_name] == time_value

        # check that having a dict with already the time input gives an error
        with pytest.raises(KeyError) as exc:
            system.add_time_to_params(tparams, time_name=time_name,
                                      time=time_value)
        error_string = str(exc.value).lstrip('\"').rstrip('\"')  # remove etra quotes
        assert error_string == "'params' must not contain my_time"

    # check that the (mutable) input dict is really copied and no reference created
    params_copy = params_example.copy()
    tparams = system.add_time_to_params(params_copy, time_name=time_name,
                                        time=time_value)
    tparams = {}
    assert params_copy == params_example
