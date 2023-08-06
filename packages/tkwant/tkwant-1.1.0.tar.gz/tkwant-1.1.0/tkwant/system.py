# -*- coding: utf-8 -*-
# Copyright 2016-2022 tkwant authors.
#
# This file is part of tkwant.  It is subject to the license terms in the file
# LICENSE.rst found in the top-level directory of this distribution and at
# https://tkwant.kwant-project.org/doc/stable/pre/license.html.
# A list of tkwant authors can be found in
# the file AUTHORS.rst at the top-level directory of this distribution and at
# https://tkwant.kwant-project.org/doc/stable/pre/authors.html.
"""Tools for extracting time-dependent parts of Kwant systems."""

import numpy as np
import inspect
import scipy.sparse as sp
import kwant

from .import _common

__all__ = ['add_time_to_params', 'ExtendedSystem',
           'is_time_dependent_function', 'orb_range', 'siteId', 'Hamiltonian']


def add_time_to_params(params, time_name, time, check_numeric_type=False):
    """Add a ``time_name: time`` key-value pair to a ``params`` dict.

    Parameters
    ----------
    params : dict or None
        Input dict. Can be empty or None. ``params`` must
        not contain the ``time_name`` key - this will raise a `KeyError`.
    time_name : obj
        A dict key to refer to the "time".
    time : obj
        The actual value of "time".
    check_numeric_type : bool, optional
        If true, check if the `time` argument is a finite real number.
        By default, no check is performed.

    Returns
    -------
    tparams : dict
        A copy of the input dict ``params`` that contains an additional
        ``time_name: time`` key-value pair.
    """
    if check_numeric_type:
        if not _common.is_type(time, 'real_number', require_finite=True):
            raise TypeError('time must be a finite real number')

    if params is None:
        tparams = {}
    else:
        if time_name in params:
            raise KeyError("'params' must not contain {}".format(time_name))
        tparams = params.copy()
    tparams[time_name] = time
    return tparams


class ExtendedSystem:
    """Hamiltonian matrix of central system + boundary conditions.

    Parameters
    ----------
    hamiltonian : `~scipy.sparse.coo_matrix`
        The Hamiltonian matrix of the central system + boundary conditions.
    boundary_slices : sequence of `slice`
        Slices into ``hamiltonian`` that project onto the boundary conditions.
    syst : `~kwant.system.FiniteSystem`
        The original kwant system.
    tmax : float, optional
        Optional maximal time until when the boundary is valid.
    """
    def __init__(self, syst, H0, boundary_slices, solver, work, tmax=None):

        self.syst = syst
        self.H0 = H0
        self.boundary_slices = boundary_slices
        self.solver = solver
        self.work = work
        self.tmax = tmax


def _hamiltonian_with_boundaries(syst, boundaries, params):
    r"""Generate the Hamiltonian with boundary conditions attached.

    Only generate the time-independent part of the Hamiltonian.
    The boundary conditions are represented by matrices :math:`h_n`
    (one per lead) that will form a direct sum with the Hamiltonian
    of the central system, :math:`H_S`:

    .. math:: H_{tot} = H_S \oplus h_0 \oplus h_1 \oplus \cdots

    In addition, coupling terms given by the lead inter-cell
    hoppings will be added between the added boundary conditions
    and the corresponding lead interface in the central system
    Hamiltonian.

    Parameters
    ----------
    syst : `~kwant.system.FiniteSystem`
        System with leads attached.
    boundaries : sequence of `~tkwant.leads.BoundaryBase`
        The boundary conditions to attach; one per lead.
    params : dict, optional
        Extra arguments to pass to the Hamiltonian of ``syst`` at the
        initial time. Must include the time argument explicitly if
        Hamiltonian is time dependent.

    Returns
    -------
    Hamiltonian H0 and first boundary slice to the lead.
    """

    if not len(syst.leads) == len(boundaries):
        raise ValueError('Number of leads= {} does not match '
                         'the number of boundaries provided= {}'
                         .format(len(syst.leads), len(boundaries)))

    # generate time-independent Hamiltonian and boundary condition
    # matrices and glue them together
    boundaries = [bc(lead, params) for lead, bc in zip(syst.leads, boundaries)]
    h_0 = syst.hamiltonian_submatrix(params=params, sparse=True)
    h_tot = sp.block_diag([h_0] + [bdy.hamiltonian for bdy in boundaries],
                          format='lil')

    boundary_slices = []

    # couple central system to boundary conditions and vice versa
    orb_offset = h_0.shape[0]
    for lead, lead_iface, boundary in zip(syst.leads, syst.lead_interfaces,
                                          boundaries):
        V = lead.inter_cell_hopping(params=params)
        # slices over lead interface orbitals within the lead
        num_iface_sites = lead.graph.num_nodes - lead.cell_size
        V_slices = [slice(*orb_range(lead, s)) for s in range(num_iface_sites)]
        # slices going *to* and *from* the boundary conditions/central system
        to_slices = [slice(*(s + orb_offset)) for s in boundary.to_slices]
        from_slices = [slice(*(s + orb_offset)) for s in boundary.from_slices]

        # iterate through all sites in the interface -- they have to
        # be treated separately, as interface sites in `syst` are not
        # necessarily grouped consecutively.
        for syst_site, V_slice in zip(lead_iface, V_slices):
            syst_slice = slice(*orb_range(syst, syst_site))
            # coupled *to* system, *from* boundary conditions
            for to_slice in to_slices:
                h_tot[syst_slice, to_slice] =\
                    V[:, V_slice].conjugate().transpose()
            # couple *from* system, *to* boundary conditions
            for from_slice in from_slices:
                h_tot[from_slice, syst_slice] = V[:, V_slice]
                pass

        # remember which orbitals correspond to this boundary condition
        boundary_slices.append(slice(orb_offset,
                                     orb_offset + boundary.hamiltonian.shape[0]))
        # now point to the start of the next boundary condition block
        orb_offset += boundary.hamiltonian.shape[0]

    return h_tot.tocsr(), boundary_slices


def is_time_dependent_function(obj, time_name):
    """Return `True` if `obj` is callable and has a time argument"""
    return callable(obj) and time_name in str(inspect.signature(obj))


def orb_range(syst, site):
    """Return the first orbital of this and the next site.

    Parameters
    ----------
    syst : `~kwant.system.System`
    site : int

    Returns
    -------
    pair of integers
    """
    assert 0 <= site < syst.graph.num_nodes
    if syst.site_ranges is None:
        raise RuntimeError('Number of orbitals not defined.\n'
                           'Declare the number of orbitals using the `norbs` '
                           'keyword argument when constructing site families')
    # Calculate the index of the run that contains the site.
    column = np.asarray(syst.site_ranges)[:, 0]
    run_idx = np.searchsorted(column, site, 'right') - 1
    # calculate the slice
    first_site, norbs, orb_offset = syst.site_ranges[run_idx]
    orb = orb_offset + (site - first_site) * norbs
    return orb, orb + norbs


class siteId:
    """Get the site index from the lattice position

    For instance, building a kwant system with:
        lat = kwant.lattice.square(a=1)
        syst = kwant.Builder()
        syst[lat(3, 4)] = 42
        syst = syst.finalized()
    the second line of:
        idx = siteId(syst, lat)
        idx(3, 4)
    will return the index of the site (whose onsite
    element has been set to 42 in the lines above) in kwant ordering.
    """

    def __init__(self, syst, lat):

        if not isinstance(syst, kwant.system.System):
            raise TypeError("'syst' must be an instance of 'kwant.system.System'")

        self._syst = syst
        self._lat = lat

    def __call__(self, *lat_coord, orbital=0):
        """Return the site index for a given lattice index.

        Parameters
        ----------
        lat_coord : tuple of int
            Lattice coordinates to refer to a lattice positions.
        orbital: int
            Orbital index

        Returns
        -------
        site_id : int
            The site index in kwant ordering.
        """
        site = self._lat(*lat_coord)
        site_id = self._syst.id_by_site[site]
        group = None
        for elem, (xx, _, _) in enumerate(self._syst.site_ranges):
            if xx > site_id:
                group = elem - 1
                break
        try:
            first_site, norbs, orb_offset = self._syst.site_ranges[group]
        except TypeError:
            raise ValueError('Group position not found')
        if not 0 <= orbital < norbs:
            raise ValueError("'0 <= orbital < norbs'; orbital={}, norbs={}"
                             .format(orbital, norbs))
        return (site_id - orb_offset) * norbs + orb_offset + orbital


def _site_to_matpos(syst, site):
    pos = syst.id_by_site[site]
    group = None
    for elem, (xx, _, _) in enumerate(syst.site_ranges):
        if xx > pos:
            group = elem - 1
            break
    try:
        first_site, norbs, orb_offset = syst.site_ranges[group]
    except TypeError:
        raise ValueError('Group position not found')
    return (pos - orb_offset) * norbs + orb_offset, norbs


class Hamiltonian:
    """Construct a Hamiltonian matrix for a single site or hopping.

    Constructing a kwant system with builder is simple.
    However, once a system is finalized, Kwant has put onsite elements and
    hoppings in some ordering and it is not evident to get the positions correctly.
    This routine constructs a Hamiltonian matrix given directly the site,
    or the hopping position. On initialization, the Hamiltonian matrix is
    construced. Calling the get method, one needs to provide the matrix
    subblock, which is inserted at the site or hopping position in
    the full Hamiltonian matrix.
    """
    def __init__(self, syst, site=None, hopping=None):
        if site is None and hopping is None:
            raise ValueError('either a site or a hopping must be present')
        if site is not None and hopping is not None:
            raise ValueError('site and hopping are mutually exclusive')
        if site is not None:
            pos1, norbs1 = _site_to_matpos(syst, site)
            pos2, norbs2 = pos1, norbs1
            self._is_hopping = False
        else:
            assert len(hopping) == 2
            pos1, norbs1 = _site_to_matpos(syst, hopping[0])
            pos2, norbs2 = _site_to_matpos(syst, hopping[1])
            self._is_hopping = True
        self._size = syst.site_ranges[-1][2]  # total hamiltonian size
        row = []
        col = []
        for i in range(norbs1):
            for j in range(norbs2):
                row.append(pos1 + i)
                col.append(pos2 + j)
        if self._is_hopping:
            self._row = np.asarray(row + col)
            self._col = np.asarray(col + row)
        else:
            self._row = np.asarray(row)
            self._col = np.asarray(col)
        return

    def get(self, submat):
        data = np.asarray(submat).flatten()
        if self._is_hopping:
            data = np.append(data, np.asarray(submat).T.conjugate().flatten())
        qt = sp.coo_matrix((data, (self._row, self._col)), dtype=complex,
                           shape=(self._size, self._size))
        qt.eliminate_zeros()
        return qt
