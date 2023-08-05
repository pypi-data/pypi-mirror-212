"""
Module qes_read_module


Defined at qes_read_module.fpp lines 13-10452

"""
from __future__ import print_function, absolute_import, division
import _qepy
import f90wrap.runtime
import logging

_arrays = {}
_objs = {}


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "qes_read_module".')

for func in _dt_array_initialisers:
    func()
