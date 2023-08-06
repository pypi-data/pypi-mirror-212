# -*- coding: utf-8 -*-
# Copyright 2022 tkwant authors.
#
# This file is part of tkwant.  It is subject to the license terms in the file
# LICENSE.rst found in the top-level directory of this distribution and at
# https://tkwant.kwant-project.org/doc/stable/pre/license.html.
# A list of tkwant authors can be found in
# the file AUTHORS.rst at the top-level directory of this distribution and at
# https://tkwant.kwant-project.org/doc/stable/pre/authors.html.
"""Tools for calculating time-dependent manybody Green functions."""

import copy
import numpy as np
import collections.abc

import kwantspectrum
from . import manybody, _logging, _common


__all__ = ['GreenFunction']


# set module logger
logger = _logging.make_logger(name=__name__)
log_func = _logging.log_func(logger)


class _GreenGeneric():

    # generic green function of the form
    # g(t0, t1) = i \sum_\alpha \int \frac{dE}{2 \pi} f_\alpha(E) \psi_{\alpha, E}(t0) \psi^*_{\alpha, E}(t1)
    # if f is the fermi function we get the lesser green function g^<,
    # whereas for f=1 we get (the negative) retarded function g^R

    def __init__(self, *args, refine=True, **kwargs):

        # no refine on individual wave function based on density
        self._state0 = manybody.State(*args, **kwargs, refine=False)
        self._state1 = manybody.State(*args, **kwargs, refine=False)

        self.comm = self._state0.comm

        if refine:
            self.refine_intervals()

        # by default, return the result of the higher-order rule, which in
        # our convention has to be the last element of the weight array
        self.return_element = -1

    def evolve(self, time0, time1):
        '''Evolve the Greenfunction foreward in time up to G(time0, time1)'''

        self._state0.evolve(time0)
        self._state1.evolve(time1)

    def evaluate(self, i, j, root=0):
        '''Evaluate the Greenfunction at the site positions G_{i,j}'''

        result = self._calc_green_element(i, j, root=root)

        if self.return_element is None:
            return result
        try:
            return result[self.return_element]
        except Exception:  # catch `None` result on all non-MPI root ranks
            return result

    def refine_intervals(self, atol=1E-5, rtol=1E-5, limit=2000,
                         sites=None, intervals=None):
        '''Refine the manybody integral of all diagonal G_{i,i} elements
        Parameters
        ----------
        sites : sequence of tuples (i, j) with i, j type integer, optional
            By default, refine is done on all diagonal G_{i,i} elements
            If present, refine will be done for G_{i,j} elements where i, j
            are elements of the tuples (i, j). This replaces the
            ```error_op``` argument in ```tkwant.manybody.State.refine()```
        other parameters as for ```tkwant.manybody.State.refine()```
        '''

        assert _common.is_type(atol, 'real_number')
        if atol < 0:
            raise ValueError('atol={} is negative.'.format(atol))
        assert _common.is_type(rtol, 'real_number')
        if rtol < 0:
            raise ValueError('rtol={} is negative.'.format(rtol))
        assert _common.is_type(limit, 'integer')
        if limit <= 1:
            raise ValueError('limit={} must be > 1.'.format(limit))
        tol = min(1E-14, 0.5 * (atol + rtol))

        time0 = self._state0.time
        time1 = self._state1.time

        if sites is None:
            sites = [(i, i) for i in range(len(self._state0.extended_syst.syst.sites))]

        def green_with_error(_intervals):
            green = []
            errors = []
            for interval in _intervals:
                green_ = []
                errors_ = []
                for elem in sites:
                    error, kronrod = self._error_estimate_quadpack(interval,
                                                                   elem[0], elem[1],
                                                                   return_estimate=True,
                                                                   tol=0.5 * (atol + rtol))
                    green_.append(kronrod)
                    errors_.append(error)
                green.append(green_)
                errors.append(errors_)
            return np.array(green), np.array(errors)

        if intervals is None:
            intervals = self._state0.get_intervals()
        else:
            intervals = copy.deepcopy(intervals)
            if not isinstance(intervals, collections.abc.Iterable):
                intervals = [intervals]

        # refine only intervals with Gauss-Kronrod quadrature
        intervals[:] = [interval for interval in intervals
                        if interval.quadrature == 'kronrod']

        results, errors = green_with_error(intervals)

        result = np.sum(results, axis=0)  # sum of the integrals over the subintervals
        errsum = np.sum(errors, axis=0)  # sum of the errors over the subintervals

        i = 0
        while True:  # loop until converged

            errbnd = np.maximum(atol, rtol * np.abs(result))  # requested accuracy

            # order all intervals by error, decreasing order
            try:
                max_error_per_interval = np.max(errors - errbnd[np.newaxis, :], axis=1)
            except:
                max_error_per_interval = errors - errbnd

            error_idx = np.argsort(max_error_per_interval)[::-1]

            intervals = [intervals[i] for i in error_idx]
            results = results[error_idx]
            errors = errors[error_idx]
            max_error_per_interval = max_error_per_interval[error_idx]

            errmax = errors[0]
            resultmax = results[0]

            logger.info('refinement step={}, time0={}, time1={}, max errsum={}, '
                        'min errbnd={}, total number of intervals={}'.
                        format(i, time0, time1, np.max(errsum), np.min(errbnd), len(intervals)))
            for j, (inte, err) in enumerate(zip(intervals, errors)):
                logger.debug("interval_num={}, {}, max error={}".format(j, inte, np.max(err)))

            if (errsum <= errbnd).all():  # converged
                logger.info('refinement converged')
                break

            if len(intervals) >= limit:
                logger.warning('maximum number of intervals reached')
                break

            # bisect the interval with the largest error
            interval_largest_error = intervals.pop(0)
            new_intervals = manybody._split_interval(interval_largest_error, 2)
            intervals += new_intervals

            # update the intervals stored in the solver, evolve to current time
            self._state0._remove_interval(interval_largest_error)
            self._state1._remove_interval(interval_largest_error)
            for interval in new_intervals:
                self._state0._add_interval(interval, tol=tol)
                self._state1._add_interval(interval, tol=tol)
            self.evolve(time0, time1)

            # recalculate the error and observable estimate
            new_results, new_errors = green_with_error(new_intervals)

            results = np.append(results, new_results, axis=0)
            errors = np.append(errors, new_errors, axis=0)

            results = np.delete(results, 0, axis=0)
            errors = np.delete(errors, 0, axis=0)

            result = result + new_results[0] + new_results[1] - resultmax
            errsum = errsum + new_errors[0] + new_errors[1] - errmax
            i += 1

        return np.max(errsum), intervals, errors

    def estimate_error(self, i, j, intervals=None, full_output=False):
        '''Estimate the error of the manybody integral'''

        sum_up = False
        if intervals is None:
            intervals = self._state0.get_intervals()
            sum_up = True
        if isinstance(intervals, collections.abc.Iterable):
            errors_per_interval = np.array([self._error_estimate_quadpack(interval, i, j)
                                            for interval in intervals])
            if sum_up:
                errors = np.sum(errors_per_interval, axis=0)
                if not full_output:
                    errors = np.max(errors)
            else:
                if full_output:
                    errors = errors_per_interval
                else:
                    errors = np.array([np.max(err) for err in errors_per_interval])
        else:
            if full_output:
                errors = estimate(intervals, error_op)
            else:
                errors = np.max(estimate(intervals, error_op))
        return errors

    def _calc_green_element(self, i, j, keys=None, root=0, return_integrand=False):
        '''Evaluation of a Green function element and the integrand'''

        # the mpi rank distribution is deterministic, so the we will have
        # the same keys on the same mpi rank

        local_keys = self._state0.manybody_wavefunction.psi.local_keys()
        if keys is None:
            keys = local_keys
        else:  # intersection between given keys and keys on MPI rank
            keys = list(set(keys) & set(local_keys))

        integral = 0  # local integral part on mpi process

        # calculate weighted sum (partly on every rank)
        if return_integrand:
            integrand = {}
            for key in keys:
                psi_0 = self._state0.manybody_wavefunction.psi.local_data()[key].psi()
                psi_1 = np.conj(self._state1.manybody_wavefunction.psi.local_data()[key].psi())
                psi2 = psi_0[i] * psi_1[j]
                weight = 1j * self._state0.manybody_wavefunction.tasks[key].weight
                phys_weight = 1j * self._state0.manybody_wavefunction.tasks[key].phys_weight
                integral += np.outer(weight, psi2)
                integrand[key] = phys_weight * psi2
        else:
            for key in keys:
                psi_0 = self._state0.manybody_wavefunction.psi.local_data()[key].psi()
                psi_1 = np.conj(self._state1.manybody_wavefunction.psi.local_data()[key].psi())
                psi2 = psi_0[i] * psi_1[j]
                weight = 1j * self._state0.manybody_wavefunction.tasks[key].weight
                integral += np.outer(weight, psi2)

        if root is None:
            result = self.comm.allreduce(integral)
        else:
            result = self.comm.reduce(integral, root=root)
        result = np.squeeze(result)

        if return_integrand:
            return result, integrand
        return result

    def _evaluate_interval(self, interval, i, j, root=None, return_integrand=False):
        """Evaluate the statistical average over the given interval.

        Parameters
        ----------
        interval : `tkwant.manybody.Interval`
            Interval over which the manybody sum should be calculated.
        i, j : integer
            Green function element
        root : int or None, optional
            root receive the result, other rank receive None.
            If root is None all ranks receive the result.
        return_integrand : bool, optional
            If true, return also the integrand of the integral.

        Returns
        -------
        result : `~numpy.ndarray`
            The green function element, integrated over the interval.
        integrand : dict, optional
            The integrand to the integral. Only returned if ``return_integrand``
            it true.
        """
        keys = self._state0._get_keys_from_interval(interval)
        return self._calc_green_element(i, j, keys=keys, root=root,
                                        return_integrand=return_integrand)

    def _error_estimate_quadpack(self, interval, i, j, return_estimate=False, tol=1e-5):
        '''Estimate an manybody integral error of a given interval for the G_{i,j} element.'''

        if not interval.quadrature == 'kronrod':
            raise ValueError('quadpack error estimate works only on '
                             'Gauss-Kronrod quadrature intervals')

        (gauss, kronrod), func = self._evaluate_interval(interval, i, j,
                                                         return_integrand=True)

        dk = interval.kmax - interval.kmin
        assert dk > 0
        assert tol > 0
        kronrod_scaled = kronrod / dk

        integral = 0
        for key, f in func.items():
            kronrod_weight = self._state0.manybody_wavefunction.tasks[key].math_weight[1]
            integral += kronrod_weight * np.abs(f - kronrod_scaled)
        ik = self.comm.allreduce(integral)

        ik = np.where(ik > 0, ik, tol)  # ik can become exactly zero

        assert (ik > 0).all()
        tmp = 200 * np.abs(gauss - kronrod) / ik
        error = np.squeeze(ik * np.minimum(1, tmp * np.sqrt(tmp)))
        if return_estimate:
            return error, kronrod
        return error


class GreenFunction():

    # This class has a lazy init, evolve and refine_intervals routine.
    # The calls to these methods is saved in a joblist and the actual calls
    # are only executed before the the evaluate() method of the stored green
    # functions (green_lesser, green_retarded) is called.
    # This is for performance reasons and guarantees that only the function which
    # is really required (green_lesser and/or green_retarded) is actually calculated.

    '''

    Parameters
    ----------
    init positional and keyword arguments as ```tkwant.manybody.State```.
    The remaining parameters are:
    i, j : integer
        Green function element G_{i,j}
    time0, time1 : float, float
        Green function times G_(time0, time1)
    root : int or None, optional
        MPI root receive the result, other rank receive None.
        If root is None all ranks receive the result.
    There is no ```evaluate()``` method, but a method to evaluate
    each Green function type, such as ```.lesser()``` for G^<, ```.greater()```
    for G^> and so on.
    '''

    def __init__(self, *args, **kwargs):

        logger.debug('init GreenFunction')

        self._args = args
        self._kwargs = kwargs
        self._jobs_lesser = []
        self._jobs_retarded = []
        self._green_lesser = None
        self._green_retarded = None
        self._time0 = 0
        self._time1 = 0

    def evolve(self, time0, time1):
        if time0 < self._time0:
            raise ValueError("time0={} < previous time0={}".format(time0, self._time0))
        if time1 < self._time1:
            raise ValueError("time1={} < previous time1={}".format(time1, self._time1))
        self._jobs_lesser.append(('_evolve_lesser', (time0, time1), {}))
        self._jobs_retarded.append(('_evolve_retarded', (time0, time1), {}))
        self._time0 = time0
        self._time1 = time1

    def refine_intervals(self, *args, **kwargs):
        self._jobs_lesser.append(('_refine_lesser', args, kwargs))
        self._jobs_retarded.append(('_refine_retarded', args, kwargs))

    def lesser(self, i, j, root=0):
        if self._green_lesser is None:
            self._init_lesser()
        self._do_jobs(self._jobs_lesser)
        return self._green_lesser.evaluate(i, j, root)

    def retarded(self, i, j, root=0):
        if self._time0 < self._time1:
            return 0
        if self._green_retarded is None:
            self._init_retarded()
        self._do_jobs(self._jobs_retarded)
        res = self._green_retarded.evaluate(i, j, root)
        if res == None:
            return
        return - res

    def advanced(self, i, j, root=0):
        if self._time0 >= self._time1:
            return 0
        if self._green_retarded is None:
            self._init_retarded()
        self._do_jobs(self._jobs_retarded)
        return self._green_retarded.evaluate(j, i, root)

    def greater(self, i, j, root=0):
        # G^R − G^A = G^> − G^<
        lesser = self.lesser(i, j, root)
        if self._time0 >= self._time1:
            gra = self.retarded(i, j, root)
            sgn = 1
        else:
            gra = self.advanced(i, j, root)
            sgn = -1
        if lesser == None:
            return
        return lesser + sgn * gra

    def ordered(self, i, j, root=0):
        if self._time0 >= self._time1:
            return self.greater(i, j, root)
        return self.lesser(i, j, root)

    def anti_ordered(self, i, j, root=0):
        if self._time0 >= self._time1:
            return self.lesser(i, j, root)
        return self.greater(i, j, root)

    def keldysh(self, i, j, root=0):
        greater = self.greater(i, j, root)
        lesser = self.lesser(i, j, root)
        if greater == None:
            return
        return greater + lesser

    def _init_lesser(self):
        logger.debug('init G^<')
        self._green_lesser = _GreenGeneric(*self._args, **self._kwargs)

    def _init_retarded(self):

        logger.debug('init G^R')

        #  get the occuption form the arguments (positional or keyword)
        if len(self._args) > 2:
            occupations = self._args[2]
        else:
            occupations = self._kwargs.get('occupations', None)

        #  fill up all bands up to the highest energy
        # respect that not all bands/leads might be taken into acount
        if occupations is None:
            occupations = manybody.lead_occupation(chemical_potential=None)
        else:
            try:  # sequence of occupations
                full_occupations = []
                for occ in occupations:
                    if occ is None:  # if a lead is not counted, it should stay unoccupied
                        full_occupations.append(None)
                    else:
                        full_occupations.append(manybody.lead_occupation(chemical_potential=None))
                occupations = full_occupations
            except Exception:  # if occupations is not iterable
                occupations = manybody.lead_occupation(chemical_potential=None)

        #  change the occuption in args (positional) or kwargs (keyword)
        kwargs = copy.deepcopy(self._kwargs)  # dict is mutable !
        if len(self._args) > 2:
            arglist = list(self._args)
            arglist[2] = occupations
            args = tuple(arglist)
        else:
            args = self._args
            kwargs['occupations'] = occupations

        self._green_retarded = _GreenGeneric(*args, **kwargs)

    def _do_jobs(self, joblist):
        # loop over all jobs to do, reinitialize list afterwards
        for jobname, args, kwargs in joblist:
            logger.debug('jobname={}, args={}, kwargs={}'.format(jobname, args, kwargs))
            job = getattr(self, jobname)
            job(*args, **kwargs)
        joblist.clear()

    def _refine_lesser(self, *args, **kwargs):
        logger.debug('refine G^<')
        self._green_lesser.refine_intervals(*args, **kwargs)

    def _refine_retarded(self, *args, **kwargs):
        logger.debug('refine G^R')
        self._green_retarded.refine_intervals(*args, **kwargs)

    def _evolve_lesser(self, time0, time1, **kwargs):
        logger.debug('evolve G^<')
        self._green_lesser.evolve(time0, time1)

    def _evolve_retarded(self, time0, time1, **kwargs):
        logger.debug('evolve G^R')
        self._green_retarded.evolve(time0, time1)

    def estimate_error_lesser(self, i, j, intervals=None, full_output=False):
        self._do_jobs(self._jobs_lesser)
        return self._green_lesser.estimate_error(i, j, intervals, full_output)
