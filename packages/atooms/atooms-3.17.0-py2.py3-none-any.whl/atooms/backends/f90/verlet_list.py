import os
import logging
import numpy
import f2py_jit
from .linked_cells import LinkedCells
from .helpers import _merge_source

_log = logging.getLogger(__name__)


class VerletList(object):

    def __init__(self, skin=0.2, update="largest", update_period=10, helpers='helpers.f90',
                 inline=True, debug=False, parallel=False, binning="auto"):
        self.skin = skin
        self.update = update
        self.update_period = update_period
        self.displacement = None
        self.rcut = None
        self.number_of_neighbors = None
        self.neighbors = None
        self.is_adjusted = False
        self.calls = 0
        self._last_call = 0
        self.binning = binning
        self._linked_cells = None

        # Merge all sources into a unique source blob
        source = _merge_source(helpers, 'neighbor_list.f90')

        if inline:
            from f2py_jit.finline import inline_source
            source = inline_source(source)

        # TODO: refactor into a helper function
        # with open('/tmp/dump.f90', 'w') as fh:
        #     fh.write(source)
        args, opt_args = '', '-O3 -ffree-form -ffree-line-length-none'
        if debug:
            opt_args += ' -pg -fbounds-check'
        if parallel:
            opt_args += ' -fopenmp'
            args += ' -lgomp'
        extra_args = '--opt="{}" {}'.format(opt_args, args)
        self._uid = f2py_jit.build_module(source, extra_args=extra_args,
                                          metadata={'neighbors': 'neighbor_list.f90',
                                                    'helpers': helpers,
                                                    'inline': inline,
                                                    'parallel': parallel},
                                          )
        # This way we cannot deepcopy but a bit more efficient (because importing from cache locks...)
        self._f90 = f2py_jit.import_module(self._uid)

    def __str__(self):
        return f'Verlet list (skin={self.skin}, update={self.update})'

    def adjust(self, box, pos, rcut, boost=1.0):
        """
        Adjust neighbor list to positions of particles in the box and cut off distance.
        """
        from math import gamma, pi

        if self.is_adjusted:
            return
        self.rcut = rcut + self.skin
        if self.binning == "auto" or self.binning:
            self._linked_cells = LinkedCells(numpy.min(self.rcut), newton=True)
            self._linked_cells._adjust(box)
            self._linked_cells._is_adjusted = True
            if max(self._linked_cells.n_cell) <= 3:
                self._linked_cells = None
        ndim, N = pos.shape
        volume = pi**(ndim/2.) / gamma(ndim/2. + 1) * numpy.max(self.rcut)**ndim
        rho = N / numpy.product(box)
        nmax = int(rho * volume * 1.5)
        self.displacement = numpy.zeros_like(pos, order='F')
        self.number_of_neighbors = numpy.zeros(N, dtype=numpy.int32, order='F')
        self.neighbors = numpy.zeros((nmax, N), dtype=numpy.int32, order='F')
        self._pos_old = pos.copy(order='F')
        self.is_adjusted = True

    def add_displacement(self, pos, box):
        """
        Accumulate displacements assuming that PBC has been applied, hence we need to refold them.
        """
        self._f90.neighbor_list.add_displacement(pos, self._pos_old, box, self.displacement)

    def need_update(self):
        """Return True if neighbor list must be completely updated."""
        if self.update == 'periodic':
            return self.calls % self.update_period == 0
        elif self.update == 'largest':
            return self._f90.neighbor_list.need_update_largest(self.displacement, self.skin)
        else:
            raise ValueError('unknown update method {}', format(self.update))

    def compute(self, box, pos, ids):
        """Compute Verlet lists"""
        self.add_displacement(pos, box)
        if self.calls == 0 or self.need_update():
            if self._linked_cells:
                self._linked_cells.compute(box, pos, ids)
                self.neighbors = numpy.empty_like(self._linked_cells.neighbors, order='F', dtype=numpy.int32)
                self.number_of_neighbors = numpy.empty_like(self._linked_cells.number_neighbors, dtype=numpy.int32)
                self._f90.neighbor_list.compute_from_neighbors(box, pos, ids, self.rcut,
                                                               self._linked_cells.neighbors + 1, self._linked_cells.number_neighbors,
                                                               self.neighbors, self.number_of_neighbors)
            else:
                self._f90.neighbor_list.compute(box, pos, ids, self.rcut, self.neighbors, self.number_of_neighbors)
            # This parallel piece does not help
            # self._f90.neighbor_list.zero(self.displacement)
            self.displacement[:, :] = 0.
            _log.debug('updated list after {} callls'.format(self.calls - self._last_call))
            self._last_call = self.calls
        self.calls += 1
